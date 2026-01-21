from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Gold Strategy API running"

@app.route("/signal")
def signal():
    return jsonify({
        "price": 2450.12,
        "signal": "BUY",
        "confidence": 78
    })
