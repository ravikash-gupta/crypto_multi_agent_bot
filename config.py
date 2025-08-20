import os
from dotenv import load_dotenv
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
BINANCE_USE_TESTNET = os.getenv("BINANCE_USE_TESTNET", "true").lower() == "true"

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CRYPTOQUANT_API_KEY = os.getenv("CRYPTOQUANT_API_KEY", "")

AI_META_USE_LLM = os.getenv("AI_META_USE_LLM", "false").lower() == "true"
AI_META_MODEL = os.getenv("AI_META_MODEL", "gpt-4o-mini")
AI_META_MODEL_PATH = os.getenv("AI_META_MODEL_PATH", "training/meta_model.pkl")

ENABLE_DUAL_AI = os.getenv("ENABLE_DUAL_AI", "false").lower() == "true"
DEBATE_ROUNDS = int(os.getenv("DEBATE_ROUNDS", "2"))

MAX_RISK_PER_TRADE = float(os.getenv("MAX_RISK_PER_TRADE", "0.01"))
POSITION_SIZING_EQUITY = float(os.getenv("POSITION_SIZING_EQUITY", "1000"))
CONFIDENCE_TO_EXECUTE = float(os.getenv("CONFIDENCE_TO_EXECUTE", "0.75"))
