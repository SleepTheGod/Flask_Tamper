from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from vulnerability_scanner import scan_vulnerability
from ml_detection import detect_anomaly
import requests
import json

app = Flask(__name__)
socketio = SocketIO(app)
request_log = []

@app.route('/')
def index():
    return render_template('index.html')

# Real-time capture and anomaly detection
@app.route('/capture', methods=['POST'])
def capture_request():
    data = request.json
    headers = data['headers']
    body = data['body']
    
    is_anomalous = detect_anomaly(headers, body)
    anomalies = deep_analysis(data)  # Use deep inspection function

    log_entry = {
        'url': data['url'],
        'method': data['method'],
        'headers': headers,
        'body': body,
        'anomalous': is_anomalous,
        'anomalies': anomalies
    }
    request_log.append(log_entry)
    socketio.emit('new_request', log_entry)
    return jsonify({'status': 'captured'})

# Deep analysis for filtering and inspection
def deep_analysis(data):
    suspicious_headers = ['Authorization', 'Cookie', 'User-Agent']
    anomalies = []

    # Check headers for suspicious values
    for header, value in data['headers'].items():
        if header in suspicious_headers and 'admin' in value:
            anomalies.append(f"Possible admin bypass attempt in {header}: {value}")
    
    # Check body for potential SQL injection patterns
    if any(keyword in data['body'] for keyword in ['SELECT', 'DROP', '--', "';--", '"--']):
        anomalies.append("Possible SQL Injection detected in body")

    return anomalies

# Vulnerability scanning endpoint
@app.route('/scan', methods=['POST'])
def scan_url():
    data = request.json
    url = data.get('url')
    result = scan_vulnerability(url)
    return jsonify({'status': 'scanned', 'result': result})

# Fuzzing endpoint
@app.route('/fuzz', methods=['POST'])
def fuzz_request():
    data = request.json
    url = data['url']
    headers = data['headers']
    payloads = fuzz_payloads()

    results = []
    for attack_type, fuzzes in payloads.items():
        for fuzz in fuzzes:
            modified_body = data['body'].replace('<FUZZ>', fuzz)
            response = requests.request(data['method'], url, headers=headers, data=modified_body)
            results.append({
                'payload': fuzz,
                'status_code': response.status_code,
                'response_body': response.text
            })
    
    return jsonify({'status': 'fuzzed', 'results': results})

def fuzz_payloads():
    with open('fuzzing/payloads.json') as f:
        return json.load(f)

# WebSocket communication capture
@app.route('/capture_ws', methods=['POST'])
def capture_websocket():
    data = request.json
    print(f"Intercepted WebSocket message: {data['content']}")
    return jsonify({'status': 'captured'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
