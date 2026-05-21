from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUITE = ROOT / "evaluation" / "test_suite.json"
DEFAULT_OUTPUT = ROOT / "results" / "local_evaluation_results.json"


def _contains_all(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def _contains_none(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return all(term.lower() not in lowered for term in terms)


def score_response(response: str, must_include: list[str], must_avoid: list[str]) -> dict[str, Any]:
    include_hits = [term for term in must_include if term.lower() in response.lower()]
    avoid_hits = [term for term in must_avoid if term.lower() in response.lower()]
    include_score = len(include_hits) / max(len(must_include), 1)
    avoid_score = 1.0 if not avoid_hits else 0.0
    score = round((0.75 * include_score) + (0.25 * avoid_score), 3)
    return {
        "score": score,
        "include_hits": include_hits,
        "avoid_hits": avoid_hits,
        "passed": _contains_all(response, must_include) and _contains_none(response, must_avoid),
    }


def run(endpoint: str, suite_path: Path, output_path: Path) -> dict[str, Any]:
    suite = json.loads(suite_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []

    for category in suite["categories"]:
        for test_case in category["test_cases"]:
            payload = {suite["endpoint_contract"]["request_json_key"]: test_case["prompt"]}
            try:
                request = Request(
                    endpoint,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urlopen(request, timeout=20) as http_response:
                    body = json.loads(http_response.read().decode("utf-8"))
                response_text = body[suite["endpoint_contract"]["response_json_key"]]
                error = None
            except (HTTPError, URLError, TimeoutError, KeyError, json.JSONDecodeError) as exc:
                response_text = ""
                error = str(exc)

            rubric = score_response(
                response=response_text,
                must_include=test_case.get("must_include", []),
                must_avoid=test_case.get("must_avoid", []),
            )
            results.append(
                {
                    "id": test_case["id"],
                    "category": category["name"],
                    "prompt": test_case["prompt"],
                    "expected_behavior": test_case["expected_behavior"],
                    "response": response_text,
                    "error": error,
                    **rubric,
                }
            )

    category_summary = {}
    for category in suite["categories"]:
        category_results = [item for item in results if item["category"] == category["name"]]
        category_summary[category["name"]] = {
            "test_count": len(category_results),
            "pass_count": sum(1 for item in category_results if item["passed"]),
            "average_score": round(
                sum(item["score"] for item in category_results) / max(len(category_results), 1),
                3,
            ),
        }

    summary = {
        "suite_name": suite["suite_name"],
        "endpoint": endpoint,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_tests": len(results),
        "pass_count": sum(1 for item in results if item["passed"]),
        "average_score": round(sum(item["score"] for item in results) / max(len(results), 1), 3),
        "category_summary": category_summary,
        "results": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a local rubric evaluation against the chat endpoint.")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000/chat")
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    summary = run(args.endpoint, args.suite, args.output)
    print(json.dumps({k: summary[k] for k in ["suite_name", "total_tests", "pass_count", "average_score"]}, indent=2))


if __name__ == "__main__":
    main()
