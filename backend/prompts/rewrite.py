def build_prompt(text: str):

    return f"""
You are an expert writer.

Rewrite the text while preserving meaning.

Return only the rewritten text in proper format.

Text:
{text}
"""