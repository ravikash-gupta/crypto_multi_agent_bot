import json
from dataclasses import dataclass
from typing import Dict, Any
import numpy as np, os
from utils.logger import get_logger
from config import AI_META_USE_LLM, AI_META_MODEL, AI_META_MODEL_PATH
log = get_logger("Agent5")
try:
    import joblib
    _meta_model = joblib.load(AI_META_MODEL_PATH) if os.path.exists(AI_META_MODEL_PATH) else None
except Exception:
    _meta_model = None

@dataclass
class Agent5Output:
    payload: Dict[str, Any]

class AIMetaAgent:
    def __init__(self):
        pass

    def _numeric_combiner(self, data):
        sentiment = float(data.get("market_sentiment_signal",0))
        ta = float(data.get("technical_analysis_signal",0.0))
        conf = float(data.get("trade_confidence_score",0.0))
        social = float(data.get("social_sentiment",0.0))
        w = np.array([0.35,0.4,0.2,-0.15])
        x = np.array([sentiment,ta,conf,social])
        z = float(np.tanh(np.dot(w,x)))
        meta_conf = (z+1)/2.0
        rationale = f"Numeric combiner fused sentiment={sentiment}, TA={ta}, base_conf={conf}, social={social} -> meta_conf={meta_conf:.3f}"
        data["ai_meta_score"] = meta_conf
        data["ai_meta_rationale"] = rationale
        if meta_conf < 0.5:
            data["recommended_action"] = "HOLD"
        return data

    def _offline_model_score(self, data):
        if _meta_model is None:
            return data
        feat_names = ["stablecoin_netflow_24h","btc_netflow_24h","stablecoin_netflow_7d","btc_netflow_7d","market_sentiment_signal","technical_analysis_signal","trade_confidence_score","social_sentiment"]
        x = np.array([[float(data.get(n,0.0)) for n in feat_names]],dtype=float)
        try:
            proba = float(_meta_model.predict_proba(x)[0,1])
        except Exception:
            proba = float(_meta_model.predict(x)[0])
        data["ai_meta_score"] = proba
        data["ai_meta_rationale"] = "Offline ML model score."
        if proba < 0.5:
            data["recommended_action"] = "HOLD"
        return data

    def _llm_reasoner(self, data):
        log.info("LLM mode requested but not wired in this scaffold; using numeric fallback.")
        return self._numeric_combiner(data)

    def run(self, downstream_payload):
        out = dict(downstream_payload)
        out = self._offline_model_score(out)
        if "ai_meta_score" not in out:
            if AI_META_USE_LLM:
                out = self._llm_reasoner(out)
            else:
                out = self._numeric_combiner(out)
        log.info("Agent5 output ready.")
        return Agent5Output(payload=out)
