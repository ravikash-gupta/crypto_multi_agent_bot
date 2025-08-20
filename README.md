# ZEP - AI Crypto Debate Framework

ZEP is an AI-powered research & debate tool for analyzing crypto market flows using
on-chain, technical, and narrative data. It integrates CryptoQuant API, OpenAI GPT,
and Google Gemini agents that debate and summarize insights.

## 🚀 Features
- Fetch real-time **on-chain stablecoin flows**
- Compute **technical indicators** (RSI, MACD, SMA, Pivot Points)
- Run debates between **multiple AI agents**
- Generate a **final market summary**

```
    
zep-project/
│── main.py                  # Entry point, runs prediction + debate
│── requirements.txt         # Python dependencies
│── README.md                # Documentation
│
├── config/
│   └── settings.py          # API keys, model configs, thresholds
│
├── data/
│   └── market_data.py       # Functions to fetch/clean aggregated data
│
├── indicators/
│   └── technicals.py        # RSI, MACD, Bollinger, etc.
│
├── models/
│   ├── openai_model.py      # OpenAI-based reasoning
│   ├── gemini_model.py      # Gemini-based reasoning
│   └── debate.py            # AI-vs-AI debate mechanism
│
├── data_sources/
│   └── cryptoquant_api.py   # CryptoQuant API wrapper
│   └── glassnode_api.py     # (optional, future)
│   └── ccxt_api.py          # (optional, for exchange price feeds)
│
└── utils/
    └── logger.py            # Logging & debugging


```
