"""
Official CeRAI Docker pipeline: import → execute plans → analyze → export JSON.

Prerequisites:
  - Docker Desktop running
  - Drug-discovery server on host:8000 (python server.py)
  - GROQ_API_KEY in drug-discovery-ai-eval/.env (target LLM)
  - Optional: OLLAMA_URL or GPU_URL in AIEvaluationTool/.env for metric analysis

Writes: results/cerai_official_run.json
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
CERAI_ROOT = Path(os.getenv("CERAI_ROOT", ROOT.parent / "AIEvaluationTool"))
OUTPUT = ROOT / "results" / "cerai_official_run.json"

# CeRAI test plan names (from evaluation/cerai_plans_subset.json)
PLANS_TO_RUN = [
    "Drug_Discovery_Safety",  # Guardrails_and_Safety (T3)
    "Drug_Discovery_Language",  # Language_Support (T4)
    "Drug_Discovery_Responsible_AI",  # Responsible_AI (T1)
]


def _run(cmd: list[str], cwd: Path, timeout: int = 3600) -> subprocess.CompletedProcess[str]:
    print(f"\n>>> {' '.join(cmd)}")
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _docker_compose(*args: str) -> subprocess.CompletedProcess[str]:
    return _run(["docker", "compose", *args], CERAI_ROOT)


def _docker_backend(*args: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        "docker",
        "compose",
        "run",
        "--rm",
        "--no-deps",
        "-w",
        "/app",
        "app-backend",
        *args,
    ]
    return _run(cmd, CERAI_ROOT)


def _sync_files() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "export_cerai_datapoints.py")], check=True, cwd=ROOT)
    shutil.copy2(ROOT / "evaluation" / "cerai_datapoints.json", CERAI_ROOT / "data" / "drug_discovery_datapoints.json")
    shutil.copy2(ROOT / "evaluation" / "cerai_plans_subset.json", CERAI_ROOT / "data" / "drug_discovery_plans.json")
    shutil.copy2(CERAI_ROOT / "config.drug_discovery.json", CERAI_ROOT / "config.json")


def _wait_health(url: str, attempts: int = 30) -> bool:
    for _ in range(attempts):
        try:
            with urlopen(url, timeout=3) as resp:
                if resp.status == 200:
                    return True
        except (URLError, TimeoutError, OSError):
            pass
        time.sleep(2)
    return False


def _parse_plan_ids(stdout: str) -> dict[str, int]:
    """Parse rich table lines: plan_id | plan_name | ..."""
    plans: dict[str, int] = {}
    for line in stdout.splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2 and parts[0].isdigit():
            plans[parts[1]] = int(parts[0])
    return plans


def _parse_run_names(stdout: str) -> list[str]:
    names: list[str] = []
    for line in stdout.splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2 and parts[0].isdigit() and parts[1] not in ("Name", "Run ID"):
            names.append(parts[1])
    return names


def _export_report_json(run_name: str) -> dict | None:
    proc = _docker_backend(
        "python",
        "src/app/response_analyzer/report.py",
        "--config",
        "config.json",
        "--run-name",
        run_name,
        "--get-report",
        "--force",
    )
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout)
        return None
    # Report may be written under data/reports — collect stdout JSON if present
    match = re.search(r"\{[\s\S]*\}", proc.stdout)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {"run_name": run_name, "report_stdout": proc.stdout[-4000:]}


def main() -> None:
    if not CERAI_ROOT.exists():
        print(f"CeRAI root missing: {CERAI_ROOT}")
        sys.exit(1)

    _sync_files()

    target_health = os.getenv("TARGET_HEALTH_URL", "http://127.0.0.1:8000/health")
    if not _wait_health(target_health):
        print(f"Start the assistant first: python server.py (health check failed: {target_health})")
        sys.exit(1)

    print("Building CeRAI Docker images (first run may take several minutes)...")
    build = _docker_compose("build", timeout=1800)
    if build.returncode != 0:
        print(build.stderr or build.stdout)
        sys.exit(build.returncode)

    up = _docker_compose(
        "up",
        "-d",
        "db",
        "selenium-browser",
        "interface-manager",
        "auth-service",
        "tdms-backend",
        "app-backend",
    )
    if up.returncode != 0:
        print(up.stderr or up.stdout)
        sys.exit(up.returncode)

    time.sleep(15)

    imp = _docker_backend("python", "src/app/importer/main.py", "--config", "config.json")
    print(imp.stdout)
    if imp.returncode != 0:
        print(imp.stderr)
        sys.exit(imp.returncode)

    plans_proc = _docker_backend(
        "python",
        "src/app/testcase_executor/main.py",
        "--config",
        "config.json",
        "--get-plans",
    )
    plan_ids = _parse_plan_ids(plans_proc.stdout)
    print("Plans:", plan_ids)

    runs_meta: list[dict] = []
    for plan_name in PLANS_TO_RUN:
        plan_id = plan_ids.get(plan_name)
        if plan_id is None:
            print(f"Warning: plan not found: {plan_name}")
            continue
        run_name = f"drug-discovery-{plan_name.lower().replace('_', '-')}-{int(time.time())}"
        exec_proc = _docker_backend(
            "python",
            "src/app/testcase_executor/main.py",
            "--config",
            "config.json",
            "--testplan-id",
            str(plan_id),
            "--max-testcases",
            "50",
            "--run-name",
            run_name,
            "--execute",
        )
        print(exec_proc.stdout[-2000:] if exec_proc.stdout else "")
        if exec_proc.returncode != 0:
            print(exec_proc.stderr)
            runs_meta.append({"plan": plan_name, "plan_id": plan_id, "run_name": run_name, "execute_error": exec_proc.stderr[-2000:]})
            continue

        analyze = _docker_backend(
            "python",
            "src/app/response_analyzer/analyze.py",
            "--config",
            "config.json",
            "--run-name",
            run_name,
            "--force",
        )
        report = _export_report_json(run_name)
        runs_meta.append(
            {
                "plan": plan_name,
                "plan_id": plan_id,
                "run_name": run_name,
                "execute_ok": exec_proc.returncode == 0,
                "analyze_ok": analyze.returncode == 0,
                "analyze_tail": (analyze.stdout or analyze.stderr or "")[-1500:],
                "report": report,
            }
        )

    all_runs = _docker_backend(
        "python",
        "src/app/testcase_executor/main.py",
        "--config",
        "config.json",
        "--get-runs",
    )

    payload = {
        "evaluation_layer": "official",
        "tool": "CeRAI AIEvaluationTool v2.0 (Docker)",
        "cerai_repository": str(CERAI_ROOT),
        "target_url": "http://host.docker.internal:8000/v1/chat/completions",
        "plans_executed": PLANS_TO_RUN,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runs": runs_meta,
        "all_runs_table": all_runs.stdout,
        "note": (
            "Metric analysis uses CeRAI strategies (LLM-as-judge via OLLAMA_URL, toxicity models, etc.). "
            "Set OLLAMA_URL or GPU_URL in AIEvaluationTool/.env if analyze step fails."
        ),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
