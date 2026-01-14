import matplotlib.pyplot as plt
from gold_app_strategy import load_data, run_strategy

print("GENERATING STRATEGY CHART...")

data = run_strategy(load_data())

if len(data) == 0:
    print("No data to plot")
    exit()

# Price
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="Gold Price", color="gold")

# BUY / SELL markers
buy_signals = data[data["signal"] == 1]
sell_signals = data[data["signal"] == 0]

plt.scatter(
    buy_signals.index,
    buy_signals["Close"],
    marker="^",
    color="green",
    label="BUY",
    s=80
)

plt.scatter(
    sell_signals.index,
    sell_signals["Close"],
    marker="v",
    color="red",
    label="SELL",
    s=80
)

plt.title("Gold Strategy – BUY / SELL Signals")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("gold_strategy_signals.png")
plt.close()

# =========================
# Equity Curve
# =========================

equity = (1 + data["strategy_returns"]).cumprod()

plt.figure(figsize=(12, 4))
plt.plot(data.index, equity, color="cyan", label="Equity Curve")
plt.title("Gold Strategy – Equity Curve")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("gold_strategy_equity.png")
plt.close()

print("✅ Charts saved:")
print(" - gold_strategy_signals.png")
print(" - gold_strategy_equity.png")
