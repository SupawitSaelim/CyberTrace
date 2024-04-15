from flask import Flask, render_template, request, jsonify
from scanner.port_scanner import scan_port
import socket
import netifaces

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanning')
def scanning():
    return render_template('scanning.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/getinfo')
def getinfo():
    computer_name, private_ip, prefix, mac_address = get_private_ip_hostname_prefix_and_mac()
    return render_template('getinfo.html', computer_name=computer_name, private_ip=private_ip, prefix=prefix, mac_address=mac_address)

@app.route('/scan', methods=['POST'])
def scan():
    target_ip = request.form['target_ip']
    start_port = int(request.form['start_port'])
    end_port = int(request.form['end_port'])
    
    results = {}
    for port in range(start_port, end_port + 1):
        result = scan_port(target_ip, port)
        if result is not None:
            results[port] = result

    return jsonify(results)

def get_private_ip_hostname_prefix_and_mac():
    hostname = socket.gethostname()
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface != "lo":
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                ipv4_info = addresses[netifaces.AF_INET][0]
                ip_address = ipv4_info.get("addr")
                netmask = ipv4_info.get("netmask")
                if not ip_address.startswith("127."):
                    prefix = sum(bin(int(x)).count('1') for x in netmask.split('.'))
                    mac_address = addresses[netifaces.AF_LINK][0]["addr"]
                    return hostname, ip_address, prefix, mac_address
    return None, None, None, None

if __name__ == "__main__":
    app.run(debug=True)
