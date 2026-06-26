from .grammar import build_prompt as grammar_prompt
from .rewrite import build_prompt as rewrite_prompt
from .professional import build_prompt as professional_prompt

PROMPTS = {
    "grammar" : grammar_prompt,
    "rewrite" : rewrite_prompt,
    "professional" : professional_prompt
}