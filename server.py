import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])

# ✅ Handle domain + device info
@socketio.on("domain_detected")
def handle_domain_detected(data):
    print(f"[Domain] {data['domain']} from {data.get('device_ip')} ({data.get('device_name')})")
    emit("new_log", data, broadcast=True)
    emit("new_device_log", {
        "device_name": data.get("device_name", "Unknown"),
        "device_ip": data.get("device_ip"),
        "device_mac": data.get("device_mac")
    }, broadcast=True)

@app.route("/api/filters", methods=["GET", "POST"])
def manage_filters():
    if request.method == "GET":
        with open("targets.json") as f:
            return jsonify(json.load(f))
    else:
        data = request.json
        with open("targets.json", "w") as f:
            json.dump(data, f)
        return jsonify({"status": "updated"})

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5050)
