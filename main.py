from utils.ibkr_connector import fetch_positions_from_ibkr
from utils.proxy_resolver import resolve_proxies_for_holdings

def main():
    print("🔌 Connecting to IBKR to fetch positions...")
    holdings = fetch_positions_from_ibkr()

    if not holdings:
        print("⚠️ No holdings found or IBKR connection failed.")
        return

    print(f"📦 Retrieved {len(holdings)} holdings. Resolving proxies via OpenAI...")
    proxies = resolve_proxies_for_holdings(holdings)

    print("\n🧠 Enriched Holdings with Proxies:")
    for orig, proxy in zip(holdings, proxies):
        print(f"- {orig['symbol']} → {proxy['symbol']} ({proxy['secType']} on {proxy['exchange']})")

if __name__ == "__main__":
    main()

