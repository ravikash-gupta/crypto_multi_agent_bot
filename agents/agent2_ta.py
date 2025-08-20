import pandas as pd, numpy as np
from dataclasses import dataclass, asdict
from binance.client import Client
from ta.momentum import RSIIndicator
from ta.volume import VolumeWeightedAveragePrice
from utils.logger import get_logger
from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_USE_TESTNET

log = get_logger("Agent2")

@dataclass
class Agent2Output:
    stablecoin_netflow_24h: float
    btc_netflow_24h: float
    stablecoin_netflow_7d: float
    btc_netflow_7d: float
    market_sentiment_signal: int
    technical_analysis_signal: float
    key_levels: dict

class TechnicalAnalysisSpecialist:
    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=BINANCE_USE_TESTNET)

    def _get_klines(self, interval, limit=500):
        kl = self.client.get_klines(symbol=self.symbol, interval=interval, limit=limit)
        cols = ["open_time","open","high","low","close","volume","close_time","qav","num_trades","taker_base","taker_quote","ignore"]
        df = pd.DataFrame(kl, columns=cols)
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        return df

    def _pivot_points(self, df):
        last = df.iloc[-2]
        high, low, close = last["high"], last["low"], last["close"]
        pivot = (high+low+close)/3
        r1 = 2*pivot - low
        s1 = 2*pivot - high
        r2 = pivot + (high-low)
        s2 = pivot - (high-low)
        r3 = high + 2*(pivot-low)
        s3 = low - 2*(high-pivot)
        return {"pivot":pivot,"R1":r1,"S1":s1,"R2":r2,"S2":s2,"R3":r3,"S3":s3}

    def _ta_score(self, df):
        rsi = RSIIndicator(close=df["close"], window=14).rsi().iloc[-1]
        vwap = VolumeWeightedAveragePrice(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"], window=24).vwap().iloc[-1]
        price = df["close"].iloc[-1]
        ma50 = df["close"].rolling(50).mean().iloc[-1]
        ma200 = df["close"].rolling(200).mean().iloc[-1]
        score = 0.0
        if rsi < 30: score += 0.25
        elif rsi > 70: score -= 0.25
        if price > vwap: score += 0.25
        else: score -= 0.1
        if ma50 > ma200: score += 0.3
        else: score -= 0.3
        if price > ma50: score += 0.2
        else: score -= 0.2
        return float(max(-1.0,min(1.0,score)))

    def run(self, agent1_out):
        df_1h = self._get_klines(Client.KLINE_INTERVAL_1HOUR)
        df_4h = self._get_klines(Client.KLINE_INTERVAL_4HOUR)
        score_1h = self._ta_score(df_1h)
        score_4h = self._ta_score(df_4h)
        ta_score = float(np.clip((score_1h+score_4h)/2.0,-1.0,1.0))
        key_levels = {"1h": self._pivot_points(df_1h), "4h": self._pivot_points(df_4h)}
        out = Agent2Output(
            stablecoin_netflow_24h=agent1_out.stablecoin_netflow_24h,
            btc_netflow_24h=agent1_out.btc_netflow_24h,
            stablecoin_netflow_7d=agent1_out.stablecoin_netflow_7d,
            btc_netflow_7d=agent1_out.btc_netflow_7d,
            market_sentiment_signal=agent1_out.market_sentiment_signal,
            technical_analysis_signal=ta_score,
            key_levels=key_levels,
        )
        log.info("Agent2 output ready.")
        return out
