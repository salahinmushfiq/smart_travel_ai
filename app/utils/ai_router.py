from dotenv import load_dotenv
import time
from huggingface_hub import InferenceClient
import os
import requests

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")
print("HF TOKEN LOADED:", bool(HF_TOKEN))
client = InferenceClient(provider="hf-inference",token=HF_TOKEN)

MODEL = "google/flan-t5-base"


def generate_answer(prompt: str, retries: int = 3):

    for attempt in range(retries):
        try:
            response = client.text_generation(
                model=MODEL,
                prompt=prompt,
                max_new_tokens=200,
                temperature=0.5,
                return_full_text=False,
            )

            if response:
                return response.strip()

        except Exception as e:
            print(f"[HF ERROR attempt={attempt+1}]", repr(e))
            time.sleep(2)

    return "AI temporarily unavailable."