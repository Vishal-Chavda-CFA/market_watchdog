import yfinance as yf
import pandas as pd

def directional_volatility_weighting(vol_30, vol_60, vol_90):
    """
    Determines a directional volatility weight based on the trend of recent volatilities.
    """
    if vol_30 > vol_60 > vol_90:
        return 1.2  # Volatility rising
    elif vol_30 < vol_60 < vol_90:
        return 0.85  # Volatility falling
    else:
        return 1.0  # Neutral

def compute_adjusted_tolerance(ticker):
    """
    For a given ticker, compute the adjusted daily movement tolerance based on 10y historical data
    and volatility trend.
    """
    try:
        data = yf.download(ticker, period="10y", interval="1d")
        data['returns'] = data['Adj Close'].pct_change()
        data.dropna(inplace=True)

        avg_daily_move = data['returns'].abs().mean()
        long_term_vol = data['returns'].std()

        vol_30 = data['returns'].rolling(30).std().iloc[-1]
        vol_60 = data['returns'].rolling(60).std().iloc[-1]
        vol_90 = data['returns'].rolling(90).std().iloc[-1]

        recent_vol_avg = (vol_30 + vol_60 + vol_90) / 3
        vol_ratio = recent_vol_avg / long_term_vol

        directional_weight = directional_volatility_weighting(vol_30, vol_60, vol_90)
        adjusted_tolerance = avg_daily_move * vol_ratio * directional_weight

        return {
            'ticker': ticker,
            'avg_daily_move': avg_daily_move,
            'adjusted_tolerance': adjusted_tolerance,
            'vol_ratio': vol_ratio,
            'directional_weight': directional_weight,
            'vol_30': vol_30,
            'vol_60': vol_60,
            'vol_90': vol_90,
            'long_term_vol': long_term_vol
        }

    except Exception as e:
        print(f"[ERROR] Failed to compute adjusted tolerance for {ticker}: {e}")
        return None
