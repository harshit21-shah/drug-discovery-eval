# Issue: CeRAI local importer dependency conflict between googletrans and modern OpenAI SDK

## Problem

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
2. Export drug-discovery datapoints.
3. Run `python scripts/bootstrap_cerai.py`.
4. Observe importer dependency failure.

## Impact

This blocks local non-Docker importer execution and makes it hard to use CeRAI from a clean Python environment.

## Suggested Fix

Separate optional translation dependencies from importer/interface dependencies, or replace `googletrans==4.0.0rc1` with a maintained translation package compatible with modern `httpx`.

