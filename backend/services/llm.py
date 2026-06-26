import requests
from backend.config import OLLAMA_URL, OLLAMA_MODEL

MODEL = OLLAMA_MODEL

def generate(prompt : str):
    payload = {
        "model" : MODEL,
        "prompt" : prompt,
        "stream" : False
    }

    response = requests.post(
        OLLAMA_URL,
        json = payload
    )
    data = response.json()

    return data["response"]