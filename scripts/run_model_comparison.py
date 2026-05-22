"""Run the same benchmark against multiple configured LLM models.

This script is intentionally provider-agnostic for OpenAI-compatible APIs.
Examples:
  $env:GROQ_API_KEY="..."
  python scripts/run_model_comparison.py --models llama-3.3-70b-versatile,llama-3.1-8b-instant

It writes `results/model_comparison.json` and `results/model_comparison.csv`.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON = ROOT / "results" / "model_comparison.json"
OUTPUT_CSV = ROOT / "results" / "model_comparison.csv"


def run_for_model(model: str, endpoint: str, skip_judge: bool) -> dict:
    env = os.environ.copy()
    if env.get("GROQ_API_KEY"):
        env["GROQ_MODEL"] = model
        env["GROQ_JUDGE_MODEL"] = env.get("GROQ_JUDGE_MODEL", model)
    elif env.get("OPENAI_API_KEY"):
        env["OPENAI_MODEL"] = model
        env["OPENAI_JUDGE_MODEL"] = env.get("OPENAI_JUDGE_MODEL", model)
    else:
        raise RuntimeError("Set GROQ_API_KEY or OPENAI_API_KEY before running model comparison.")

    output = ROOT / "results" / f"model_{model.replace('/', '_').replace(':', '_')}.json"
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "run_cerai_evaluation.py"),
        "--endpoint",
        endpoint,
        "--output",
        str(output),
    ]
    if skip_judge:
        cmd.append("--skip-judge")
    subprocess.run(cmd, cwd=ROOT, env=env, check=True)
    return json.loads(output.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare multiple LLM models on the drug discovery suite.")
    parser.add_argument("--models", required=True, help="Comma-separated model ids.")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000/chat")
    parser.add_argument("--skip-judge", action="store_true")
    args = parser.parse_args()

    rows = []
    payload = {"models": []}
    for model in [m.strip() for m in args.models.split(",") if m.strip()]:
        result = run_for_model(model, args.endpoint, args.skip_judge)
        row = {
            "model": model,
            "total_tests": result["total_tests"],
            "pass_count": result["pass_count"],
            "average_score": result["average_combined_score"],
        }
        for category, stats in result["category_summary"].items():
            row[f"{category}_pass_rate"] = round(stats["pass_count"] / max(stats["test_count"], 1), 3)
        rows.append(row)
        payload["models"].append({"model": model, "summary": row, "result_file": f"results/model_{model}.json"})

    OUTPUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUTPUT_JSON} and {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

