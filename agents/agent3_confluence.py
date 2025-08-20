from dataclasses import dataclass, asdict
from utils.logger import get_logger
log = get_logger("Agent3")

@dataclass
class Agent3Output:
    stablecoin_netflow_24h: float
    btc_netflow_24h: float
    stablecoin_netflow_7d: float
    btc_netflow_7d: float
    market_sentiment_signal: int
    technical_analysis_signal: float
    key_levels: dict
    trade_confidence_score: float
    recommended_action: str

class MultiTimeframeConfluenceEngine:
    def __init__(self):
        pass

    def run(self, agent2_out):
        sentiment = agent2_out.market_sentiment_signal
        ta = agent2_out.technical_analysis_signal
        aligned = (sentiment == 1 and ta > 0) or (sentiment == -1 and ta < 0)
        base_conf = 0.6 if aligned else 0.4
        conf = base_conf + 0.4 * abs(ta)
        conf = max(0.0,min(1.0,conf))
        if conf < 0.55:
            action = "HOLD"
        else:
            if ta > 0 and sentiment >= 0:
                action = "BUY"
            elif ta < 0 and sentiment <= 0:
                action = "SELL"
            else:
                action = "HOLD"
        out = Agent3Output(
            stablecoin_netflow_24h=agent2_out.stablecoin_netflow_24h,
            btc_netflow_24h=agent2_out.btc_netflow_24h,
            stablecoin_netflow_7d=agent2_out.stablecoin_netflow_7d,
            btc_netflow_7d=agent2_out.btc_netflow_7d,
            market_sentiment_signal=agent2_out.market_sentiment_signal,
            technical_analysis_signal=agent2_out.technical_analysis_signal,
            key_levels=agent2_out.key_levels,
            trade_confidence_score=conf,
            recommended_action=action,
        )
        log.info("Agent3 output ready.")
        return out
