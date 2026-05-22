from __future__ import annotations

import json
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import environ
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from app.assistant import answer
from app.llm_client import llm_available, llm_status


ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "results" / "cerai_evaluation_results.json"
BENCHMARK_PATH = ROOT / "results" / "benchmark_evaluation_results.json"
STATIC_RESULTS = {
    "/results/analytics.html": ("text/html; charset=utf-8", ROOT / "results" / "analytics.html"),
    "/results/pass_rate_by_category.svg": ("image/svg+xml", ROOT / "results" / "pass_rate_by_category.svg"),
    "/results/failure_analysis.md": ("text/markdown; charset=utf-8", ROOT / "results" / "failure_analysis.md"),
}


def _load_summary() -> dict[str, object]:
    if RESULTS_PATH.exists():
        return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    fallback = ROOT / "results" / "local_evaluation_results.json"
    if fallback.exists():
        return json.loads(fallback.read_text(encoding="utf-8"))
    return {}


def _render_index() -> str:
    summary = _load_summary()
    benchmark = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8")) if BENCHMARK_PATH.exists() else {}
    total = summary.get("total_tests", "—")
    passed = summary.get("pass_count", "—")
    avg = summary.get("average_combined_score", summary.get("average_score", "—"))
    bench_total = benchmark.get("total_tests", "-")
    bench_passed = benchmark.get("pass_count", "-")
    bench_avg = benchmark.get("average_combined_score", "-")
    status = llm_status()
    llm_on = (
        f"enabled ({status['provider']}: {status['model']})"
        if status["llm_enabled"]
        else str(status.get("hint", "set GROQ_API_KEY or OPENAI_API_KEY"))
    )
    tool = summary.get("evaluation_tool", "Run scripts/run_cerai_evaluation.py")

    rows = ""
    for name, stats in (summary.get("category_summary") or {}).items():
        pc = stats.get("pass_count", "—")
        tc = stats.get("test_count", "—")
        sc = stats.get("average_combined_score", stats.get("average_score", "—"))
        rows += f"<tr><td>{name}</td><td>{pc}/{tc}</td><td>{sc}</td></tr>\n"

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Drug Discovery AI Evaluation</title>
    <style>
      body {{ font-family: Arial, sans-serif; line-height: 1.55; margin: 40px auto; max-width: 900px; color: #202124; }}
      h1, h2 {{ line-height: 1.2; }}
      code, pre {{ background: #f5f7f9; border-radius: 4px; padding: 2px 4px; }}
      table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
      th, td {{ border: 1px solid #d8dee4; padding: 8px 10px; text-align: left; }}
      th {{ background: #f5f7f9; }}
      section {{ margin-top: 28px; }}
      .note {{ border-left: 4px solid #3858e9; padding-left: 14px; color: #333; }}
    </style>
  </head>
  <body>
    <h1>Drug Discovery Research Assistant Evaluation</h1>
    <p class="note">
      Gates Foundation AI Fellows India technical assignment. Path: Option B - Critique & Rebuild. Endpoints:
      <code>POST /chat</code>, <code>POST /v1/chat/completions</code> (CeRAI LOCAL-compatible).
    </p>
    <section>
      <h2>System</h2>
      <p>LLM-powered drug discovery assistant ({llm_on}) with curated RAG snippets and explicit safety routing.</p>
      <p>Evaluation pipeline: <strong>{tool}</strong></p>
    </section>
    <section>
      <h2>Latest Results</h2>
      <p>Main suite: <strong>{passed}/{total}</strong> passed; average score <strong>{avg}</strong>.</p>
      <p>Held-out benchmark: <strong>{bench_passed}/{bench_total}</strong> passed; average score <strong>{bench_avg}</strong>.</p>
      <p><a href="/results/analytics.html">View evaluation analytics</a></p>
      <table>
        <thead><tr><th>Category</th><th>Passed</th><th>Avg score</th></tr></thead>
        <tbody>{rows or "<tr><td colspan='3'>Run evaluation to populate results.</td></tr>"}</tbody>
      </table>
    </section>
    <section>
      <h2>Endpoint Contract</h2>
      <pre>POST /chat
{{ "message": "What is target identification in drug discovery?" }}

POST /v1/chat/completions  (OpenAI-compatible, for CeRAI LOCAL provider)</pre>
    </section>
    <section>
      <h2>Limitations</h2>
      <p>Passing this suite does not certify production biomedical correctness. Expert review and CeRAI metric coverage remain required.</p>
    </section>
  </body>
</html>"""


def _extract_user_message(messages: list[object]) -> str:
    user_parts: list[str] = []
    for item in messages:
        if not isinstance(item, dict):
            continue
        if item.get("role") == "user":
            content = item.get("content", "")
            if isinstance(content, str):
                user_parts.append(content)
    return "\n".join(user_parts).strip()


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

    def _send_file(self, status: int, content_type: str, path: Path) -> None:
        body = path.read_bytes()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict[str, object]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        return json.loads(raw_body.decode("utf-8") or "{}")

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/health":
            self._send_json(200, {"status": "ok", **llm_status()})
        elif path == "/":
            self._send_html(200, _render_index())
        elif path in STATIC_RESULTS and STATIC_RESULTS[path][1].exists():
            content_type, file_path = STATIC_RESULTS[path]
            self._send_file(200, content_type, file_path)
        elif path == "/chat":
            query = parse_qs(parsed.query)
            message = query.get("message", [""])[0]
            if message:
                self._send_json(200, {"response": answer(message)})
            else:
                self._send_json(
                    200,
                    {
                        "usage": 'POST /chat with {"message":"..."} or GET /chat?message=...',
                    },
                )
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            payload = self._read_json_body()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid json"})
            return

        if path == "/chat":
            message = payload.get("message")
            if not isinstance(message, str):
                self._send_json(400, {"error": "message must be a string"})
                return
            self._send_json(200, {"response": answer(message)})
            return

        if path == "/v1/chat/completions":
            messages = payload.get("messages", [])
            if not isinstance(messages, list):
                self._send_json(400, {"error": "messages must be a list"})
                return
            user_message = _extract_user_message(messages)
            if not user_message:
                self._send_json(400, {"error": "no user message found"})
                return
            text = answer(user_message)
            model = payload.get("model") if isinstance(payload.get("model"), str) else "drug-discovery-assistant"
            now = int(time.time())
            self._send_json(
                200,
                {
                    "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
                    "object": "chat.completion",
                    "created": now,
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": text},
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                },
            )
            return

        self._send_json(404, {"error": "not found"})

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    port = int(environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving on http://0.0.0.0:{port} (llm={'on' if llm_available() else 'off'})")
    server.serve_forever()


if __name__ == "__main__":
    main()
