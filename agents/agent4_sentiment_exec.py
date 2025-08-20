import math
from dataclasses import dataclass
from textblob import TextBlob
import tweepy
from utils.logger import get_logger
from utils.binance_client import place_order, get_client
from binance.enums import SIDE_BUY, SIDE_SELL
from config import TWITTER_BEARER_TOKEN, CONFIDENCE_TO_EXECUTE, POSITION_SIZING_EQUITY, MAX_RISK_PER_TRADE

log = get_logger("Agent4")

@dataclass
class FinalTradeOutput:
    stablecoin_netflow_24h: float
    btc_netflow_24h: float
    stablecoin_netflow_7d: float
    btc_netflow_7d: float
    market_sentiment_signal: int
    technical_analysis_signal: float
    key_levels: dict
    trade_confidence_score: float
    recommended_action: str
    executed: bool
    order_response: dict
    entry_price: float
    stop_loss: float
    take_profit: float
    social_sentiment: float

class SentimentAndExecutionAgent:
    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol

    def _twitter_sentiment(self, query="(Bitcoin OR $BTC) lang:en -is:retweet", max_tweets=50):
        if not TWITTER_BEARER_TOKEN:
            log.warning("TWITTER_BEARER_TOKEN not set; social sentiment = 0")
            return 0.0
        client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
        tweets = client.search_recent_tweets(query=query, max_results=min(max_tweets,100))
        if not tweets.data:
            return 0.0
        scores = []
        for t in tweets.data:
            scores.append(TextBlob(t.text).sentiment.polarity)
        return float(sum(scores)/len(scores)) if scores else 0.0

    def _position_size(self, price, stop):
        risk_per_unit = abs(price - stop)
        if risk_per_unit == 0:
            return 0.0
        qty = (POSITION_SIZING_EQUITY * MAX_RISK_PER_TRADE) / risk_per_unit
        return math.floor(qty*10000)/10000

    def run(self, agent3_out):
        social = self._twitter_sentiment()
        execute = agent3_out.trade_confidence_score >= CONFIDENCE_TO_EXECUTE and abs(social) < 0.4
        levels4 = agent3_out.key_levels.get("4h",{})
        pivot = levels4.get("pivot")
        s1, r1 = levels4.get("S1"), levels4.get("R1")
        client = get_client()
        ticker = client.get_symbol_ticker(symbol=self.symbol)
        price = float(ticker["price"])
        executed = False; order_response = {}; entry_price = price; stop_loss = 0.0; take_profit = 0.0
        if execute and agent3_out.recommended_action in ("BUY","SELL"):
            if agent3_out.recommended_action == "BUY":
                stop_loss = s1 if s1 else price*0.98
                take_profit = r1 if r1 else price*1.02
                qty = self._position_size(price, stop_loss)
                if qty >= 0.0001:
                    order_response = place_order(self.symbol, SIDE_BUY, qty, limit=False)
                    executed = True
            else:
                stop_loss = r1 if r1 else price*1.02
                take_profit = s1 if s1 else price*0.98
                qty = self._position_size(stop_loss, price)
                if qty >= 0.0001:
                    order_response = place_order(self.symbol, SIDE_SELL, qty, limit=False)
                    executed = True
        out = FinalTradeOutput(
            stablecoin_netflow_24h=agent3_out.stablecoin_netflow_24h,
            btc_netflow_24h=agent3_out.btc_netflow_24h,
            stablecoin_netflow_7d=agent3_out.stablecoin_netflow_7d,
            btc_netflow_7d=agent3_out.btc_netflow_7d,
            market_sentiment_signal=agent3_out.market_sentiment_signal,
            technical_analysis_signal=agent3_out.technical_analysis_signal,
            key_levels=agent3_out.key_levels,
            trade_confidence_score=agent3_out.trade_confidence_score,
            recommended_action=agent3_out.recommended_action,
            executed=executed,
            order_response=order_response,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            social_sentiment=social,
        )
        log.info("Agent4 output ready.")
        return out
