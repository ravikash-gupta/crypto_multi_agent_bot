import os, requests
from utils.logger import get_logger
log = get_logger("cryptoquant")
API_KEY = os.getenv("CRYPTOQUANT_API_KEY", "")
BASE_URL = "https://api.cryptoquant.com/v1"
ENDPOINTS = {
    "btc_exchange_inflow": "/bitcoin/exchange-flows/inflow",
    "btc_exchange_outflow": "/bitcoin/exchange-flows/outflow",
    "btc_flow_indicator_whale_ratio": "/bitcoin/flow-indicator/whale-ratio",
    "btc_mpi": "/bitcoin/market-indicator/mpi",
    "btc_mvrv": "/bitcoin/market-indicator/mvrv",
    "btc_network_nvt": "/bitcoin/network-indicator/nvt",
    "btc_miner_outflow": "/bitcoin/miner-flows/outflow",
    "btc_inter_entity_flows": "/bitcoin/inter-entity-flows",
    "btc_fund_data": "/bitcoin/fund-data",
    "btc_market_data": "/bitcoin/market-data",
    "btc_network_data": "/bitcoin/network-data",
    "btc_mempool": "/bitcoin/mempool",
    "btc_lightning": "/bitcoin/lightning-network",
    "stablecoin_exchange_flows": "/stablecoin/exchange-flows",
    "stablecoin_market_data": "/stablecoin/market-data",
    "stablecoin_network_data": "/stablecoin/network-data",
}

def _get(endpoint, params=None):
    if not API_KEY:
        log.warning("CRYPTOQUANT_API_KEY not set; returning stub for %s", endpoint)
        return {"stub": True, "endpoint": endpoint}
    url = BASE_URL + endpoint
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        else:
            log.error("CryptoQuant API error %s: %s", r.status_code, r.text)
            return {"error": r.text, "status_code": r.status_code}
    except Exception as e:
        log.exception("Exception fetching CryptoQuant: %s", e)
        return {"error": str(e)}

def fetch_all(selected=None):
    keys = list(ENDPOINTS.keys()) if selected is None else selected
    out = {}
    for k in keys:
        ep = ENDPOINTS.get(k)
        if not ep:
            out[k] = {"error": "unknown key"}
            continue
        out[k] = _get(ep)
    return out
