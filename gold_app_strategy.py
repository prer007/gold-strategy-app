"""
=========================================================
GOLD TREND STRATEGY — APP-READY VERSION
Owner: Justin
Version: 1.0.1

LEGAL NOTICE:
Educational & informational only. Not financial advice.
No guarantees. No auto-trading. No account access.

ANTI-SCAM PROTECTION:
- Informational signals only
- No execution logic
- No brokerage connections
=========================================================
"""

# ===================== IMPORTS =====================
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ===================== CONFIG =====================
APP_VERSION = "1.0.1"
APP_OWNER = "Justin"

SHORT_MA = 40
LONG_MA = 150
STOP_LOSS_PCT = 0.08
CONFIDENCE_LOOKBACK = 20

# ===================== DATA =====================
def load_data():
    gold = yf.download("GLD", start="2005-01-01", interval="1d", auto_adjust=True)
    sp500 = yf.download("^GSPC", start="2005-01-01", interval="1d", auto_adjust=True)

    # ✅ FIX: Flatten columns
    gold.columns = gold.columns.get_level_values(0)
    sp500.columns = sp500.columns.get_level_values(0)

    gold = gold[['Close']].dropna()
    sp500 = sp500[['Close']].dropna()

    sp500['SMA_200'] = sp500['Close'].rolling(200).mean()
    sp500['bearish'] = sp500['Close'] < sp500['SMA_200']

    data = gold.join(sp500['bearish'], how='inner')
    return data

# ===================== STRATEGY =====================
def run_strategy(data):
    data['SMA_short'] = data['Close'].rolling(SHORT_MA).mean()
    data['SMA_long'] = data['Close'].rolling(LONG_MA).mean()
    data.dropna(inplace=True)

    data['signal'] = 0
    position = 0
    entry_price = 0

    for i in range(1, len(data)):
        if position == 0:
            if data['SMA_short'].iloc[i] > data['SMA_long'].iloc[i] and data['bearish'].iloc[i]:
                position = 1
                entry_price = data['Close'].iloc[i]
        else:
            if data['Close'].iloc[i] < entry_price * (1 - STOP_LOSS_PCT):
                position = 0
            elif data['SMA_short'].iloc[i] < data['SMA_long'].iloc[i]:
                position = 0

        data.iloc[i, data.columns.get_loc('signal')] = position

    data['returns'] = data['Close'].pct_change()
    data['strategy_returns'] = data['returns'] * data['signal'].shift(1)
    data['equity'] = (1 + data['strategy_returns']).cumprod()

    return data

# ===================== CONFIDENCE SCORE =====================
def confidence_score(data):
    vol = data['returns'].rolling(CONFIDENCE_LOOKBACK).std()
    trend = abs(data['SMA_short'] - data['SMA_long']) / data['Close']
    score = (trend / vol).clip(0, 1)
    return round(score.iloc[-1] * 100, 1)

# ===================== DASHBOARD =====================
def dashboard(data):
    last_signal = "BUY" if data['signal'].iloc[-1] == 1 else "SELL / CASH"

    max_dd = ((data['equity'] / data['equity'].cummax()) - 1).min()
    sharpe = (data['strategy_returns'].mean() /
              data['strategy_returns'].std()) * np.sqrt(252)

    print("\n================ DASHBOARD ================")
    print(f"Owner: {APP_OWNER}")
    print(f"Version: {APP_VERSION}")
    print(f"Date: {datetime.now().date()}")
    print("------------------------------------------")
    print(f"Signal: {last_signal}")
    print(f"Equity Multiple: {round(data['equity'].iloc[-1], 2)}x")
    print(f"Max Drawdown: {round(max_dd * 100, 2)}%")
    print(f"Sharpe Ratio: {round(sharpe, 2)}")
    print(f"Confidence: {confidence_score(data)}%")
    print("===========================================\n")

# ===================== ALERT =====================
def send_alert(data):
    last = data.iloc[-1]
    alert = {
        "time": str(datetime.now()),
        "signal": "BUY" if last['signal'] == 1 else "SELL / CASH",
        "price": round(last['Close'], 2),
        "confidence": confidence_score(data),
        "version": APP_VERSION
    }
    print("🔔 ALERT:", alert)

# ===================== PLOT =====================
def plot_signals(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Gold Price', alpha=0.8)
    plt.plot(data['SMA_short'], label='Short MA')
    plt.plot(data['SMA_long'], label='Long MA')

    buys = data[data['signal'] == 1]
    sells = data[data['signal'] == 0]

    plt.scatter(buys.index, buys['Close'], color='green', marker='^', label='BUY')
    plt.scatter(sells.index, sells['Close'], color='red', marker='v', label='SELL')

    plt.legend()
    plt.title("Gold Strategy Signals")
    plt.tight_layout()
    plt.savefig("gold_strategy_chart.png")
    plt.show()

# ===================== MAIN =====================
if __name__ == "__main__":
    data = load_data()
    data = run_strategy(data)

    data.to_csv("gold_strategy_signals.csv")

    dashboard(data)
    send_alert(data)
    plot_signals(data)

    print("✅ Strategy run complete.")
