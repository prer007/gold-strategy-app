"""
===========================================================
APP NAME: Gold Signal Engine
VERSION: 1.1.0
OWNER: Justin
COPYRIGHT © 2026 Justin. All Rights Reserved.
===========================================================

THIS SOFTWARE PROVIDES MARKET ANALYSIS ONLY.
NO FINANCIAL ADVICE.
NO TRADE EXECUTION.
"""

# =========================
# DEPENDENCIES
# =========================
import sys
import subprocess
from datetime import datetime
import json

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

try:
    import matplotlib.pyplot as plt
except ImportError:
    install("matplotlib")
    import matplotlib.pyplot as plt

import yfinance as yf
import pandas as pd
import numpy as np

# =========================
# APP METADATA
# =========================
APP_NAME = "Gold Signal Engine"
VERSION = "1.1.0"
OWNER = "Justin"
RUN_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

WATERMARK = f"{APP_NAME} v{VERSION} | © {OWNER} | {RUN_TIME}"

# =========================
# TERMS OF USE (LEGAL)
# =========================
TERMS = f"""
TERMS OF USE – {APP_NAME}

• Educational & informational only
• NOT financial advice
• NOT investment advice
• No trades executed
• No funds handled

ANTI-SCAM NOTICE:
This app will NEVER ask for:
• Money
• Wallet keys
• Login credentials
• Brokerage access

Owner ({OWNER}) is not liable for losses.
"""

print(TERMS)

with open("TERMS_OF_USE.txt", "w") as f:
    f.write(TERMS)

# =========================
# SETTINGS
# =========================
GOLD = "GLD"
SHORT_MA = 40
LONG_MA = 150

# =========================
# DOWNLOAD DATA
# =========================
df = yf.download(GOLD, start="2005-01-01", interval="1d")
df.columns = df.columns.droplevel(1)
df = df[['Close']].dropna()

# =========================
# INDICATORS
# =========================
df['SMA_short'] = df['Close'].rolling(SHORT_MA).mean()
df['SMA_long'] = df['Close'].rolling(LONG_MA).mean()
df.dropna(inplace=True)

# =========================
# SIGNAL ENGINE
# =========================
df['signal'] = 0
df.loc[df['SMA_short'] > df['SMA_long'], 'signal'] = 1
df['signal_change'] = df['signal'].diff()

# =========================
# CONFIDENCE SCORE (0–100)
# =========================
df['confidence'] = (
    abs(df['SMA_short'] - df['SMA_long']) / df['Close']
) * 500
df['confidence'] = df['confidence'].clip(0, 1) * 100
df['confidence'] = df['confidence'].round(1)

# =========================
# ALERTS (LIVE STYLE)
# =========================
alerts = df[df['signal_change'] != 0][
    ['Close', 'signal', 'confidence']
]

for date, row in alerts.iterrows():
    action = "BUY" if row['signal'] == 1 else "SELL"
    print(f"🔔 {date.date()} | {action} | Confidence: {row['confidence']}%")

# =========================
# PERFORMANCE
# =========================
df['returns'] = df['Close'].pct_change()
df['strategy_returns'] = df['returns'] * df['signal'].shift(1)
df['equity'] = (1 + df['strategy_returns']).cumprod()

# =========================
# PLOT BUY / SELL MARKERS
# =========================
plt.figure(figsize=(14,7))
plt.plot(df.index, df['Close'], label="Gold Price", alpha=0.8)
plt.plot(df.index, df['SMA_short'], linestyle="--", label="Short MA")
plt.plot(df.index, df['SMA_long'], linestyle="--", label="Long MA")

buy_signals = df[df['signal_change'] == 1]
sell_signals = df[df['signal_change'] == -1]

plt.scatter(buy_signals.index, buy_signals['Close'], marker="^", s=100)
plt.scatter(sell_signals.index, sell_signals['Close'], marker="v", s=100)

plt.title("Gold BUY / SELL Signals\n" + WATERMARK)
plt.legend()
plt.grid()
plt.savefig("gold_signals.png")
plt.show()

# =========================
# SAVE DATA
# =========================
df['watermark'] = WATERMARK
df.to_csv("gold_signals_with_confidence.csv")

# =========================
# READ-ONLY API EXPORT
# =========================
api_output = {
    "app": APP_NAME,
    "version": VERSION,
    "owner": OWNER,
    "generated": RUN_TIME,
    "latest_signal": int(df['signal'].iloc[-1]),
    "confidence": float(df['confidence'].iloc[-1]),
    "disclaimer": "Educational use only. No financial advice."
}

with open("api_read_only.json", "w") as f:
    json.dump(api_output, f, indent=4)

# =========================
# APP STORE LEGAL TEXT
# =========================
LEGAL_TEXT = f"""
{APP_NAME}

Market trend visualization tool.
No financial advice.
No trade execution.
No user funds.

Owner: {OWNER}
Version: {VERSION}
"""

with open("LEGAL_APP_TEXT.txt", "w") as f:
    f.write(LEGAL_TEXT)

print("\n✅ ALL FILES GENERATED")
print("• gold_signals.png")
print("• gold_signals_with_confidence.csv")
print("• api_read_only.json")
print("• TERMS_OF_USE.txt")
print("• LEGAL_APP_TEXT.txt")
print("\n🛡️ APP OWNER PROTECTION ACTIVE")
