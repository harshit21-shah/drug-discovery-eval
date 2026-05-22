# Issue: CeRAI setup blocked by backend dependency install and local importer dependency conflict

## Problem

I attempted to run CeRAI for a conversational AI evaluation assignment. The repository cloned successfully, Docker Compose configuration validates, and the MariaDB service starts. However, the full Docker stack does not reach a usable UI/API state, and the local importer path also hits a Python dependency conflict.

### Docker path

Running the full stack fails while building backend services:

```text
target tdms-backend: failed to solve:
pip install --no-cache-dir -r /tmp/requirements.txt
did not complete successfully
exit code: 2
```

### Local importer path

When running the CeRAI importer locally for the drug-discovery datapoints, the importer eventually imports:

```text
src/lib/interface_manager/client.py
```

which expects:

```python
from openai import OpenAI
```

However, installing the local dependency path that includes `googletrans==4.0.0rc1` pulls `httpx==0.13.3`. A modern OpenAI SDK requires a newer `httpx/httpcore` stack. Upgrading OpenAI then breaks `googletrans` with:

```text
AttributeError: module 'httpcore' has no attribute 'SyncHTTPTransport'
```

## Steps To Reproduce

1. Clone CeRAI.
2. Run `docker compose config --quiet`; observe that config validation passes.
3. Run `docker compose up -d db`; observe that the MariaDB container becomes healthy.
4. Run `docker compose up -d selenium-browser interface-manager auth-service tdms-backend app-backend app-front-end tdms-frontend nginx`.
5. Observe backend build failure during `pip install --no-cache-dir -r /tmp/requirements.txt`.
6. For the local path, export datapoints and run the importer/bootstrap script.
7. Observe importer dependency failure around OpenAI/httpx/googletrans compatibility.

## Impact

This blocks both the full Docker path and the local importer path, making it difficult to evaluate a conversational endpoint reproducibly from a clean environment.

## Suggested Fix

Pin a known-good Docker dependency set for backend builds and separate optional translation dependencies from importer/interface dependencies. Alternatively, replace `googletrans==4.0.0rc1` with a maintained translation package compatible with modern `httpx`.
