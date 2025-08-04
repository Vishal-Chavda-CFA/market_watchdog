# utils/proxy_resolver.py

import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def resolve_proxies_for_holdings(holdings: list) -> list:
    """
    Accepts a list of holdings where each is a dict like:
    {'symbol': 'MHG', 'secType': 'FUT', 'description': 'Copper Futures', 'exchange': ''}

    Returns a list of proxy dicts like:
    {'symbol': 'CPER', 'secType': 'STK', 'exchange': 'ARCA'}
    """
    try:
        # Format input block for prompt
        input_block = ""
        for h in holdings:
            input_block += f"- Symbol: {h.get('symbol')}, SecType: {h.get('secType')}, Desc: {h.get('description', '')}, Exchange: {h.get('exchange', '')}\n"

        # Add example mappings to help the model learn your style
        proxy_examples = (
            "Here are a few examples of how to resolve complex or non-equity instruments:\n"
            "- M2K (Micro Russell 2000 Futures) → IWM (STK on ARCA)\n"
            "- MHG (Copper Futures) → CPER (STK on ARCA)\n"
            "- MGC (Gold Futures) → GLD (STK on ARCA)\n"
            "- MET (Ethereum Futures) → ETH (CRYPTO on PAXOS)\n\n"
        )

        user_prompt = (
            f"{proxy_examples}"
            f"Now resolve the following holdings:\n{input_block}\n\n"
            "Respond ONLY with a JSON array. Example format:\n"
            '[{"symbol": "IWM", "secType": "STK", "exchange": "ARCA"}]'
        )

        system_msg = (
            "You are a financial market proxy resolver. Given a list of securities, return the best matching "
            "**TWS-compatible proxy instruments** that represent their price behavior. Output ONLY a JSON array "
            "with fields: `symbol`, `secType`, `exchange`. Do not explain or add any text outside the array. "
            "Use valid TWS-compatible instruments only."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )

        result = response['choices'][0]['message']['content'].strip()
        proxy_data = json.loads(result)

        if not isinstance(proxy_data, list):
            raise ValueError("Expected a list of proxy objects in JSON array format.")

        return proxy_data

    except Exception as e:
        print(f"[ERROR] Failed to resolve batch proxies: {e}")
        return [{"symbol": "UNKNOWN", "secType": "UNKNOWN", "exchange": "UNKNOWN"} for _ in holdings]
