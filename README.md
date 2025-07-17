# Public Port Scanner UI

A simple web-based TCP and UDP port scanner for your **public IP address**, with live results streamed to the browser. Supports scanning **all ports**, a **custom range**, or **specific ports**. Built using Flask and Socket.IO, and can be easily deployed via Docker.

## 🚀 Features

- 🔍 Scan **TCP and UDP ports**
- 🎯 Options to scan:
  - All ports (1–65535)
  - Custom port range (e.g., 20–100)
  - Specific ports (e.g., 22,80,443)
- 🌐 Automatically detects your public IP
- 📡 Real-time results in browser
- 🐳 Docker-ready for easy deployment

## 🧱 Tech Stack

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [Socket.IO](https://socket.io/)
- Python 3.11

## ⚙️ Installation

### 🔧 Local Setup

```bash
git clone https://github.com/devdanielsun/public-port-scanner-ui.git
cd public-port-scanner-ui
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

On windows:

```bash
...
pip3 install -U pip virtualenv
virtualenv --system-site-packages -p python ./venv
.\venv\Scripts\activate
...
```

Visit: [http://localhost:5000](http://localhost:5000)

### 🐳 Docker Setup

```bash
docker build -t public-port-scanner .
docker run -d --rm -p 5000:5000 --cap-add=NET_RAW --cap-add=NET_ADMIN public-port-scanner
```

> **Note:** `--cap-add` is required for accurate UDP scanning in Docker.


## 🔐 Disclaimer

This scanner only scans **your own public IP address**. Unauthorized scanning of third-party systems may be illegal.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing

Pull requests are welcome! If you have suggestions or issues, feel free to open an issue or submit a PR.