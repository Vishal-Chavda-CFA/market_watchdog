import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_volatility_stats(proxy_ticker: str):
    """
    Given a proxy ticker, returns historical volatility stats:
    - 10-year daily standard deviation
    - 90-day rolling annualized volatility
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365 * 10)

    try:
        df = yf.download(proxy_ticker, start=start_date, end=end_date, progress=False)

        if df.empty or 'Adj Close' not in df:
            raise ValueError(f"No data returned for: {proxy_ticker}")

        df['Returns'] = df['Adj Close'].pct_change()
        df.dropna(inplace=True)

        # 10-year daily standard deviation (non-annualized)
        long_term_std = df['Returns'].std()

        # Rolling 90-day annualized volatility
        df['RollingVol90'] = df['Returns'].rolling(window=90).std() * (252 ** 0.5)
        recent_rolling_vol = df['RollingVol90'].iloc[-1]

        return {
            'proxy': proxy_ticker,
            '10y_std_dev': round(long_term_std, 6),
            'rolling_90d_vol': round(recent_rolling_vol, 6),
            'latest_price': round(df['Adj Close'].iloc[-1], 2)
        }

    except Exception as e:
        print(f"[ERROR] Volatility fetch failed for {proxy_ticker}: {e}")
        return {
            'proxy': proxy_ticker,
            '10y_std_dev': None,
            'rolling_90d_vol': None,
            'latest_price': None
        }
