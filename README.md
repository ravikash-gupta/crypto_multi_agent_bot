# crypto_multi_agent_bot

cp .env.example .env and fill your keys.

Create a Python virtual environment and pip install -r requirements.txt.

Test the pipeline on Binance testnet (set BINANCE_USE_TESTNET=true) and use test API keys if available.

Wire the real OpenAI / Gemini API calls in utils/llm_clients.py if you want the debate to use real LLM outputs. (The wrappers already attempt to import and call; you may need to configure credentials per provider instructions.)

If you want fully deterministic on-chain features, sign up for CryptoQuant, set CRYPTOQUANT_API_KEY in .env, and the agent will fetch real endpoints.

Final notes & next steps I can do immediately for you

I can try to package this project into a single ZIP and provide a download link (I attempted earlier and hit an error while zipping automatically — I can retry now if you want).

I can wire the exact OpenAI & Gemini API calls inside utils/llm_clients.py using your preferred call patterns (I have the stub code; I can replace it with robust prompts and parsing). If you want that I’ll add safe parsing and JSON output enforcement so the debate agent can reliably extract action/confidence.

I can add a backtester that uses historical CryptoQuant + Binance klines to auto-label outcomes and create training data for the offline meta-agent — useful for production.

Tell me which of these (package into ZIP, wire LLM calls, backtester, or something else) you want me to do next and I’ll proceed. If you want the ZIP now, say “make zip” and I’ll produce and give you a download link.

    '''
    
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


    '''
