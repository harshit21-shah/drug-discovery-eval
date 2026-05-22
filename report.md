# Evaluation Report: Drug Discovery Research Assistant

## 1. Path Chosen

**Option B - Critique & Rebuild.**

I began with Option A, but the official CeRAI execution path did not complete in the available environment. Rather than substitute a custom runner while still claiming a full Option A result, I reframed the submission as Option B: document the CeRAI setup blocker, critique the gaps that matter for biomedical evaluation, and build a minimal CeRAI-aligned alternative that can run reproducibly.

## 2. System Evaluated

**Drug Discovery Research Assistant** is a conversational REST endpoint for biomedical research support in the AI for Drug Discovery fellowship context.

| Property | Detail |
| --- | --- |
| Chat endpoint | `POST /chat` with `{"message": "..."}` |
| CeRAI-compatible endpoint | `POST /v1/chat/completions` in OpenAI chat-completions format |
| Model backend | Groq or OpenAI LLM when `GROQ_API_KEY` or `OPENAI_API_KEY` is supplied |
| Retrieval | Curated drug-discovery snippets in `app/knowledge_base.py` |
| Safety | Pattern-based pre-generation routing for clinical advice, self-experimentation, prompt injection, fake citations, unsupported certainty, and false premises |
| Fallback | Limited deterministic safety/retrieval fallback when no API key is configured |

This is not a production clinical system. It is an evaluation target and reproducibility harness for responsible biomedical AI testing.

## 3. CeRAI Engagement and Blocker

Repository reviewed: https://github.com/cerai-iitm/AIEvaluationTool

| Step | Status |
| --- | --- |
| Documentation review | Completed |
| Category mapping | `evaluation/cerai_mapping.md` |
| Datapoint export | 35 cases exported to `evaluation/cerai_datapoints.json` |
| Docker Compose validation | `docker compose config --quiet` passes |
| MariaDB service | `docker compose up -d db` starts `aiet-db` |
| Official local importer | Attempted via `scripts/bootstrap_cerai.py` |
| Full official metric run | Not completed |

The official local importer reached CeRAI source code but hit a dependency conflict: `googletrans==4.0.0rc1` expects an old `httpx/httpcore` stack, while CeRAI's Interface Manager imports the modern `OpenAI` SDK class. Upgrading OpenAI fixes `from openai import OpenAI` but breaks `googletrans` with:

```text
AttributeError: module 'httpcore' has no attribute 'SyncHTTPTransport'
```

This is documented in `evaluation/cerai_attempt.md`. I filed detailed issues on the CeRAI repository for the setup blocker, biomedical metric gap, and citation-verification gap:

- https://github.com/cerai-iitm/AIEvaluationTool/issues/181
- https://github.com/cerai-iitm/AIEvaluationTool/issues/182
- https://github.com/cerai-iitm/AIEvaluationTool/issues/183

Live endpoint health was verified on 2026-05-22:

```text
https://drug-discovery-eval.onrender.com/health -> status: ok, provider: groq
```

## 4. Rebuild: CeRAI-Aligned Alternative

The rebuild includes:

- A live conversational endpoint with `/chat` and OpenAI-compatible `/v1/chat/completions`.
- A 35-case domain evaluation suite covering factuality, uncertainty, safety, evidence reasoning, prompt injection, UX, multilingual accessibility, and hallucination.
- A separate 50-item held-out benchmark covering target identification, biomarkers, ADMET, clinical trials, drug repurposing, and safety/hallucination.
- A CeRAI-style runner in `scripts/run_cerai_evaluation.py` with transparent keyword checks and optional LLM-as-judge scoring when credentials are configured.
- Failure-analysis and analytics artifacts under `results/`.

## 5. Evaluation Integrity

The test suite and endpoint were co-designed by the same author, so circularity is a real risk. I mitigated it in three ways:

1. Safety routing uses category-level pattern matching, not verbatim test-prompt literals.
2. The 50-item benchmark was held out from endpoint tuning and is run separately from the 35-case suite.
3. The report separates no-secret fallback results from the intended LLM-backed run; a full model-backed run would reduce reliance on pre-generation routing and should be treated as the stronger evaluation.

The benchmark result is intentionally lower than the main suite result. That is useful evidence: it shows the fallback endpoint generalizes only partially and should not be overclaimed.

## 6. Verified Results

**Run date:** 2026-05-22  
**Provider:** none configured  
**Judge:** skipped  
**Environment:** no-secret fallback mode with `DISABLE_LLM=1`

### Model-Backed Subset

A smaller model-backed subset was also run with Groq and LLM-as-judge enabled. I used a 12-case subset to avoid provider rate limits while still covering factuality, uncertainty, safety, evidence reasoning, prompt injection, UX, multilingual accessibility, and hallucination.

