from mitmproxy import http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
import requests

class Interceptor:
    def request(self, flow: http.HTTPFlow):
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
        print(f"Intercepted WebSocket message: {flow.message.content}")
        requests.post('http://localhost:5000/capture_ws', json={
            'content': flow.message.content.decode('utf-8')
        })

def start_proxy():
    options = Options(listen_host='0.0.0.0', listen_port=8080, ssl_insecure=True)
    master = DumpMaster(options)
    addon = Interceptor()
    ws_addon = WebSocketInterceptor()
    master.addons.add(addon)
    master.addons.add(ws_addon)
    try:
        master.run()
    except KeyboardInterrupt:
        master.shutdown()

if __name__ == "__main__":
    start_proxy()
