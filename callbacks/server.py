"""
Minimal callback/webhook server using only Python stdlib.

Endpoints:
- GET /oauth/callback          -> logs query (code,state,id_token,etc.) and shows a simple page
- POST /apple/notifications    -> logs JSON body, returns 200
- GET /healthz                 -> liveness probe

Run:
  python callbacks/server.py --port 8787

Notes:
- Uses only stdlib, no extra installs required.
- Pair with a free no-account tunnel (see callbacks/README.md) to get a public https URL.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import argparse
import sys


class Handler(BaseHTTPRequestHandler):
    server_version = "CraftXCallback/1.0"

    def _log(self, message: str):
        sys.stdout.write(message + "\n")
        sys.stdout.flush()

    def _send_json(self, obj: dict, status: int = 200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, status: int = 200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802 (stdlib style)
        parsed = urlparse(self.path)
        if parsed.path == "/healthz":
            return self._send_json({"status": "ok"})

        if parsed.path == "/oauth/callback":
            params = {k: v[0] if isinstance(v, list) and v else v for k, v in parse_qs(parsed.query).items()}
            self._log(f"[oauth/callback] query: {json.dumps(params)}")
            html = (
                "<html><head><title>Callback received</title></head><body>"
                "<h2>Callback received</h2>"
                "<p>You can return to the app. Details logged on the server console.</p>"
                "</body></html>"
            )
            return self._send_html(html)

        # Fallback 404
        return self._send_json({"error": "not_found", "path": parsed.path}, status=404)

    def do_POST(self):  # noqa: N802
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length else b""
        body_text = raw.decode("utf-8", errors="replace")

        if parsed.path == "/apple/notifications":
            # Log raw body (Apple sends JWT or JSON depending on config).
            self._log(f"[apple/notifications] body: {body_text}")
            # Echo minimal ack
            try:
                payload = json.loads(body_text)
            except Exception:
                payload = {"raw": body_text}
            return self._send_json({"status": "received", "echo": payload})

        return self._send_json({"error": "not_found", "path": parsed.path}, status=404)


def main():
    parser = argparse.ArgumentParser(description="Minimal callback/webhook server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8787, help="Bind port (default 8787)")
    args = parser.parse_args()

    addr = (args.host, args.port)
    httpd = HTTPServer(addr, Handler)
    print(f"[server] listening on http://{args.host}:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[server] shutting down...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
