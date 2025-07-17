import socket

def scan_tcp(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            return result == 0
    except:
        return False

def scan_udp(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.sendto(b'', (ip, port))
            s.recvfrom(1024)
            return True
    except socket.timeout:
        return False
    except:
        return False