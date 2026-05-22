# Drug Discovery Research Assistant Evaluation

Technical assignment submission for the Gates Foundation AI Fellows India 2026 process.

## Path Chosen

**Option A - Evaluate & Report**, with partial official CeRAI execution and a CeRAI-aligned fallback runner.

I evaluated a drug-discovery-focused conversational endpoint rather than a generic chatbot because the fellowship introduction was for the **AI for Drug Discovery** project.

## What This Repo Contains

| Artifact | Path |
| --- | --- |
| Live HTTP endpoint | `server.py` |
| LLM/RAG assistant | `app/assistant.py`, `app/llm_client.py`, `app/knowledge_base.py` |
| Safety router | `app/safety.py` |
| 35-case evaluation suite | `evaluation/test_suite.json` |
| 50-item benchmark | `benchmark/drug_discovery_benchmark.json` |
| CeRAI datapoints | `evaluation/cerai_datapoints.json` |
| CeRAI mapping and attempt notes | `evaluation/cerai_mapping.md`, `evaluation/cerai_attempt.md` |
| CeRAI issue drafts | `evaluation/issues/` |
| Evaluation runner | `scripts/run_cerai_evaluation.py` |
| Model comparison runner | `scripts/run_model_comparison.py` |
| Results and analysis | `results/cerai_evaluation_results.json`, `results/failure_analysis.md`, `results/analytics.html` |

## Endpoint

The server exposes:

```text
GET  /health
POST /chat
GET  /chat?message=...
POST /v1/chat/completions
```

`/v1/chat/completions` follows the OpenAI chat-completions shape so CeRAI can call it as a LOCAL/OpenAI-compatible target.

## Model Configuration

No API keys are committed.

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Then add either:

```text
GROQ_API_KEY=...
```

or:

```text
OPENAI_API_KEY=...
```

If no key is set, the server uses a limited deterministic safety/retrieval fallback. That fallback is useful for health checks and safety routing, but it is not a substitute for evaluating a real LLM.

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

Test:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"What is target identification in drug discovery?\"}"
```

## Run Evaluation

With the server running:

```bash
python scripts/run_cerai_evaluation.py --endpoint http://127.0.0.1:8000/chat
```

This writes:

```text
results/cerai_evaluation_results.json
```

When `GROQ_API_KEY` or `OPENAI_API_KEY` is configured, the runner also performs LLM-as-judge scoring.

## Model Comparison

```bash
python scripts/run_model_comparison.py --models llama-3.3-70b-versatile,llama-3.1-8b-instant
```

Outputs:

```text
results/model_comparison.json
results/model_comparison.csv
```

## CeRAI Integration

What was verified:

- CeRAI documentation reviewed.
- `docker compose config --quiet` passes in the CeRAI repo.
- `docker compose up -d db` starts the CeRAI MariaDB container.
- 35 datapoints export to `evaluation/cerai_datapoints.json`.
- Local importer bootstrap reaches official CeRAI code.

Current blocker:

- Official local importer hits a dependency conflict between `googletrans==4.0.0rc1` and the modern OpenAI SDK expected by CeRAI's Interface Manager.

Details:

```text
evaluation/cerai_attempt.md
evaluation/issues/
```

## Verified No-Secret Result

Because no API key is committed, the verified result is a fallback run:

```text
35 tests
20 passed
average score 0.818
```

This is intentionally not represented as a full LLM evaluation. A full model-backed run requires setting `GROQ_API_KEY` or `OPENAI_API_KEY`.

## Deployment

Render/Railway/Hugging Face configs are included:

```text
Dockerfile
render.yaml
railway.json
Procfile
```

Start command:

```bash
python server.py
```

## Security

See `SECURITY.md`. Do not commit `.env` or API keys.
