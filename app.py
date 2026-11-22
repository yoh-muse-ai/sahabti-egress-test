import os, json, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "egress-test"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return "ERROR: " + str(e)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = "EGRESS CHECK\n\nipinfo.io:\n" + fetch("https://ipinfo.io/json") + "\n\nip-api.com:\n" + fetch("http://ip-api.com/json") + "\n"
        data = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, *a):
        pass

HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), H).serve_forever()
