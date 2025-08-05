# 🛡️ Market Watchdog

**Market Watchdog** is an automated monitoring system that runs silently in the background, watching your investment portfolio for volatility breaches, fetching real-time news, and delivering concise, curated alerts directly to your phone.

---

## 🚀 Overview

Market Watchdog is designed to:

1. **Autostart on Machine Boot**  
   - Logs into Interactive Brokers' TWS automatically.  
   - No manual login required.

2. **Extract Holdings from IBKR**  
   - Pulls live holdings using IB API.  
   - Parses into a Python dataframe.

3. **Resolve Proxies for Each Holding**  
   - Matches each holding to a high-fidelity performance proxy.  
   - Uses OpenAI API to intelligently resolve edge cases.

4. **Benchmarking**  
   - Yesterday’s closing price serves as the baseline.  
   - Historical data fetched via `yfinance` or IBKR API.

5. **Volatility Tuning**  
   - Pulls 10-year historical data to compute average daily move.  
   - Adjusts for recent volatility trends.

6. **Real-Time Intraday Monitoring**  
   - Checks every 15 seconds during market hours.  
   - Monitors for breaches of adjusted thresholds.

7. **News Triage via Perplexity**  
   - Breaches trigger queries to Perplexity.  
   - News is scraped, summarized, and filtered (Bloomberg prioritized).

8. **SMS Alerts**  
   - Condensed alerts delivered via AT&T’s email-to-text gateway.  
   - Includes proxy name, % move, summary, and Bloomberg link (if available).

9. **Repeat Notifications**  
   - Sends updates every 2 hours post-breach until market close.  
   - One alert per proxy per breach window.

10. **Fault Tolerance**  
    - Detects TWS disconnects or failures.  
    - Auto-reinitiates and confirms via SMS.

---

## 🧠 Example Workflow

```bash
1. Power on laptop
2. Market Watchdog autostarts
3. Logs into IBKR TWS
4. Extracts and resolves portfolio holdings
5. Monitors intraday volatility for each proxy
6. If breach detected → fetch market news → send SMS alert
7. Repeat updates every 2 hours (if breach remains)
