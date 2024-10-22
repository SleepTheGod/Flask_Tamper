from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# Store request log
request_log = []

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Capture HTTP request and emit to the frontend
@app.route('/capture', methods=['POST'])
def capture_request():
    data = request.json
    log_entry = {
        'url': data['url'],
        'method': data['method'],
        'headers': data['headers'],
        'body': data['body']
    }
    request_log.append(log_entry)
    socketio.emit('new_request', log_entry)
    return jsonify({'status': 'captured'})

# Modify request and replay it
@app.route('/modify', methods=['POST'])
def modify_request():
    data = request.json
    method = data['method']
    url = data['url']
    headers = data['headers']
    body = data['body']

    # Replay the modified request
    response = requests.request(method, url, headers=headers, data=body)
    return jsonify({
        'status': 'success',
        'response': {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response.text
        }
    })

# Real-time data handling via SocketIO
@socketio.on('capture_request')
def handle_capture_request(data):
    emit('new_request', data)

# Run Flask with SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True)
