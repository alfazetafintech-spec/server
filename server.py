from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_ID = "Sambit-Mishra/vkm-v0"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
    device_map="cpu",
    torch_dtype=torch.float32,
)

app = FastAPI()

class Request(BaseModel):
    system: str
    prompt: str
    max_tokens: int = 1500
    temperature: float = 0.7

@app.post("/generate")
def generate(req: Request):
    text = f"<system>\n{req.system}\n</system>\n<user>\n{req.prompt}\n</user>"
    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
        )

    result = tokenizer.decode(output[0], skip_special_tokens=True)
    return { "text": result }
