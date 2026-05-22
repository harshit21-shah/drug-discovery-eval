# Drug Discovery Research Assistant Evaluation

Technical assignment submission for the Gates Foundation AI Fellows India 2026 process.

## Path Chosen

**Option B - Critique & Rebuild.**

I started with the intended CeRAI evaluation path, but official execution was blocked by a reproducible dependency conflict. Instead of hiding that gap, this repo documents the CeRAI blocker, critiques the tool for biomedical use, and provides a minimal CeRAI-aligned evaluation harness for a drug-discovery conversational endpoint.

## What This Repo Contains

| Artifact | Path |
| --- | --- |
| Canonical live HTTP endpoint | `server.py` |
| LLM/RAG assistant | `app/assistant.py`, `app/llm_client.py`, `app/knowledge_base.py` |
| Pattern-based safety router | `app/safety.py` |
| 35-case evaluation suite | `evaluation/test_suite.json` |
| 50-item held-out benchmark | `benchmark/drug_discovery_benchmark.json` |
| CeRAI datapoints | `evaluation/cerai_datapoints.json` |
| CeRAI mapping and setup notes | `evaluation/cerai_mapping.md`, `evaluation/cerai_attempt.md` |
| CeRAI issue drafts | `evaluation/issues/` |
| Evaluation runner | `scripts/run_cerai_evaluation.py` |
| Analysis generator | `scripts/generate_analysis_artifacts.py` |
| Model comparison runner | `scripts/run_model_comparison.py` |
| Results and analysis | `results/cerai_evaluation_results.json`, `results/benchmark_evaluation_results.json`, `results/failure_analysis.md`, `results/analytics.html` |

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

Create `.env` from `.env.example` and add either:

```text
GROQ_API_KEY=...
```

or:

```text
OPENAI_API_KEY=...
```

If no key is set, the server uses a limited deterministic safety/retrieval fallback. That fallback is useful for health checks and reproducibility, but it is not a substitute for evaluating a real LLM.

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
python scripts/run_cerai_evaluation.py --endpoint http://127.0.0.1:8000/chat --skip-judge
```

Run the held-out benchmark:

```bash
python scripts/run_cerai_evaluation.py ^
  --endpoint http://127.0.0.1:8000/chat ^
  --skip-judge ^
  --suite benchmark/drug_discovery_benchmark.json ^
  --output results/benchmark_evaluation_results.json
```

When `GROQ_API_KEY` or `OPENAI_API_KEY` is configured, omit `--skip-judge` to enable LLM-as-judge scoring.

## Model-Backed Run Status

No model-backed result is committed because no active API key is present in this repo or runtime, and a previously exposed secret-like key was intentionally not reused. See:

```text
results/model_backed_run_status.md
```

## Verified No-Secret Results

Because no API key is committed, the verified results are fallback runs:

| Dataset | Passed | Average score |
| --- | ---: | ---: |
| Main 35-case suite | 27/35 | 0.914 |
| Held-out 50-item benchmark | 20/50 | 0.745 |

The benchmark is intentionally reported separately because it is a harder held-out check and helps reveal overfitting/circularity risk.

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

## Model Comparison

```bash
python scripts/run_model_comparison.py --models llama-3.3-70b-versatile,llama-3.1-8b-instant
```

Outputs:

```text
results/model_comparison.json
results/model_comparison.csv
```

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
