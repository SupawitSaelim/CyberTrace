# scanner/port_scanner.py
import socket

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        if result == 0:
            return f"Port {port} is open"
        else:
            pass
    except Exception as e:
        return f"Error: {e}"
