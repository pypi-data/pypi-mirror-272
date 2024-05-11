from __future__ import annotations

import math
from pathlib import Path
from typing import Optional, Tuple, Union, cast

import torch
import torch.nn.functional as F
from einops import einsum, rearrange, repeat
from safetensors.torch import load_file
from torch import Tensor, nn

from openelm_pytorch.config import (
    ModelConfig,
    PretrainedModelConfig,
    PretrainedModelName,
)
from openelm_pytorch.utils import make_divisible


class RMSNorm(nn.Module):
    def __init__(
        self,
        dims: int,
        eps: float = 1e-6,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dims, device=device, dtype=dtype))
        self.eps = eps

    def forward(self, x: Tensor) -> Tensor:
        scale: float = 1 / x.size(-1) ** 0.5
        norm = (x).norm(p=2, dim=-1, keepdim=True) * scale
        return self.weight * x / (norm + self.eps)


class RoPE(nn.Module):
    def __init__(self, dim: int, base: float = 10000, scale: float = 1.0):
        super().__init__()
        self.dim = dim
        self.base = base
        self.scale = scale

    def create_cos_sin_theta(
        self,
        n: int,
        d: int,
        offset: int = 0,
        base: float = 10000,
        scale: float = 1.0,
        dtype: torch.dtype | None = None,
        device: torch.device | None = None,
    ) -> tuple[Tensor, Tensor]:
        # TODO: Cache cos and sin values for performance.
        half_d = d // 2
        positions = torch.arange(offset, n, device=device, dtype=dtype) * scale
        freqs = torch.exp(
            -torch.arange(0.0, half_d, device=device, dtype=dtype)
            * (math.log(base) / half_d)
        )
        theta = positions[:, None] * freqs[None, :]
        return torch.cos(theta), torch.sin(theta)

    def forward(self, x: Tensor, offset: int = 0) -> Tensor:
        shape = x.shape
        x = rearrange(x, "b ... s d -> (b ...) s d")
        n = x.shape[1] + offset
        costheta, sintheta = self.create_cos_sin_theta(
            n=n,
            d=self.dim,
            offset=offset,
            base=self.base,
            scale=self.scale,
            device=x.device,
            dtype=x.dtype,
        )

        x1 = x[..., : self.dim // 2]
        x2 = x[..., self.dim // 2 : self.dim]
        rx1 = x1 * costheta - x2 * sintheta
        rx2 = x1 * sintheta + x2 * costheta

        rx = torch.cat([rx1, rx2], dim=-1)
        return rx.view(shape)


class MultiHeadAttention(nn.Module):
    def __init__(
        self,
        model_dim: int,
        num_query_heads: int,
        num_kv_heads: int,
        head_dim: int,
        rope_freq_constant: float,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ):
        super().__init__()
        assert num_query_heads % num_kv_heads == 0

        self.qkv_proj = nn.Linear(
            model_dim,
            (num_query_heads + num_kv_heads + num_kv_heads) * head_dim,
            bias=False,
            device=device,
            dtype=dtype,
        )

        self.pos_embedding = RoPE(head_dim, base=rope_freq_constant)
        self.q_norm = RMSNorm(head_dim, device=device, dtype=dtype)
        self.k_norm = RMSNorm(head_dim, device=device, dtype=dtype)

        self.out_proj = nn.Linear(
            num_query_heads * head_dim,
            model_dim,
            bias=False,
            device=device,
            dtype=dtype,
        )

        self.head_dim = head_dim
        self.num_q_heads = num_query_heads
        self.num_k_heads = num_kv_heads
        self.num_v_heads = num_kv_heads
        self.model_dim = model_dim
        self.num_groups = self.num_q_heads // self.num_k_heads
        self.scale: float = 1 / (head_dim**0.5)
        self.reset_parameters()

    @classmethod
    def from_config(
        cls,
        config: ModelConfig,
        layer_idx: int,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ) -> MultiHeadAttention:
        return cls(
            model_dim=config.model_dim,
            num_query_heads=config.num_query_heads[layer_idx],
            num_kv_heads=config.num_kv_heads[layer_idx],
            head_dim=config.head_dim,
            rope_freq_constant=config.rope_freq_constant,
            device=device,
            dtype=dtype,
        )

    def forward(
        self,
        x: Tensor,
        past_key_value: Optional[Tuple[Tensor, Tensor]] = None,
        use_kv_cache: bool = False,
        is_causal: bool = False,
    ) -> Tuple[Tensor, Optional[Tuple[Tensor, Tensor]]]:
        qkv = self.qkv_proj.forward(x)
        qkv = rearrange(qkv, "b s (h d) -> b h s d", d=self.head_dim)
        queries = qkv[:, : self.num_q_heads]
        keys = qkv[:, self.num_q_heads : self.num_q_heads + self.num_k_heads]
        values = qkv[:, self.num_q_heads + self.num_k_heads :]

        queries = self.q_norm.forward(queries)
        keys = self.k_norm.forward(keys)

        if use_kv_cache:
            if past_key_value is not None:
                past_keys = past_key_value[0]
                past_values = past_key_value[1]
                queries = self.pos_embedding.forward(queries, offset=past_keys.shape[2])
                keys = self.pos_embedding.forward(keys, offset=past_keys.shape[2])
                keys = torch.cat([past_keys, keys], dim=2)
                values = torch.cat([past_values, values], dim=2)
            else:
                queries = self.pos_embedding.forward(queries)
                keys = self.pos_embedding.forward(keys)

            past_key_value = (keys, values)

        if self.num_groups != 1:
            # NOTE: There is a big difference between 'torch.repeat' and 'mx.repeat'!
            # 'mx.repeat' repeats each element 'n' times, whereas 'torch.repeat' repeats
            # the entire tensor dimension 'n' times.  To achieve the same behavior,
            # we repeat along a new axis, and then rearrange the tensor.
            keys = rearrange(
                repeat(keys, "b h s d -> b h g s d", g=self.num_groups),
                "b h g s d -> b (h g) s d",
            )
            values = rearrange(
                repeat(values, "b h s d -> b h g s d", g=self.num_groups),
                "b h g s d -> b (h g) s d",
            )

        # NOTE: Because the GQA key/value tensors are repeated above, the QKV tensors
        # all have the same number of heads!  This is slightly less efficient than
        # the optimal implementation (without repeating keys/values), but it reduces
        # the attention computation below to vanilla scaled dot-product attention.
        attention_output = F.scaled_dot_product_attention(
            query=queries,
            key=keys,
            value=values,
            is_causal=is_causal,
            scale=self.scale,
        )
        # Fold the attention heads back into the model dimension.
        attention_output = rearrange(attention_output, "b h s d -> b s h d")
        attention_output = rearrange(attention_output, "b s h d -> b s (h d)")

        out = self.out_proj.forward(attention_output)
        return out, past_key_value

    def reset_parameters(self):
        """The initialization scheme is followed, following `OPT
        <https://arxiv.org/pdf/2205.01068.pdf>`_.
        """
        std = self.model_dim**-0.5
        nn.init.normal_(self.qkv_proj.weight, std=std)
        nn.init.normal_(self.out_proj.weight, std=std)


class FeedForwardNetwork(nn.Module):
    def __init__(
        self,
        dim: int,
        hidden_dim: int,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ):
        super().__init__()
        self.dim = dim  # used by reset_parameters
        # NOTE: The first linear layer is split into two parts. The first part is used
        # to compute Swish activation, which is then multiplied by the second part.
        # This is equivalent to having two separate linear layers, which together
        # form a gated linear unit (GLU).
        self.proj_1 = nn.Linear(
            dim, 2 * hidden_dim, bias=False, device=device, dtype=dtype
        )
        self.act = nn.SiLU()  # AKA Swish
        self.proj_2 = nn.Linear(hidden_dim, dim, bias=False, device=device, dtype=dtype)

    @classmethod
    def from_config(
        cls,
        config: ModelConfig,
        layer_idx: int,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ) -> FeedForwardNetwork:
        ffn_multiplier = config.ffn_multipliers[layer_idx]
        hidden_dim = make_divisible(
            ffn_multiplier * config.model_dim, divisor=config.ffn_dim_divisor
        )
        return cls(
            dim=config.model_dim, hidden_dim=hidden_dim, device=device, dtype=dtype
        )

    def forward(self, x: Tensor) -> Tensor:
        y = self.proj_1.forward(x)
        y1, y2 = y.chunk(2, dim=-1)
        y = self.act(y1) * y2
        return self.proj_2(y)

    def reset_parameters(self):
        """The initialization scheme is followed, following `OPT
        <https://arxiv.org/pdf/2205.01068.pdf>`_.
        """
        std = self.dim**-0.5
        nn.init.normal_(self.proj_1.weight, std=std)
        nn.init.normal_(self.proj_2.weight, std=std)


class TransformerDecoderLayer(nn.Module):
    def __init__(
        self,
        attn: MultiHeadAttention,
        attn_norm: RMSNorm,
        ffn: FeedForwardNetwork,
        ffn_norm: RMSNorm,
    ):
        super().__init__()
        self.attn_norm = attn_norm
        self.attn = attn
        self.ffn_norm = ffn_norm
        self.ffn = ffn

    @classmethod
    def from_config(
        cls,
        config: ModelConfig,
        layer_idx: int,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ) -> TransformerDecoderLayer:
        attn = MultiHeadAttention.from_config(
            config, layer_idx=layer_idx, device=device, dtype=dtype
        )
        attn_norm = RMSNorm(config.model_dim, device=device, dtype=dtype)
        ffn = FeedForwardNetwork.from_config(
            config, layer_idx=layer_idx, device=device, dtype=dtype
        )
        ffn_norm = RMSNorm(config.model_dim, device=device, dtype=dtype)
        return cls(attn=attn, attn_norm=attn_norm, ffn=ffn, ffn_norm=ffn_norm)

    def forward(
        self,
        x: Tensor,
        past_key_value: tuple[Tensor, Tensor] | None = None,
        use_kv_cache: bool = False,
        is_causal: bool = False,
    ) -> Tuple[Tensor, Optional[Tuple[Tensor, Tensor]]]:
        # Pre-norm attention
        y_attn = self.attn_norm(x)
        y_attn, past_key_value = self.attn.forward(
            y_attn,
            past_key_value=past_key_value,
            use_kv_cache=use_kv_cache,
            is_causal=is_causal,
        )
        y_attn = x + y_attn

        # Pre-norm FFN
        y_ffn = y_attn + self.ffn(self.ffn_norm(y_attn))
        return y_ffn, past_key_value

    def reset_parameters(self):
        self.attn.reset_parameters()
        self.ffn.reset_parameters()


class OpenELM(nn.Module):
    def __init__(
        self,
        embeddings: nn.Embedding,
        layers: nn.ModuleList,
        norm: nn.Module,
    ) -> None:
        super().__init__()
        self.token_embeddings = embeddings
        self.layers = layers
        self.norm = norm

    @classmethod
    def from_config(
        cls,
        config: ModelConfig,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ) -> OpenELM:
        embeddings = nn.Embedding(
            num_embeddings=config.vocab_size,
            embedding_dim=config.model_dim,
            device=device,
            dtype=dtype,
        )
        layers = nn.ModuleList(
            [
                TransformerDecoderLayer.from_config(
                    config, layer_idx=layer_idx, device=device, dtype=dtype
                )
                for layer_idx in range(config.num_transformer_layers)
            ]
        )
        norm = RMSNorm(config.model_dim, device=device, dtype=dtype)
        return cls(embeddings=embeddings, layers=layers, norm=norm)

    @classmethod
    def from_pretrained(
        cls,
        model_name: str | PretrainedModelName,
        save_dir: str | Path | None = None,
        device: torch.device | str = "cpu",
        dtype: torch.dtype | None = None,
    ) -> OpenELM:
        config = PretrainedModelConfig.from_name(model_name)
        # NOTE: Initialize empty weights using the 'meta' device, so we don't
        # need to allocate 2x the memory to load each model.
        model = cls.from_config(config.config, device=torch.device("meta"), dtype=dtype)

        if save_dir is None:
            save_dir = Path(torch.hub.get_dir()) / "openelm-pytorch" / model_name
        elif isinstance(save_dir, str):
            save_dir = Path(save_dir)
        save_dir.mkdir(exist_ok=True, parents=True)

        # To simplify the rest of this function, convert to a list of URIs to load
        # the weights from.  (A single URI is a special case of a list of URIs.)
        if isinstance(config.weights_uri, str):
            weights_uris = [config.weights_uri]
        else:
            weights_uris = config.weights_uri

        # Load each set of weights from file, and add them to the state dictionary.
        state_dict: dict[str, Tensor] = {}
        num_files = len(weights_uris)
        for i, weights_uri in enumerate(weights_uris, 1):
            weights_path = save_dir / f"weights-{i:05d}-of-{num_files:05d}.safetensors"
            if not weights_path.exists():
                print(f"Downloading model weights to {weights_path}...")
                torch.hub.download_url_to_file(weights_uri, str(weights_path))

            device_str = str(device) if isinstance(device, torch.device) else device
            state_dict.update(load_file(weights_path, device=device_str))

        # Strip the 'transformer.' prefix from the state_dict keys.  Needed, because
        # the Huggingface version of the model has a top-level 'transformer' module,
        # whereas this implementation does not.
        model.load_state_dict(
            {k.removeprefix("transformer."): v for k, v in state_dict.items()},
            assign=True,  # Needed, because we used device='meta' above.
        )
        return model.eval()

    def forward(
        self,
        input_ids: Tensor,
        past_key_values: list[tuple[Tensor, Tensor] | None] | None = None,
        use_kv_cache: bool = False,
        is_causal: bool = True,
    ) -> Union[Tensor, dict[str, Tensor | list[tuple[Tensor, Tensor] | None]]]:
        num_layers = len(self.layers)
        if past_key_values is None:
            past_key_values = [None] * num_layers
        past_key_values = cast(list[tuple[Tensor, Tensor] | None], past_key_values)

        x = self.token_embeddings.forward(input_ids)
        is_causal = is_causal and x.shape[1] > 1

        for i, layer in enumerate(self.layers):
            layer = cast(TransformerDecoderLayer, layer)
            x, past_key_values[i] = layer.forward(
                x,
                past_key_value=past_key_values[i],
                use_kv_cache=use_kv_cache,
                # NOTE: If using KV cache, do not use causal attention.
                is_causal=(is_causal and x.shape[1] > 1),
            )

        x = self.norm(x)
        logits = einsum(x, self.token_embeddings.weight, "b s d, e d -> b s e")

        if use_kv_cache:
            assert past_key_values is not None
            return {"logits": logits, "past_key_values": past_key_values}
        else:
            return logits

    def reset_parameters(self) -> None:
        std = self.token_embeddings.embedding_dim**-0.5
        nn.init.normal_(self.token_embeddings.weight, std=std)

        for layer in self.layers:
            layer = cast(TransformerDecoderLayer, layer)
            layer.reset_parameters()
