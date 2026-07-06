import asyncio
import httpx
from pydantic_ai import Agent
from pydantic_ai.exceptions import UnexpectedModelBehavior

SATS_PER_BTC = 100_000_000
USD_TO_MWK = 2000.0          # rough FX; live rate on Day 9

agent = Agent(
    "groq:llama-3.3-70b-versatile",
    instructions=(
        "You are a Bitcoin assistant for users in Malawi. "
        "For ANY conversion between sats, BTC, USD, or Malawi Kwacha (MWK), you "
        "MUST call the tools — never guess numbers. First call get_btc_price to "
        "get the live USD price, then convert. Report amounts with thousands "
        "separators. If the user sends a bare number with no currency, ask which "
        "conversion they want instead of calling a tool."
        ),
)

@agent.tool_plain
async def get_btc_price(currency: str = "USD") -> float:
    """Fetch the current live price of 1 Bitcoin.

    Args:
        currency: Fiat currency code, e.g. "USD" or "EUR". Defaults to "USD".
    """
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get("https://mempool.space/api/v1/prices")
        resp.raise_for_status()
        data = resp.json()
    code = currency.upper()
    if code not in data:
        code = "USD"                     # fall back if we don't have that currency
    return float(data[code])


@agent.tool_plain
def sats_to_mwk(sats: float, btc_price_usd: float) -> float:
    """Convert satoshis to Malawi Kwacha at the given BTC price.

    Args:
        sats: Number of satoshis to convert.
        btc_price_usd: Current price of 1 BTC in US dollars.
    """
    btc = sats / SATS_PER_BTC
    return btc * btc_price_usd * USD_TO_MWK

@agent.tool_plain
def mwk_to_sats(mwk: float, btc_price_usd: float) -> float:
    """Convert Malawi Kwacha to satoshis at the given BTC price.

    Args:
        mwk: Amount in Malawi Kwacha to convert.
        btc_price_usd: Current price of 1 BTC in US dollars.
    """
    usd = mwk / USD_TO_MWK
    return (usd / btc_price_usd) * SATS_PER_BTC


async def main():
    print("🧌 Sats Agent (Malawi). Ask me anything. Type 'quit' to exit.\n")
    history = None
    while True:
        user = input("you> ").strip()

        # NEW: clean ways to leave, and ignore empty input.
        if user.lower() in {"quit", "exit"}:
            print("Goodbye! 👋")
            break
        if not user:
            continue

        # NEW: one bad turn should never crash the program.
        # try/except is Python's version of matching on a Result.
        try:
            result = await agent.run(user, message_history=history)
            print(f"agent> {result.output}\n")
            history = result.all_messages()   # only keep history on success
        except UnexpectedModelBehavior as e:
            print(f"agent> (I got confused there — try rephrasing.) [{e}]\n")
        except httpx.HTTPError as e:
            print(f"agent> (Couldn't reach the price service: {e})\n")
        except Exception as e:
            # Catch-all so the loop survives anything unexpected.
            print(f"agent> (Unexpected error: {type(e).__name__}: {e})\n")


if __name__ == "__main__":
    asyncio.run(main())
