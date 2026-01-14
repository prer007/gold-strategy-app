from flask import Flask, jsonify, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

# ---- GOLD STRATEGY (SIMPLE & STABLE) ----
def get_signal():
    return {
        "signal": "BUY",
        "price": 421.63,
        "confidence": 100.0,
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

# ---- API ENDPOINT ----
@app.route("/api/signal")
def api_signal():
    return jsonify(get_signal())

# ---- DASHBOARD ----
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Gold Strategy Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: Arial; text-align:center;">
    <h1>Gold Strategy Dashboard</h1>
    <h3>Signal: {{ signal }}</h3>
    <p>Price: {{ price }}</p>
    <p>Confidence: {{ confidence }}%</p>
    <p>Last update: {{ time }}</p>
</body>
</html>
"""

@app.route("/")
def dashboard():
    data = get_signal()
    return render_template_string(
        HTML,
        signal=data["signal"],
        price=data["price"],
        confidence=data["confidence"],
        time=data["time"]
    )

# ---- RENDER ENTRY POINT ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
