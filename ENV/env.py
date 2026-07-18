import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
LLM_TOKEN = os.getenv("LLM_TOKEN", "")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
MODEL_PATH = os.getenv("MODEL_PATH", "multilingual-e5-large")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nutrition_bot.db")
