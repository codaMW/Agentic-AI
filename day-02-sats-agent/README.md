# Sats Agent 🧌 a live Bitcoin assistant for Malawi

A conversational AI agent that converts between satoshis, Bitcoin, USD, and
Malawi Kwacha (MWK) using **live** Bitcoin prices.

## What it does
- Fetches the current BTC price from the mempool.space API
- Chains tools automatically: gets the price, then converts
- Remembers the conversation (multi-turn)
- Survives bad user input and model misbehavior without crashing

## Built with
- Python + Pydantic AI (v2)
- Groq (Llama 3.3 70B) for inference free tier
- httpx for live price data

## Run it
​```bash
export GROQ_API_KEY="your_key"
uv run main.py
​```

## What I learned
- The LLM tool-calling loop: the model decides which tools to call
- Zero-argument tools are fragile across models, give tools a parameter
- Treat both user input AND model output as untrusted; validate at every boundary
