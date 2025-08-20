import os, csv
from typing import Dict, Any
from utils.logger import get_logger
log = get_logger("dataset")

DATA_PATH = os.getenv("META_DATASET_PATH", "training/meta_dataset.csv")
FEATURE_COLUMNS = [
    "stablecoin_netflow_24h","btc_netflow_24h","stablecoin_netflow_7d","btc_netflow_7d",
    "market_sentiment_signal","technical_analysis_signal","trade_confidence_score","social_sentiment",
]
TARGET_COLUMN = "profitable_outcome"

def ensure_header():
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(FEATURE_COLUMNS + [TARGET_COLUMN])

def log_example(features: Dict[str, Any], outcome: int):
    ensure_header()
    row = [features.get(c, 0.0) for c in FEATURE_COLUMNS] + [int(outcome)]
    with open(DATA_PATH, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    log.info("Logged dataset example.")

def load_dataset():
    ensure_header()
    with open(DATA_PATH, "r", encoding='utf-8') as f:
        rows = list(csv.reader(f))
    if len(rows) <= 1:
        return []
    return rows
