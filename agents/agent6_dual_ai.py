import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Tuple
from utils.logger import get_logger
from utils.llm_clients import OpenAIClientWrapper, GeminiClientWrapper
from config import DEBATE_ROUNDS
log = get_logger("Agent6")

@dataclass
class DebateOutput:
    openai_view: str
    gemini_view: str
    consensus_summary: str
    consensus_action: str
    consensus_confidence: float

class DualAIDiscussionAgent:
    def __init__(self):
        self.openai = OpenAIClientWrapper()
        self.gemini = GeminiClientWrapper()

    def _analysis_prompt(self, data):
        return (
            "You are a crypto trading expert. Analyze this BTC/USDT market snapshot JSON and return:\n"
            "- a directional view (BUY/SELL/HOLD)\n"
            "- a brief rationale (2-3 bullets)\n"
            "- a confidence score 0..1\n"
            f"INPUT_JSON: {json.dumps(data)}"
        )

    def _cross_ex_prompt(self, prev_self, other_last):
        return (
            "Short debate round:\n"
            f"- Your previous view: {prev_self}\n"
            f"- Opponent's view: {other_last}\n"
            "Revise or defend your stance in 2 sentences max."
        )

    def _parse_action_conf(self, text):
        t = text.lower()
        action = "HOLD"
        if "buy" in t and "sell" not in t:
            action = "BUY"
        elif "sell" in t and "buy" not in t:
            action = "SELL"
        import re
        m = re.search(r"(confidence|score)[^0-9]*([01](?:\.\d+)?)", t)
        conf = float(m.group(2)) if m else 0.5
        return action, max(0.0, min(1.0, conf))

    def run(self, snapshot):
        prompt = self._analysis_prompt(snapshot)
        oa_msg = self.openai.analyze(prompt)
        gm_msg = self.gemini.analyze(prompt)
        oa_last, gm_last = oa_msg, gm_msg
        for _ in range(max(0, DEBATE_ROUNDS)):
            oa_last = self.openai.analyze(self._cross_ex_prompt(oa_last, gm_last))
            gm_last = self.gemini.analyze(self._cross_ex_prompt(gm_last, oa_last))
        oa_act, oa_conf = self._parse_action_conf(oa_last)
        gm_act, gm_conf = self._parse_action_conf(gm_last)
        if oa_act == gm_act:
            action = oa_act
            conf = (oa_conf + gm_conf) / 2.0
            summary = f"Consensus: {action} (OpenAI {oa_conf:.2f}, Gemini {gm_conf:.2f})."
        else:
            action = "HOLD"
            conf = (oa_conf + gm_conf) / 4.0
            summary = f"Disagreement (OpenAI {oa_act} {oa_conf:.2f} vs Gemini {gm_act} {gm_conf:.2f}); defaulting to HOLD."
        out = DebateOutput(openai_view=oa_last, gemini_view=gm_last, consensus_summary=summary, consensus_action=action, consensus_confidence=conf)
        log.info("Agent6 output ready.")
        return out
