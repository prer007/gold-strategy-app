from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Gold Strategy API running"

@app.route("/signal")
def signal():
    return jsonify({
        "price": 2450.12,
        "signal": "BUY",
        "confidence": 78,
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
