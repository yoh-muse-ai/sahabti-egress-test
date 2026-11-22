import os, socket
from http.server import BaseHTTPRequestHandler, HTTPServer

def probe(host, port):
    try:
        s = socket.create_connection((host, port), timeout=3)
        s.settimeout(3)
        banner = s.recv(100).decode("utf-8", "replace").strip()
        s.close()
        return "REACHABLE banner=" + banner
    except Exception as e:
        return "FAIL: " + str(e)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        lines = ["PRIVATE NETWORK PROBE", ""]
        for ip in ("10.81.0.10", "10.81.0.13"):
            lines.append(ip + ":22 -> " + probe(ip, 22))
        body = ("\n".join(lines) + "\n").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass

HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), H).serve_forever()
