import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import requests
from scanner import scan_tcp, scan_udp

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, async_mode="eventlet")

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_public_ip")
def public_ip():
    ip = get_public_ip()
    return ip if ip else "Unavailable"

@socketio.on("start_scan")
def start_scan(data):
    ip = get_public_ip()
    if not ip:
        socketio.emit("scan_result", {"port": -1, "type": "error", "status": "Could not retrieve IP"})
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
            socketio.emit("scan_result", {"port": -1, "type": "error", "status": "Invalid range"})
            return
    elif scan_type == "specific":
        try:
            port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
        except:
            socketio.emit("scan_result", {"port": -1, "type": "error", "status": "Invalid ports"})
            return

    def valid_port(p):
        return 1 <= p <= 65535

    # After parsing port_list
    port_list = [p for p in port_list if valid_port(p)]
    if not port_list:
        socketio.emit("scan_result", {"port": -1, "type": "error", "status": "No valid ports to scan"})
        return
    
    def scan():
        for port in port_list:
            socketio.emit("scan_progress", {"port": port})

            if scan_tcp(ip, port):
                socketio.emit("scan_result", {"port": port, "type": "TCP", "status": "open"})
            if scan_udp(ip, port):
                socketio.emit("scan_result", {"port": port, "type": "UDP", "status": "open"})

        socketio.emit("scan_progress", {"port": port, "status": "completed"})
        socketio.emit("scan_complete")

    eventlet.spawn(scan)

if __name__ == "__main__":
    print("Server is running on http://localhost:5000")
    socketio.run(app, host="0.0.0.0", port=5000)
    