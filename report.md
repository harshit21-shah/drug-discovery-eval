# Evaluation Report: Drug Discovery Research Assistant

## 1. System Evaluated

**Drug Discovery Research Assistant** is a conversational REST endpoint for biomedical research support in the AI for Drug Discovery fellowship context.

| Property | Detail |
| --- | --- |
| Chat endpoint | `POST /chat` with `{"message": "..."}` |
| CeRAI-compatible endpoint | `POST /v1/chat/completions` in OpenAI chat-completions format |
| Model backend | Groq or OpenAI LLM when `GROQ_API_KEY` or `OPENAI_API_KEY` is supplied |
| Retrieval | Curated drug-discovery snippets in `app/knowledge_base.py` |
| Safety | Pre-generation routing for clinical advice, self-experimentation, jailbreaks, fake citations, and false premises |
| Fallback | Limited deterministic safety/retrieval fallback when no API key is configured |

The assistant is **not** a production clinical system. It demonstrates how a domain-specific conversational endpoint should be evaluated before deployment.

## 2. Evaluation Question

> Can a drug-discovery-oriented LLM assistant provide useful, cautious, and accessible responses under realistic biomedical scenarios, including India-context language and safety edge cases?

## 3. Test Suite

The main suite contains **35 prompts across 8 categories**:

1. Biomedical Factuality
2. Uncertainty Handling
3. Safety and Overclaiming
4. Evidence Reasoning
5. Prompt Injection Resistance
6. User Experience
7. Multilingual and Accessibility
8. Hallucination and Consistency

I also added `benchmark/drug_discovery_benchmark.json`, a separate **50-item reusable benchmark** covering target identification, biomarkers, ADMET, clinical trials, drug repurposing, and safety/hallucination.

## 4. CeRAI Tool Engagement

Repository: https://github.com/cerai-iitm/AIEvaluationTool

| Step | Status |
| --- | --- |
| Documentation review | Completed |
| Category mapping | `evaluation/cerai_mapping.md` |
| Datapoint export | 35 cases exported to `evaluation/cerai_datapoints.json` |
| Docker Compose validation | `docker compose config --quiet` passes |
| MariaDB service | `docker compose up -d db` starts `aiet-db` |
| Official local importer | Attempted via `scripts/bootstrap_cerai.py` |
| Full official metric run | Not completed |

The official local importer reached CeRAI source code but was blocked by a dependency conflict: `googletrans==4.0.0rc1` pins an old `httpx/httpcore` stack, while CeRAI's Interface Manager imports the modern `OpenAI` SDK class. Upgrading OpenAI fixes `from openai import OpenAI` but breaks `googletrans` with:

```text
AttributeError: module 'httpcore' has no attribute 'SyncHTTPTransport'
```

I documented this in `evaluation/cerai_attempt.md` and added issue drafts under `evaluation/issues/`.

## 5. Evaluation Method

The repo includes a CeRAI-aligned runner:

```bash
python scripts/run_cerai_evaluation.py --endpoint http://127.0.0.1:8000/chat
```

It:

1. Sends the suite prompts to the endpoint.
2. Applies a transparent keyword rubric using `must_include` and `must_avoid`.
3. Applies LLM-as-judge scoring when `GROQ_API_KEY` or `OPENAI_API_KEY` is configured.
4. Writes `results/cerai_evaluation_results.json`.

Because the committed environment contains no API key, the verified result below is the **no-secret fallback run**. It is intentionally not described as a full LLM or full official CeRAI result.

## 6. Verified Results

**Run date:** 2026-05-22  
**Provider:** none configured  
**Judge:** skipped  
**Results:** `results/cerai_evaluation_results.json`

| Metric | Value |
| --- | ---: |
| Total tests | 35 |
| Keyword/rubric pass | 20/35 |
| Average rubric score | 0.818 |

| Category | Passed | Avg score |
| --- | ---: | ---: |
| Biomedical Factuality | 3/5 | 0.8 |
| Uncertainty Handling | 1/4 | 0.625 |
| Safety and Overclaiming | 4/4 | 1.0 |
| Evidence Reasoning | 1/4 | 0.719 |
| Prompt Injection Resistance | 4/4 | 1.0 |
| User Experience | 1/4 | 0.75 |
| Multilingual and Accessibility | 2/6 | 0.708 |
| Hallucination and Consistency | 4/4 | 1.0 |

## 7. Interpretation

- Safety, jailbreak resistance, and hallucination controls are strong even without an API key because they are handled by pre-generation routing.
- Uncertainty, evidence reasoning, and UX are weak in fallback mode because a real LLM is not configured.
- This is the central methodological lesson: a fallback endpoint is useful for resilience, but proper AI evaluation requires enabling the LLM backend and judge.
- The full model-backed run is reproducible by setting `GROQ_API_KEY` or `OPENAI_API_KEY` and rerunning `scripts/run_cerai_evaluation.py`.

## 8. Failure Analysis and Visuals

Generated artifacts:

- `results/failure_analysis.md`
- `results/pass_rate_by_category.svg`
- `results/analytics.html`

These summarize where the fallback endpoint fails and make the category-level results easier to inspect.

## 9. Machine-Readable Summary

```json
{
  "path_chosen": "Option A - Evaluate & Report",
  "system": "Drug Discovery Research Assistant",
  "endpoint_type": "LLM + RAG + safety routing when configured; deterministic fallback otherwise",
  "official_cerai_status": "partial; compose and DB verified, importer blocked by dependency conflict",
  "test_cases": 35,
  "benchmark_items": 50,
  "verified_no_secret_pass_count": 20,
  "verified_no_secret_average_score": 0.818,
  "results_file": "results/cerai_evaluation_results.json"
}
```

## 10. Conclusion

This submission improves on a simple chatbot evaluation by adding a domain-specific benchmark, an LLM-capable endpoint, CeRAI-compatible datapoints, an OpenAI-compatible endpoint for CeRAI LOCAL integration, LLM-as-judge hooks, failure analysis, and issue drafts for tool limitations.

The remaining gap is a full official CeRAI run with all services and model credentials available. That gap is documented rather than hidden.
