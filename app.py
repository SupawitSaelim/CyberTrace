from flask import Flask, render_template, request
from scanner.port_scanner import scan_port
from flask import jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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





if __name__ == "__main__":
    app.run(debug=True)
