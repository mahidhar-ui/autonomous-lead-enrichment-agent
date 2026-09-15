import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")

LLM_BASE_URL = os.getenv(
    "LLM_BASE_URL",
    "https://api.groq.com/openai/v1"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "openai/gpt-oss-20b"
)

REQUEST_TIMEOUT_MS = int(
    os.getenv("REQUEST_TIMEOUT_MS", "30000")
)

MAX_PAGES_PER_DOMAIN = int(
    os.getenv("MAX_PAGES_PER_DOMAIN", "8")
)

MAX_CHARS_PER_PAGE = int(
    os.getenv("MAX_CHARS_PER_PAGE", "7000")
)

MAX_CONTEXT_CHARS = int(
    os.getenv("MAX_CONTEXT_CHARS", "28000")
)

if not LLM_API_KEY:
    raise RuntimeError(
        "Missing GROQ_API_KEY or OPENAI_API_KEY in .env"
    )