from flask import Flask, request, render_template, redirect, jsonify
import requests
import threading

app = Flask(__name__)

# Store captured HTTP requests and responses
captured_requests = []

@app.route('/')
def index():
    # Display the UI for tampering with requests
    return render_template('index.html', captured_requests=captured_requests)

# Route for intercepting and modifying HTTP requests
@app.route('/modify_request', methods=['POST'])
def modify_request():
    req_data = request.json
    url = req_data.get('url')
    method = req_data.get('method')
    headers = req_data.get('headers')
    body = req_data.get('body', None)

    # Send the modified request to the target server
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=body)
    else:
        response = requests.request(method, url, headers=headers, data=body)

    # Store the response for inspection
    captured_requests.append({
        'request': req_data,
        'response_status': response.status_code,
        'response_headers': dict(response.headers),
        'response_body': response.text
    })

    return jsonify({
        'status': response.status_code,
        'headers': dict(response.headers),
        'body': response.text
    })

# Capture HTTP requests from the client side
@app.route('/capture', methods=['POST'])
def capture_request():
    data = request.json
    captured_requests.append(data)
    return jsonify(success=True)

# Route to clear captured requests
@app.route('/clear', methods=['POST'])
def clear_captured_requests():
    captured_requests.clear()
    return jsonify(success=True)

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True, port=8080)
