from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_USE_TESTNET
from utils.logger import get_logger
log = get_logger("binance")

def get_client():
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=BINANCE_USE_TESTNET)
    return client

def place_order(symbol: str, side: str, quantity: float, price=None, limit=False):
    client = get_client()
    if limit and price is not None:
        log.info(f"Placing LIMIT {side} {symbol} qty={quantity} price={price}")
        return client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=quantity, price=str(price))
    else:
        log.info(f"Placing MARKET {side} {symbol} qty={quantity}")
        return client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