| Metric | Value |
| --- | ---: |
| Total tests | 12 |
| Combined pass | 12/12 |
| Average combined score | 0.888 |
| Provider | Groq |
| Model/Judge | `llama-3.1-8b-instant` |

Result file: `results/model_backed_results.json`

Limitation: the model-backed subset used the same provider family for endpoint generation and LLM-as-judge scoring. This demonstrates model-backed evaluation, but it does not control for judge bias as strongly as an independent judge model would.

### Main 35-Case Suite

| Metric | Value |
| --- | ---: |
| Total tests | 35 |
| Keyword/rubric pass | 27/35 |
| Average rubric score | 0.914 |

| Category | Passed | Avg score |
| --- | ---: | ---: |
| Biomedical Factuality | 4/5 | 0.900 |
| Uncertainty Handling | 2/4 | 0.812 |
| Safety and Overclaiming | 4/4 | 1.000 |
| Evidence Reasoning | 3/4 | 0.938 |
| Prompt Injection Resistance | 4/4 | 1.000 |
| User Experience | 2/4 | 0.875 |
| Multilingual and Accessibility | 4/6 | 0.833 |
| Hallucination and Consistency | 4/4 | 1.000 |

### Held-Out 50-Item Benchmark

| Metric | Value |
| --- | ---: |
| Total tests | 50 |
| Keyword/rubric pass | 20/50 |
| Average rubric score | 0.745 |

| Category | Passed | Avg score |
| --- | ---: | ---: |
| Target Identification | 2/8 | 0.688 |
| Biomarkers | 4/8 | 0.750 |
| ADMET | 2/8 | 0.656 |
| Clinical Trials | 3/8 | 0.750 |
| Drug Repurposing | 3/8 | 0.781 |
| Safety and Hallucination | 6/10 | 0.825 |

## 7. Failure Pattern

The main failure mode is not unsafe refusal failure. It is retrieval and fallback mismatch on open-ended generation tasks. Before the retrieval fix, a biomarker prompt could retrieve docking/ADMET snippets because the retriever used summary-token overlap more than title-level matching. I changed retrieval scoring to weight title tokens, exact keyword phrases, and category-level matches more strongly.

Remaining failures show the limit of a small curated fallback: it can refuse unsafe or fabricated requests reliably, but it cannot always synthesize complete explanations for broader biomedical concepts. A real LLM-backed run should be used for final evaluation.

## 8. Critique of CeRAI for Biomedical Use

CeRAI is useful because it structures endpoint evaluation, datapoints, plans, and metric execution. For drug discovery, I would extend it in three ways:

| Limitation | Draft issue | Filed issue URL |
| --- | --- | --- |
| Local importer dependency conflict between `googletrans`, `httpx/httpcore`, and the modern OpenAI SDK | `evaluation/issues/001_dependency_conflict_googletrans_openai.md` | https://github.com/cerai-iitm/AIEvaluationTool/issues/181 |
| Need biomedical scientific-validity rubrics for target evidence, ADMET, biomarker validation, clinical-trial reasoning, and translational risk | `evaluation/issues/002_biomedical_metric_gap.md` | https://github.com/cerai-iitm/AIEvaluationTool/issues/182 |
| Need citation verification so biomedical claims can be checked against verifiable references rather than judged only by fluency | `evaluation/issues/003_citation_verification.md` | https://github.com/cerai-iitm/AIEvaluationTool/issues/183 |

I would also add domain failure analysis that distinguishes hallucination, irrelevant retrieval, unsupported certainty, and safe refusal.

## 9. Machine-Readable Summary

```json
{
  "path_chosen": "Option B - Critique & Rebuild",
  "system": "Drug Discovery Research Assistant",
  "endpoint_type": "LLM + RAG + safety routing when configured; deterministic fallback otherwise",
  "official_cerai_status": "partial; compose and DB verified, importer blocked by dependency conflict",
  "main_suite_tests": 35,
  "main_suite_pass_count": 27,
  "main_suite_average_score": 0.914,
  "held_out_benchmark_tests": 50,
  "held_out_benchmark_pass_count": 20,
  "held_out_benchmark_average_score": 0.745,
  "model_backed_subset_tests": 12,
  "model_backed_subset_pass_count": 12,
  "model_backed_subset_average_score": 0.888,
  "model_backed_provider": "groq",
  "results_files": [
    "results/cerai_evaluation_results.json",
    "results/benchmark_evaluation_results.json",
    "results/model_backed_results.json"
  ]
}
```

## 10. Conclusion

This submission does not claim a completed official CeRAI metric run. It shows the attempted CeRAI path, documents a concrete blocker, critiques the missing biomedical evaluation capabilities, and rebuilds a reproducible evaluation harness around a drug-discovery conversational endpoint.
