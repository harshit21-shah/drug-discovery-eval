from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import environ
from urllib.parse import urlparse

from app.assistant import answer


INDEX_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Drug Discovery AI Evaluation</title>
    <style>
      body { font-family: Arial, sans-serif; line-height: 1.55; margin: 40px auto; max-width: 860px; color: #202124; }
      h1, h2 { line-height: 1.2; }
      code, pre { background: #f5f7f9; border-radius: 4px; padding: 2px 4px; }
      section { margin-top: 28px; }
      .note { border-left: 4px solid #3858e9; padding-left: 14px; color: #333; }
    </style>
  </head>
  <body>
    <h1>Drug Discovery Research Assistant Evaluation</h1>
    <p class="note">
      This endpoint supports the Gates Foundation AI Fellows India technical assignment. It exposes
      <code>POST /chat</code> for conversational evaluation and this page as a live summary endpoint.
    </p>
    <section>
      <h2>Evaluation Focus</h2>
      <p>
        The test suite evaluates biomedical factuality, uncertainty handling, safety, evidence reasoning,
        prompt-injection resistance, user experience, and multilingual accessibility for India-context deployment.
      </p>
    </section>
    <section>
      <h2>Endpoint Contract</h2>
      <pre>POST /chat
Content-Type: application/json

{ "message": "What is target identification in drug discovery?" }</pre>
    </section>
    <section>
      <h2>Limitations</h2>
      <p>
        This is a deterministic evaluation target, not a production biomedical model. Its purpose is to make
        evaluation behavior reproducible while demonstrating how a domain-relevant conversational AI system
        should be tested before real deployment.
      </p>
    </section>
  </body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status: int, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler naming.
        path = urlparse(self.path).path
        if path == "/health":
            self._send_json(200, {"status": "ok"})
        elif path == "/":
            self._send_html(200, INDEX_HTML)
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler naming.
        path = urlparse(self.path).path
        if path != "/chat":
            self._send_json(404, {"error": "not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid json"})
            return

        message = payload.get("message")
        if not isinstance(message, str):
            self._send_json(400, {"error": "message must be a string"})
            return

        self._send_json(200, {"response": answer(message)})

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    port = int(environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving on http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()

