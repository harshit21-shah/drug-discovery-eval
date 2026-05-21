# Drug Discovery Research Assistant Evaluation

Technical assignment submission for the Gates Foundation AI Fellows India 2026 process.

## Path Chosen

I chose **Option A - Evaluate & Report**. Since I was being considered for the **AI for Drug Discovery** project, I evaluated a domain-relevant conversational endpoint rather than a generic chatbot. The endpoint is a lightweight drug-discovery research assistant, and the test suite probes whether it gives useful, cautious, and accessible responses in biomedical research scenarios.

## What Is Evaluated

The endpoint exposes a simple chat API:

```http
POST /chat
Content-Type: application/json

{ "message": "What is target identification in drug discovery?" }
```

Response:

```json
{
  "response": "..."
}
```

The assistant is deterministic and rule-based by design. It uses explicit keyword and safety routing rather than an LLM or RAG backend. This makes the evaluation reproducible and keeps the focus on test design, evaluation interpretation, and responsible AI behavior rather than on stochastic LLM variation. It also limits what the results mean: passing this suite does not prove production biomedical AI capability.

## Test Suite Design

The suite contains 23 prompts across 7 categories:

| Category | Why it matters |
| --- | --- |
| Biomedical Factuality | Checks core drug discovery concept correctness. |
| Uncertainty Handling | Tests whether the assistant avoids overconfident biomedical claims. |
| Safety and Overclaiming | Checks refusal behavior for clinical, dosage, and cure claims. |
| Evidence Reasoning | Tests whether the assistant can structure target-prioritization evidence. |
| Prompt Injection Resistance | Tests whether safety constraints survive adversarial instructions. |
| User Experience | Checks clarity for non-specialist stakeholders such as program officers. |
| Multilingual and Accessibility | Probes simple-English and Hindi explanations for India-context deployment. |
| Hallucination and Consistency | Checks fabricated citations, fictional values, false premises, and unsupported confidence. |

The test suite is available at:

```text
evaluation/test_suite.json
```

## Local Setup

Create and activate a Python environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Start the zero-dependency endpoint:

```bash
python server.py
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Try one chat call:

```bash
curl -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"What evidence would you need before prioritizing a gene target?\"}"
```

## Local Evaluation Runner

Run the transparent local rubric evaluator:

```bash
python scripts/run_local_evaluation.py
```

It writes:

```text
results/local_evaluation_results.json
```

The local runner is included as a reproducibility aid. It is not presented as a replacement for CeRAI; it makes the selected prompts, endpoint behavior, and basic rubric checks inspectable.

## Deployment

This app has no database, API keys, or model-service dependency. It can be deployed as a small Python web service.

### Railway

```bash
railway login
railway init
railway up
```

Railway uses `railway.json` and starts:

```bash
python server.py
```

### Render

Create a new Render web service from this public GitHub repository. Render can use `render.yaml`, or configure manually:

```text
Build command: pip install -r requirements.txt
Start command: python server.py
Health check path: /health
```

### Hugging Face Spaces

Create a new Space with:

```text
SDK: Docker
Visibility: Public
```

Then upload or connect this repository. The included `Dockerfile` starts the zero-dependency HTTP app on `${PORT:-7860}`, which matches Hugging Face Spaces' default web port.

## CeRAI Usage

The CeRAI AI Evaluation Tool repository is:

```text
https://github.com/cerai-iitm/AIEvaluationTool
```

CeRAI v2.0 uses a TDMS/database/importer workflow plus Interface Manager execution. The mapping from this repository's test suite to CeRAI concepts is documented in:

```text
evaluation/cerai_mapping.md
```

I attempted the official CeRAI setup locally and documented the outcome in:

```text
evaluation/cerai_attempt.md
```

The Docker Compose configuration validated after creating `.env`, but the full CeRAI Docker run was blocked because Docker Desktop's Linux engine was not reachable in the local environment. The direct Python CLI path also stopped on missing CeRAI dependencies. I included these details so the limitation is explicit rather than implied.

At a high level:

1. Install and start CeRAI using its Docker or CLI setup.
2. Register this endpoint as an API target.
3. Convert `evaluation/test_suite.json` into CeRAI datapoints.
4. Run relevant CeRAI plans for responsible AI, safety, conversational quality, language support, and task performance.
5. Export raw results and place them under `results/`.
6. Update `report.md` with the final interpretation.

## Findings Summary

The local evaluation run completed **35 test cases**, with **26/35 passing** and an average rubric score of **0.857**. The current endpoint performs best on concept explanation, evidence framing, and safety refusals because those behaviors are explicitly designed. The expanded suite intentionally surfaces gaps in hallucination handling, hidden-instruction requests, self-experimentation prompts, and some accessibility wording. It should not be interpreted as a production biomedical assistant or as a scientifically complete drug discovery system.

Key expected findings:

- Automated evaluation is useful for repeatable checks of safety, refusal behavior, and coverage.
- Biomedical factuality cannot be fully certified by lexical or generic LLM-as-judge metrics.
- Hindi/simple-English accessibility should be evaluated with native speakers and domain reviewers before deployment.
- Human expert review remains necessary for scientific validity in drug discovery.

## AI Use Disclosure

See `ai_usage.md`.

## Repository Structure

```text
app/
  assistant.py
  main.py
server.py
evaluation/
  test_suite.json
  cerai_mapping.md
scripts/
  run_local_evaluation.py
results/
  sample_results.json
README.md
report.md
ai_usage.md
submission_note.md
```
