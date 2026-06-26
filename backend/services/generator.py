from backend.services.llm import generate
from backend.prompts.registry import PROMPTS

def generate_suggestion(action : str , text : str):
    if not text.strip():
        raise ValueError("Text cannot be empty :)")
    if action not in PROMPTS:
        raise ValueError("Action not available ;(")
    prompt_builder = PROMPTS[action]
    prompt = prompt_builder(text)
    results = generate(prompt)
    return [results]