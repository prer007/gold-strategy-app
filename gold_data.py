import yfinance as yf
import pandas as pd

# =====================
# CONFIG
# =====================
ticker = "GLD"
STOP_LOSS_PCT = 0.10  # Change if needed

# =====================
# DOWNLOAD DATA
# =====================
gold = yf.download(
    ticker,
    start="2010-01-01",
    end="2025-01-01",
    interval="1d"
)

gold.columns = gold.columns.get_level_values(0)

# =====================
# INDICATORS
# =====================
gold["Return"] = gold["Close"].pct_change()
gold["MA50"] = gold["Close"].rolling(50).mean()
gold["MA200"] = gold["Close"].rolling(200).mean()

gold["Trend"] = 0
gold.loc[gold["MA50"] > gold["MA200"], "Trend"] = 1
gold.loc[gold["MA50"] < gold["MA200"], "Trend"] = -1

# =====================
# SIGNALS
# =====================
gold["Signal"] = "HOLD"
gold.loc[(gold["Trend"] == 1) & (gold["Trend"].shift(1) == -1), "Signal"] = "BUY"
gold.loc[(gold["Trend"] == -1) & (gold["Trend"].shift(1) == 1), "Signal"] = "SELL"

# =====================
# POSITION & STOP-LOSS
# =====================
gold["Position"] = 0
gold["EntryPrice"] = None

in_position = False
entry_price = 0

for i in range(1, len(gold)):
    price = gold["Close"].iloc[i]

    if gold["Signal"].iloc[i] == "BUY" and not in_position:
        in_position = True
        entry_price = price
        gold.iloc[i, gold.columns.get_loc("Position")] = 1
        gold.iloc[i, gold.columns.get_loc("EntryPrice")] = entry_price

    elif in_position:
        # Stop-loss
        if price <= entry_price * (1 - STOP_LOSS_PCT):
            in_position = False
            gold.iloc[i, gold.columns.get_loc("Signal")] = "STOP"
            gold.iloc[i, gold.columns.get_loc("Position")] = 0
            entry_price = 0

        # Trend exit
        elif gold["Signal"].iloc[i] == "SELL":
            in_position = False
            gold.iloc[i, gold.columns.get_loc("Position")] = 0
            entry_price = 0

        else:
            gold.iloc[i, gold.columns.get_loc("Position")] = 1
            gold.iloc[i, gold.columns.get_loc("EntryPrice")] = entry_price

# =====================
# PERFORMANCE
# =====================
gold["Strategy_Return"] = gold["Position"].shift(1) * gold["Return"]
gold["Strategy"] = (1 + gold["Strategy_Return"]).cumprod()
gold["BuyHold"] = (1 + gold["Return"]).cumprod()

print("\n=== FINAL STRATEGY RESULTS ===")
print(f"Strategy Final Value: {gold['Strategy'].iloc[-1]:.2f}x")
print(f"Buy & Hold Value:    {gold['BuyHold'].iloc[-1]:.2f}x")

# =====================
# SAVE
# =====================
gold.to_csv("gold_final_strategy.csv")
print("Saved gold_final_strategy.csv")
import matplotlib.pyplot as plt

# =====================
# PRICE + SIGNALS PLOT
# =====================
plt.figure()
plt.plot(gold.index, gold["Close"], label="Gold Price")
plt.plot(gold.index, gold["MA50"], label="MA50")
plt.plot(gold.index, gold["MA200"], label="MA200")

# BUY / SELL / STOP markers
buy_signals = gold[gold["Signal"] == "BUY"]
sell_signals = gold[gold["Signal"] == "SELL"]
stop_signals = gold[gold["Signal"] == "STOP"]

plt.scatter(buy_signals.index, buy_signals["Close"], marker="^")
plt.scatter(sell_signals.index, sell_signals["Close"], marker="v")
plt.scatter(stop_signals.index, stop_signals["Close"], marker="x")

plt.legend()
plt.title("Gold Price with Trading Signals")
plt.show()

# =====================
# EQUITY CURVE PLOT
# =====================
plt.figure()
plt.plot(gold.index, gold["Strategy"], label="Strategy")
plt.plot(gold.index, gold["BuyHold"], label="Buy & Hold")

plt.legend()
plt.title("Equity Curve Comparison")
plt.show()
