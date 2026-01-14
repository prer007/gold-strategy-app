from flask import Flask, jsonify
import threading
import time as time_module
from gold_app_strategy import load_data, run_strategy, confidence_score

app = Flask(__name__)

latest = {
    "signal": "LOADING",
    "price": 0.0,
    "confidence": 0,
    "time": "N/A"
}

def update_loop():
    while True:
        try:
            data = run_strategy(load_data())
            if len(data) == 0:
                time_module.sleep(30)
                continue

            last = data.iloc[-1]

            signal_value = int(last["signal"].item())
            price_value = float(last["Close"].item())

            latest["signal"] = "BUY" if signal_value == 1 else "SELL / CASH"
            latest["price"] = round(price_value, 2)
            latest["confidence"] = int(confidence_score(data))
            latest["time"] = str(last.name)

            print("API UPDATE:", latest)

        except Exception as e:
            print("ERROR:", e)

        time_module.sleep(30)

@app.route("/api/signal")
def get_signal():
    return jsonify(latest)

if __name__ == "__main__":
    threading.Thread(target=update_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
