import httpx
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel


# ==========================================
# 1. STRUCTURAL DATA MODELS (PYDANTIC)
# ==========================================

class TransactionSummary(BaseModel):
    """High-level transaction data filtered from raw mempool queues."""
    txid: str
    fee: int
    vsize: int
    value_sats: int = Field(..., alias="value")
    estimated_usd: float


class ForensicAddressReport(BaseModel):
    """Structured analytical telemetry payload regarding a suspected wallet address."""
    address: str
    total_tx_count: int
    known_associated_txids: list[str]
    velocity_patterns: str
    risk_profile: str


# ==========================================
# 2. DATA SERVICE LAYER (BITCOIN INTELLIGENCE)
# ==========================================

class BitcoinIntelligenceUnit:
    """Manages secure REST API interactions with underlying Bitcoin ledger nodes."""
    
    BTC_SPOT_PRICE: float = 90000.0  # Dynamic benchmark variable for value tracking
    WHALE_THRESHOLD_USD: float = 100000.0

    def get_recent_mempool_txs(self) -> list[TransactionSummary]:
        """Fetches the 10 most recent transactions entering the mempool pipeline."""
        try:
            response = httpx.get("https://blockstream.info/api/mempool/recent", timeout=10.0)
            response.raise_for_status()
            raw_data = response.json()

            summaries = []
            for tx in raw_data[:10]:
                sats = tx.get("value", 0)
                btc_value = sats / 100_000_000.0
                usd_value = btc_value * self.BTC_SPOT_PRICE
                
                summaries.append(TransactionSummary(
                    txid=tx["txid"],
                    fee=tx["fee"],
                    vsize=tx["vsize"],
                    value=sats,
                    estimated_usd=round(usd_value, 2)
                ))
            return summaries
        except Exception as e:
            print(f"[METRIC ERROR] Failed to fetch mempool updates: {e}")
            return []

    def perform_forensic_address_scan(self, suspect_address: str) -> ForensicAddressReport:
        """Queries on-chain transaction history arrays linked to an explicit UTXO scriptpubkey address."""
        try:
            # Query Esplora's address transaction ledger
            url = f"https://blockstream.info/api/address/{suspect_address}/txs"
            response = httpx.get(url, timeout=10.0)
            response.raise_for_status()
            tx_history = response.json()

            txids = [tx["txid"] for tx in tx_history]
            tx_count = len(txids)
            
            # Simple algorithmic profile classification based on velocity
            if tx_count > 15:
                velocity = "High-frequency operational entity. Micro-interval routing detected."
                risk = "ELEVATED - Structural similarities to tumbling mixers or illicit structural laundering."
            else:
                velocity = "Low-frequency high-volume cold store or whale nesting vault."
                risk = "MONITOR - Strategic whale reserve aggregation point."

            return ForensicAddressReport(
                address=suspect_address,
                total_tx_count=tx_count,
                known_associated_txids=txids[:5],  # High-signal telemetry subset
                velocity_patterns=velocity,
                risk_profile=risk
            )
        except Exception as e:
            print(f"[FORENSIC ERROR] Target address query aborted: {e}")
            return ForensicAddressReport(
                address=suspect_address,
                total_tx_count=0,
                known_associated_txids=[],
                velocity_patterns="Unknown - API Connection Dropped",
                risk_profile="UNVERIFIED"
            )


# ==========================================
# 3. AGENT INITIALIZATION & INSTRUCTIONS
# ==========================================

# Direct instantiation of Llama 3.3 70B via Groq
# Note: Ensure export GROQ_API_KEY="your-key" is run in your bash session
groq_model = GroqModel("llama-3.3-70b-versatile")

agent = Agent(
    groq_model,
    instructions=(
        "You are the Lead Financial Forensic Investigator and On-Chain Intelligence Architect "
        "assigned to the Joint Crypto-Crimes Taskforce (advising the IMF, CIA, FBI, and World Bank).\n\n"
        
        "### Operational Persona and Standards:\n"
        "- **Tone:** Analytical, definitive, empirical, objective, and authoritative. Do not use colloquial text.\n"
        "- **Reporting Framework:** You must deliver intelligence summaries utilizing executive institutional formatting. "
        "Use explicit sections: Executive Summary, Macro Financial Threat Matrix, On-Chain Forensic Telemetry, "
        "and Actionable Statutory Directives (Interpol/FinCEN cross-references).\n\n"
        
        "### Investigation Mandate:\n"
        "1. Identify Whale Transactions. A whale transaction is defined strictly as values >= $100,000 USD.\n"
        "2. When auditing addresses, flag any suspicious characteristics: high transaction velocities, cyclic transfers, "
        "dusting indicators, fee manipulation, or structural evasion strategies indicating unlicensed money services.\n"
        "3. Provide strategic macro-advisory observations matching strict monetary compliance standards (AML/CFT/FATF)."
    ),
    deps_type=BitcoinIntelligenceUnit,
)


# ==========================================
# 4. AGENT TOOLS DEFINITION
# ==========================================

@agent.tool
def get_mempool_telemetry(ctx: RunContext[BitcoinIntelligenceUnit]) -> list[TransactionSummary]:
    """Retrieves real-time on-chain metrics for the top 10 recent transactions inside the Bitcoin mempool queue.
    
    Use this tool to capture baseline hash strings, sizes, fee metrics, and valuation tracking estimates.
    """
    print("[CRITICAL INFO] Polling active node mempool queues...")
    return ctx.deps.get_mempool_telemetry_data()


@agent.tool
def analyze_wallet_forensics(ctx: RunContext[BitcoinIntelligenceUnit], address: str) -> ForensicAddressReport:
    """Performs deep-ledger forensic auditing and clustering analysis on a specific Bitcoin address string.
    
    Args:
        address: The alphanumeric valid public Bitcoin address script identifier.
    """
    print(f"[INVESTIGATION STAGE 2] Initiating full ledger sweep on target: {address}")
    return ctx.deps.perform_forensic_address_scan(address)


# Mapping the actual processing routine for the mock function
# This bridges the internal tracking logic to your structured object dependencies
BitcoinIntelligenceUnit.get_mempool_telemetry_data = BitcoinIntelligenceUnit.get_recent_mempool_txs


# ==========================================
# 5. INTERACTIVE INVESTIGATION REPL
# ==========================================

if __name__ == "__main__":
    intelligence_unit = BitcoinIntelligenceUnit()
    session_history = None

    print("-" * 80)
    print("FINANCIAL CRIMES ENFORCEMENT & ON-CHAIN FORENSICS INTELLIGENCE HUB INITIALIZED")
    print("System Status: Operational | Targets: Bitcoin Mainnet Ledger Queue")
    print("-" * 80)

    while True:
        try:
            prompt = input("\ninvestigator@intelligence-ops:~$ ")
            if prompt.lower() in ["exit", "quit"]:
                break
            if not prompt.strip():
                continue

            # Run synchronous execution loop with dependencies injected
            result = agent.run_sync(
                prompt,
                message_history=session_history,
                deps=intelligence_unit
            )
            
            print(f"\n[CLASSIFIED REPORT]\n{result.output}")
            session_history = result.all_messages()

        except Exception as e:
            print(f"\n[SYSTEM HALT] Execution anomaly: {type(e).__name__} - {e}")