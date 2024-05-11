import torch

from openelm_pytorch.openelm import OpenELM
from openelm_pytorch.tokenizer import Tokenizer
from openelm_pytorch.utils import get_torch_device

# From "The Treasure Island" by R.L.Stevenson, public domain.
PROMPT = (
    "Squire Trelawney, Dr. Livesey, and the rest of these gentlemen having "
    "asked me to write down the whole particulars about Treasure Island, "
    "from the"
)

device = get_torch_device()
print(f"Using device: {device}")
tokenizer = Tokenizer.from_file("tokenizer.model")
model = OpenELM.from_pretrained(
    model_name="OpenELM-450M",
    device=device,
    dtype=torch.float16,
)

print("Generating text...")
input_ids = tokenizer([PROMPT]).to(device)
tokens = input_ids[0].tolist()  # For decoding text later.

with torch.inference_mode():
    outputs = model.forward(input_ids, use_kv_cache=True)
    logits = outputs["logits"]
    output_id = outputs["logits"][0, -1].argmax().item()
    cache = outputs["past_key_values"]
    tokens.append(output_id)

    for i in range(1000):
        outputs = model.forward(
            input_ids=torch.tensor([[output_id]], device=device),
            past_key_values=cache,
            use_kv_cache=True,
        )
        logits = outputs["logits"]

        output_id = outputs["logits"][0, -1].argmax().item()
        cache = outputs["past_key_values"]

        tokens.append(output_id)
        if i % 5 == 0:
            print(f"'{tokenizer.decode(tokens)}'")
