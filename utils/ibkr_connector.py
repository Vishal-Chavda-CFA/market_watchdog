from ib_insync import IB, util

def fetch_positions_from_ibkr(host='127.0.0.1', port=7496, client_id=1):
    """
    Connects to IBKR TWS or Gateway and fetches current portfolio positions.
    """
    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id)
        positions = ib.positions()

        result = []
        for pos in positions:
            contract = pos.contract
            position_data = {
                'symbol': contract.symbol,
                'secType': contract.secType,
                'currency': contract.currency,
                'exchange': contract.exchange,
                'position': pos.position,
                'avgCost': pos.avgCost
            }
            result.append(position_data)

        return result

    except Exception as e:
        print(f"[ERROR] IBKR connection failed: {e}")
        return []

    finally:
        ib.disconnect()
