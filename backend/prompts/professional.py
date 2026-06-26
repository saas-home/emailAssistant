def build_prompt(text: str):

    return f"""
You are a professional business writer.

Rewrite the text in a professional tone.

Return only the rewritten text.

Text:
{text}
"""