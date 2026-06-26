def build_prompt(text: str):

    return f"""
You are a expert writing editor.

Correct grammar, spelling, and punctuation.

Return only the corrected text with proper grammar.

Text:
{text}
"""