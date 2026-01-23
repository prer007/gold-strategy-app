from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/signal")
def signal():
    return jsonify({
        "price": 2450.12,
        "signal": "BUY",
        "confidence": 78
    })

@app.route("/")
def home():
    return "Gold Strategy API running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
