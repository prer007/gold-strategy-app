from flask import Flask, render_template_string, jsonify
import os
import threading
import time

print("STARTING GOLD APP")

app = Flask(__name__)

HTML = """
<h1>Gold Strategy Dashboard</h1>
<p><b>Owner:</b> Justin</p>
<p><b>Signal:</b> {{ signal }}</p>
<p><b>Price:</b> {{ price }}</p>
<p><b>Confidence:</b> {{ confidence }}%</p>
<p><b>Last update:</b> {{ time }}</p>
"""

latest_data = {
    "signal": "BUY",
    "price": 421.63,
    "confidence": 100,
    "time": "LIVE"
}

@app.route("/")
def dashboard():
    return render_template_string(
        HTML,
        **latest_data
    )

@app.route("/api/signal")
def api_signal():
    return jsonify(latest_data)

def dummy_updater():
    while True:
        time.sleep(30)
        print("Heartbeat OK")

if __name__ == "__main__":
    threading.Thread(target=dummy_updater, daemon=True).start()

    port = int(os.environ.get("PORT", 5000))
    print(f"RUNNING ON PORT {port}")
    app.run(host="0.0.0.0", port=port)
