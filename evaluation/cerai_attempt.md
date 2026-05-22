# CeRAI Setup Attempt

## Repository

```text
https://github.com/cerai-iitm/AIEvaluationTool
```

Local clone used:

```text
../AIEvaluationTool
```

## Verified Steps

| Step | Command | Result |
| --- | --- | --- |
| Compose validation | `docker compose config --quiet` | Passed |
| MariaDB service | `docker compose up -d db` | `aiet-db` running |
| Full Docker stack | `docker compose up -d selenium-browser interface-manager auth-service tdms-backend app-backend app-front-end tdms-frontend nginx` | Backend image build fails during dependency installation |
| Datapoint export | `python scripts/export_cerai_datapoints.py` | 35 cases exported |
| Local importer bootstrap | `python scripts/bootstrap_cerai.py` | Reaches official CeRAI importer, then fails on dependency conflict |

## Current Official-Tool Blockers

### Docker backend build

The full Docker stack does not reach a running UI/API state. It fails while building backend targets:

```text
target tdms-backend: failed to solve:
pip install --no-cache-dir -r /tmp/requirements.txt
did not complete successfully
exit code: 2
```

Only the database container was confirmed healthy:

```text
aiet-db   Up / healthy
```

### Local importer dependency conflict

The local importer path imports CeRAI's Interface Manager client:

```python
from openai import OpenAI
```

That requires a modern OpenAI SDK. However, CeRAI also depends on:

```text
googletrans==4.0.0rc1
```

which pins an old `httpx/httpcore` stack. The bootstrap process exposes the conflict:

1. With old OpenAI SDK:

```text
ImportError: cannot import name 'OpenAI' from 'openai'
```

2. After forcing modern OpenAI and `httpx>=0.27`:

```text
AttributeError: module 'httpcore' has no attribute 'SyncHTTPTransport'
```

This blocks clean local importer execution without isolating dependency groups or using the full Docker app runtime.

## Issue Drafts

I documented concrete issue drafts:

```text
evaluation/issues/001_dependency_conflict_googletrans_openai.md
evaluation/issues/002_biomedical_metric_gap.md
evaluation/issues/003_citation_verification.md
```

These are ready to file against CeRAI if repository issue permissions are available.

## How This Submission Still Builds On CeRAI

- Exports CeRAI-style datapoints: `evaluation/cerai_datapoints.json`
- Maps categories to CeRAI metric areas: `evaluation/cerai_mapping.md`
- Exposes OpenAI-compatible `/v1/chat/completions` for CeRAI LOCAL provider style usage
- Provides a CeRAI-aligned runner: `scripts/run_cerai_evaluation.py`
- Documents official-tool setup and dependency blockers

## Next Step For Full Official Execution

Run the full Docker stack in an environment where all CeRAI services can build and run:

```powershell
cd ..\AIEvaluationTool
docker compose build
docker compose up -d db selenium-browser interface-manager auth-service tdms-backend app-backend
docker exec -it app-backend bash
python src/app/importer/main.py --config config.json
python src/app/testcase_executor/main.py --config config.json --get-plans
```

Then execute the exported drug-discovery plans and copy raw CeRAI outputs into `results/`.
