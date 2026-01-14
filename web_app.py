from flask import Flask, jsonify
import yfinance as yf
import pandas as pd
import datetime
import os

app = Flask(__name__)

def get_signal():
    try:
        data = yf.download("GLD", period="6mo", interval="1d", progress=False)

        if data.empty:
            return {
                "signal": "NO DATA",
                "price": 0,
                "confidence": 0,
                "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }

        data["SMA20"] = data["Close"].rolling(20).mean()
        data["SMA50"] = data["Close"].rolling(50).mean()

        last = data.iloc[-1]

        signal = "BUY" if last["SMA20"] > last["SMA50"] else "SELL"
        confidence = 100.0 if signal == "BUY" else 60.0

        return {
            "signal": signal,
            "price": round(float(last["Close"]), 2),
            "confidence": confidence,
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }

    except Exception as e:
        return {
            "signal": "ERROR",
            "price": 0,
            "confidence": 0,
            "time": str(e)
        }

@app.route("/")
def home():
    return "Gold Strategy API is running"

@app.route("/api/signal")
def api_signal():
    return jsonify(get_signal())

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
