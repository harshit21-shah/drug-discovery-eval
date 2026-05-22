"""Generate failure notes, simple SVG bars, and an HTML summary from evaluation JSON."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_failure_analysis(data: dict[str, Any], output: Path, source: Path) -> None:
    failures = [r for r in data["results"] if not r.get("passed")]
    lines = [
        "# Failure Analysis",
        "",
        f"Evaluation file: `{source.as_posix()}`",
        "",
        f"Total failures: {len(failures)} / {data['total_tests']}",
        "",
    ]
    for result in failures:
        reason = str(result.get("llm_judge_reason") or "")
        if reason == "skipped":
            reason = (
                "keyword_only: LLM judge was skipped for this no-secret fallback run; "
                "the response missed one or more required rubric terms or triggered an avoid term."
            )
        elif not reason:
            reason = "fallback_mismatch: response did not satisfy the transparent keyword rubric."
        response = str(result.get("response", "")).replace("\n", " ")
        if len(response) > 700:
            response = response[:697] + "..."
        lines.extend(
            [
                f"## {result['id']} - {result['category']}",
                "",
                f"**Prompt:** {result['prompt']}",
                "",
                f"**Expected:** {result.get('expected_behavior', '')}",
                "",
                f"**Response:** {response}",
                "",
                f"**Keyword hits:** include={result.get('include_hits', [])} avoid={result.get('avoid_hits', [])}",
                "",
                f"**Reason:** {reason}",
                "",
            ]
        )
    output.write_text("\n".join(lines), encoding="utf-8")


def _write_svg(data: dict[str, Any], output: Path) -> None:
    rows = list(data.get("category_summary", {}).items())
    width = 820
    height = 72 + (len(rows) * 30)
    bar_width = 430
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="20" y="30" font-family="Arial" font-size="18" font-weight="bold">Drug Discovery Evaluation: Pass Rate by Category</text>',
    ]
    for idx, (name, stats) in enumerate(rows):
        y = 62 + (idx * 30)
        total = max(int(stats.get("test_count", 0)), 1)
        passed = int(stats.get("pass_count", 0))
        rate = passed / total
        fill_width = int(bar_width * rate)
        svg.extend(
            [
                f'<text x="20" y="{y + 14}" font-family="Arial" font-size="12">{html.escape(name)}</text>',
                f'<rect x="260" y="{y}" width="{bar_width}" height="18" fill="#edf2f7"/>',
                f'<rect x="260" y="{y}" width="{fill_width}" height="18" fill="#3867d6"/>',
                f'<text x="704" y="{y + 14}" font-family="Arial" font-size="12">{passed}/{total} ({rate:.0%})</text>',
            ]
        )
    svg.append("</svg>")
    output.write_text("\n".join(svg), encoding="utf-8")


def _write_html(data: dict[str, Any], output: Path, svg_name: str, failure_name: str) -> None:
    passed = data["pass_count"]
    total = data["total_tests"]
    avg = data["average_combined_score"]
    output.write_text(
        (
            "<!doctype html><html><head><meta charset=\"utf-8\"><title>Evaluation Analytics</title></head>"
            "<body><h1>Drug Discovery Evaluation Analytics</h1>"
            f"<p>Total: {passed}/{total} passed; average score {avg}.</p>"
            f"<img src=\"{html.escape(svg_name)}\" alt=\"Pass rate by category\">"
            f"<p>See <a href=\"{html.escape(failure_name)}\">{html.escape(failure_name)}</a> for detailed failures.</p>"
            "</body></html>"
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--failure-output", type=Path, required=True)
    parser.add_argument("--svg-output", type=Path, required=True)
    parser.add_argument("--html-output", type=Path)
    args = parser.parse_args()

    data = _load(args.input)
    args.failure_output.parent.mkdir(parents=True, exist_ok=True)
    _write_failure_analysis(data, args.failure_output, args.input)
    _write_svg(data, args.svg_output)
    if args.html_output:
        _write_html(data, args.html_output, args.svg_output.name, args.failure_output.name)


if __name__ == "__main__":
    main()
