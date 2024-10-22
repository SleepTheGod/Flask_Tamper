from mitmproxy import http
import requests

class Interceptor:
    def request(self, flow: http.HTTPFlow):
        # Intercept and log HTTP requests
        print(f"Intercepted request: {flow.request.method} {flow.request.url}")
        headers = dict(flow.request.headers)
        data = {
            'url': flow.request.url,
            'method': flow.request.method,
            'headers': headers,
            'body': flow.request.content.decode('utf-8') if flow.request.content else ''
        }
        requests.post('http://localhost:5000/capture', json=data)

class WebSocketInterceptor:
    def websocket_message(self, flow: http.HTTPFlow):
        # Intercept and log WebSocket messages
        print(f"Intercepted WebSocket message: {flow.message.content}")
        requests.post('http://localhost:5000/capture_ws', json={
            'content': flow.message.content.decode('utf-8')
        })
