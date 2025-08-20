from utils.logger import get_logger
from config import OPENAI_API_KEY, GEMINI_API_KEY, AI_META_MODEL
log = get_logger("llm")

class OpenAIClientWrapper:
    def __init__(self):
        if not OPENAI_API_KEY:
            log.warning("OPENAI_API_KEY not set; OpenAI unavailable.")
            self.client = None
        else:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=OPENAI_API_KEY)
            except Exception:
                self.client = None
                log.exception("Failed to import OpenAI client.")

    def analyze(self, prompt: str):
        if self.client is None:
            return "OpenAI stub: no key or client."
        try:
            resp = self.client.chat.completions.create(model=AI_META_MODEL, messages=[{"role":"user","content":prompt}], max_tokens=400)
            return resp.choices[0].message.content
        except Exception as e:
            log.exception("OpenAI call failed: %s", e)
            return f"OpenAI error: {e}"

class GeminiClientWrapper:
    def __init__(self):
        if not GEMINI_API_KEY:
            log.warning("GEMINI_API_KEY not set; Gemini unavailable.")
            self.client = None
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                self.client = genai
            except Exception:
                self.client = None
                log.exception("Failed to import Gemini client.")

    def analyze(self, prompt: str):
        if self.client is None:
            return "Gemini stub: no key or client."
        try:
            resp = self.client.generate_text(model="chat-bison", prompt=prompt)
            return resp.text if hasattr(resp, "text") else str(resp)
        except Exception as e:
            log.exception("Gemini call failed: %s", e)
            return f"Gemini error: {e}"
