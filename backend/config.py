from dotenv import load_dotenv
import os

# Load .env from the same directory as this config file
config_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(config_dir, ".env"))
load_dotenv(os.path.join(config_dir, ".env.server"))  # load server-specific credentials (API key), overrides .env

# Ollama (local) config
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")

# Alternative server config (OpenAI-compatible API)
LLM_URL  = os.getenv("LLM_URL", "https://llm.saashome.net/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "Coder-9B")
LLM_KEY  = os.getenv("LLM_KEY")