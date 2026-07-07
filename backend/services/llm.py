import requests
from backend.config import OLLAMA_URL, OLLAMA_MODEL, LLM_URL, LLM_MODEL, LLM_KEY

def generate(prompt: str) -> str:
    if LLM_KEY:
        # OpenAI-compatible server (Coder-9B, etc.)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_KEY}",
        }
        payload = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post(LLM_URL, headers=headers, json=payload)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        # Ollama local fallback
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        }
        response = requests.post(OLLAMA_URL, json=payload)
        data = response.json()
        return data["response"]