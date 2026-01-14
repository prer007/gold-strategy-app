import os
import threading
import time
from flask import Flask, render_template_string
from gold_app_strategy import load_data, run_strategy, confidence_score

print("STARTING GOLD APP")

app = Flask(__name__)

HTML = """
<h1>Gold Strategy Dashboard</h1>

<p><b>Owner:</b> Justin</p>
<p><b>Signal:</b> {{ signal }}</p>
<p><b>Price:</b> {{ price }}</p>
<p><b>Confidence:</b> {{ confidence }}%</p>
<p><b>Last update:</b> {{ time }}</p>

<hr>
<p style="font-size:12px;">
This software is provided for educational purposes only.<br>
No financial advice is given.
</p>
"""

# Shared state (SAFE)
latest_data = {
    "signal": "LOADING",
    "price": 0.0,
    "confidence": 0,
    "time": "N/A"
}

def update_strategy():
    while True:
        try:
            data = load_data()
            if data is None or len(data) == 0:
                print("No data yet, retrying...")
                time.sleep(60)
                continue

            data = run_strategy(data)
            last = data.iloc[-1]

            signal_val = int(last["signal"])
            price_val = float(last["Close"])

            latest_data["signal"] = "BUY" if signal_val == 1 else "SELL / CASH"
            latest_data["price"] = round(price_val, 2)
            latest_data["confidence"] = confidence_score(data)
            latest_data["time"] = str(last.name)

            print(
                "LIVE UPDATE:",
                latest_data["signal"],
                latest_data["price"],
                latest_data["confidence"]
            )

        except Exception as e:
            print("UPDATE ERROR:", e)

        time.sleep(60)  # update once per minute

@app.route("/")
def dashboard():
    return render_template_string(
        HTML,
        signal=latest_data["signal"],
        price=latest_data["price"],
        confidence=latest_data["confidence"],
        time=latest_data["time"]
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
