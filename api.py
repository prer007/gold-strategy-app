from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Gold Strategy API is running"

@app.route("/signal", methods=["GET"])
def signal():
    return jsonify({
        "price": 2450.12,
        "signal": "BUY",
        "confidence": 78,
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })

if __name__ == "__main__":
    app.run()
