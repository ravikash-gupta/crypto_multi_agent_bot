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
    
zep/
│── README.md
│── requirements.txt
│── config.py
│── main.py
│
├── indicators/
│   ├── __init__.py
│   ├── onchain_data.py
│   ├── technicals.py
│
├── ai_agents/
│   ├── __init__.py
│   ├── openai_agent.py
│   ├── gemini_agent.py
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── cryptoquant_api.py
│
└── discussions/
    ├── __init__.py
    ├── debate_manager.py

```
