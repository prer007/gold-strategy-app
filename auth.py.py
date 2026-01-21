from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Gold Strategy API is running"

@app.route("/signal")
def signal():
    return jsonify({
        "price": "2350.25",
        "signal": "BUY",
        "confidence": "78%"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
