import json
from utils.logger import get_logger
from agents.agent1_onchain import OnChainExchangeFlowAnalyst
from agents.agent2_ta import TechnicalAnalysisSpecialist
from agents.agent3_confluence import MultiTimeframeConfluenceEngine
from agents.agent5_ai_meta import AIMetaAgent
from agents.agent4_sentiment_exec import SentimentAndExecutionAgent
from config import ENABLE_DUAL_AI
log = get_logger("MAIN")

def main():
    agent1 = OnChainExchangeFlowAnalyst()
    on_chain = agent1.run()
    ta = TechnicalAnalysisSpecialist(symbol="BTCUSDT")
    agent2_out = ta.run(on_chain)
    agent3 = MultiTimeframeConfluenceEngine()
    trade_setup = agent3.run(agent2_out)
    agent5 = AIMetaAgent()
    fused = agent5.run({
        "stablecoin_netflow_24h": trade_setup.stablecoin_netflow_24h,
        "btc_netflow_24h": trade_setup.btc_netflow_24h,
        "stablecoin_netflow_7d": trade_setup.stablecoin_netflow_7d,
        "btc_netflow_7d": trade_setup.btc_netflow_7d,
        "market_sentiment_signal": trade_setup.market_sentiment_signal,
        "technical_analysis_signal": trade_setup.technical_analysis_signal,
        "key_levels": trade_setup.key_levels,
        "trade_confidence_score": trade_setup.trade_confidence_score,
        "recommended_action": trade_setup.recommended_action,
        "social_sentiment": 0.0,
    })
    payload = fused.payload
    if ENABLE_DUAL_AI:
        from agents.agent6_dual_ai import DualAIDiscussionAgent
        debate = DualAIDiscussionAgent()
        debate_out = debate.run({
            "on_chain": on_chain.raw_snapshot if hasattr(on_chain,'raw_snapshot') else {},
            "ta_summary": {"technical_analysis_signal": agent2_out.technical_analysis_signal, "key_levels": agent2_out.key_levels},
            "trade_setup": {"trade_confidence_score": trade_setup.trade_confidence_score, "recommended_action": trade_setup.recommended_action}
        })
        if debate_out.consensus_action != "HOLD" and debate_out.consensus_confidence >= 0.6:
            trade_setup.recommended_action = debate_out.consensus_action
            trade_setup.trade_confidence_score = max(trade_setup.trade_confidence_score, debate_out.consensus_confidence)
    agent4 = SentimentAndExecutionAgent(symbol="BTCUSDT")
    final_trade = agent4.run(trade_setup)
    final_json = json.loads(json.dumps(final_trade, default=lambda o: o.__dict__))
    final_json["ai_meta"] = {"ai_meta_score": payload.get("ai_meta_score"), "ai_meta_rationale": payload.get("ai_meta_rationale")}
    if ENABLE_DUAL_AI and 'debate_out' in locals():
        final_json["dual_ai"] = {"consensus_action": debate_out.consensus_action, "consensus_confidence": debate_out.consensus_confidence, "consensus_summary": debate_out.consensus_summary, "openai_view": debate_out.openai_view, "gemini_view": debate_out.gemini_view}
    print(json.dumps(final_json, indent=2))

if __name__ == '__main__':
    main()
