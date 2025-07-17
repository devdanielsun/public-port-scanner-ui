import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import threading
import requests
from scanner import scan_tcp, scan_udp

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("start_scan")
def start_scan(data):
    ip = get_public_ip()
    if not ip:
        socketio.emit("scan_result", {"port": 0, "type": "error", "status": "Could not retrieve IP"})
        return

    scan_type = data.get("scan_type", "all")
    ports = data.get("ports", "")

    port_list = []
    if scan_type == "all":
        port_list = list(range(1, 65536))
    elif scan_type == "range":
        try:
            start, end = map(int, ports.split("-"))
            port_list = list(range(start, end + 1))
        except:
            socketio.emit("scan_result", {"port": 0, "type": "error", "status": "Invalid range"})
            return
    elif scan_type == "specific":
        try:
            port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
        except:
            socketio.emit("scan_result", {"port": 0, "type": "error", "status": "Invalid ports"})
            return

    def scan():
        for port in port_list:
            if scan_tcp(ip, port):
                socketio.emit("scan_result", {"port": port, "type": "TCP", "status": "open"})
            if scan_udp(ip, port):
                socketio.emit("scan_result", {"port": port, "type": "UDP", "status": "open"})
        socketio.emit("scan_complete")

    thread = threading.Thread(target=scan)
    thread.start()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)