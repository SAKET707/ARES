# config/settings.py

import os
from dotenv import load_dotenv

# Load .env once, globally
load_dotenv()

# -------------------------------------------------------------------
# API KEYS
# -------------------------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set in environment")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set in environment")

# -------------------------------------------------------------------
# LLM CONFIG
# -------------------------------------------------------------------

# Used ONLY for:
# - intent classification (Agent A)
# - explanation of tool outputs (Agent B)
LLM_PROVIDER = "groq"
LLM_MODEL = "llama-3.3-70b-versatile"

LLM_TEMPERATURE = 0.0   # deterministic
LLM_MAX_TOKENS = 2500

# -------------------------------------------------------------------
# REPO FETCH LIMITS (SAFETY)
# -------------------------------------------------------------------

# Max file size (in KB) that can be fetched
MAX_FILE_SIZE_KB = 500

# Max number of files shown in tree (top-level only)
MAX_TREE_ENTRIES = 200

# -------------------------------------------------------------------
# CACHE TOGGLES
# -------------------------------------------------------------------

ENABLE_SESSION_CACHE = True
ENABLE_FILE_CACHE = True

# FAISS is OPTIONAL and OFF by default
ENABLE_VECTORSTORE = False

# -------------------------------------------------------------------
# UI / BEHAVIOR FLAGS
# -------------------------------------------------------------------

# If True, Agent A must ask clarification on ANY ambiguity
STRICT_INTENT_MODE = True
