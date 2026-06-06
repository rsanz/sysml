#!/usr/bin/env python3
import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PILOT_IMPLEMENTATION_URL = "https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation"


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        if self.path == "/about":
            self._send_json(
                200,
                {
                    "name": "sysmlv2-api-server",
                    "based_on": PILOT_IMPLEMENTATION_URL,
                },
            )
            return
        self._send_json(404, {"error": "not_found"})

    def log_message(self, *_):
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="SysMLv2 API server scaffold")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), Handler)
    print(f"Server listening on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
