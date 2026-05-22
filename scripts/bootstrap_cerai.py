"""Copy drug-discovery datapoints into CeRAI and run importer (sqlite, no Docker)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERAI_ROOT = Path(os.getenv("CERAI_ROOT", ROOT.parent / "AIEvaluationTool"))


def main() -> None:
    if not CERAI_ROOT.exists():
        print(f"CeRAI root not found: {CERAI_ROOT}")
        sys.exit(1)

    src_datapoints = ROOT / "evaluation" / "cerai_datapoints.json"
    src_plans = ROOT / "evaluation" / "cerai_plans_subset.json"
    src_config = ROOT / "evaluation" / "cerai_config.json"

    shutil.copy2(src_datapoints, CERAI_ROOT / "data" / "drug_discovery_datapoints.json")
    shutil.copy2(src_plans, CERAI_ROOT / "data" / "drug_discovery_plans.json")

    config = json.loads(src_config.read_text(encoding="utf-8"))
    config["files"]["testcases"] = "data/drug_discovery_datapoints.json"
    config["files"]["plans"] = "data/drug_discovery_plans.json"
    out_config = CERAI_ROOT / "config.drug_discovery.json"
    out_config.write_text(json.dumps(config, indent=2), encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(CERAI_ROOT / "src")

    print("Installing CeRAI importer dependencies (subset)...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "rich",
            "sqlalchemy",
            "sqlalchemy-utils",
            "mariadb",
            "pydantic",
            "randomname",
            "googletrans==4.0.0rc1",
            "python-iso639",
            "python-jose[cryptography]",
            "passlib[bcrypt]",
            "pydantic-settings",
            "openai",
        ],
        check=False,
    )

    print("Forcing modern OpenAI SDK required by CeRAI InterfaceManagerClient...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "openai>=1.40.0", "httpx>=0.27.0"],
        check=False,
    )

    print(f"Running CeRAI importer with {out_config}")
    result = subprocess.run(
        [sys.executable, str(CERAI_ROOT / "src" / "app" / "importer" / "main.py"), "--config", str(out_config)],
        cwd=CERAI_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)
    print("CeRAI datapoints imported into sqlite:", config["db"]["file"])


if __name__ == "__main__":
    main()
