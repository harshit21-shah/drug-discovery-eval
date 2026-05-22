# Evaluation Report: Drug Discovery Research Assistant

## 1. System Evaluated

I evaluated a lightweight conversational endpoint called **Drug Discovery Research Assistant**. The endpoint is designed to answer drug-discovery research questions, explain biomedical concepts, structure evidence for target prioritization, and avoid patient-specific medical advice.

I chose this system because the fellowship introduction I received was for the **AI for Drug Discovery** project. Evaluating a domain-relevant assistant makes the assignment more representative of the judgment required in that project area than evaluating a generic chatbot.

Important implementation note: the assistant endpoint is deterministic and retrieval-aided. It uses explicit safety routing plus a small curated drug-discovery knowledge base rather than a hosted LLM. I made this choice to keep the evaluation target reproducible within the assignment window and to focus the work on evaluation design, endpoint behavior, and interpretation. This also means the results should not be read as evidence that a production generative biomedical assistant is ready for deployment.

## 2. Evaluation Question

The central question was:

> Can a drug-discovery-oriented conversational assistant provide useful, cautious, and accessible responses under realistic biomedical conversation scenarios?

## 3. Test Suite

The test suite contains 35 prompts across 8 categories:

1. Biomedical Factuality
2. Uncertainty Handling
3. Safety and Overclaiming
4. Evidence Reasoning
5. Prompt Injection Resistance
6. User Experience
7. Multilingual and Accessibility
8. Hallucination and Consistency

The multilingual/accessibility category was included because the India Country Office context makes language accessibility part of responsible deployment. These prompts are not intended to certify full multilingual biomedical ability. They probe whether the assistant can preserve clarity, caution, and basic scientific correctness when asked to explain drug discovery concepts in simple English or Hindi.

## 4. Evaluation Method

The assignment asks candidates to install, assess, and build on the CeRAI AI Evaluation Tool. I reviewed CeRAI's documentation and mapped my test categories to its responsible AI, safety, language support, conversational quality, and task performance metric areas.

I also included a small local evaluator that sends the same prompts to the endpoint and checks responses against transparent `must_include` and `must_avoid` criteria. This local evaluator is not a replacement for CeRAI. It is a reproducible sanity check that makes the test design and endpoint behavior easy to inspect.

I attempted to run CeRAI locally. After creating the required `.env`, `docker compose config --quiet` validated the Compose configuration, but `docker compose up -d db selenium-browser interface-manager auth-service tdms-backend app-backend` failed because Docker Desktop's Linux engine was not reachable in the local environment. I also tried the direct Python CLI path, which stopped at a missing dependency (`ModuleNotFoundError: No module named 'rich'`). The exact commands and errors are documented in `evaluation/cerai_attempt.md`.

To make a future CeRAI run easier, I also added `scripts/export_cerai_datapoints.py`, which converts the 35-case suite into `evaluation/cerai_datapoints.json` using a CeRAI-style datapoint schema.

## 5. Key Findings

The local evaluation run completed **35/35 test cases**, with an average rubric score of **1.0**. Category-level results were:

| Category | Passed | Average score |
| --- | ---: | ---: |
| Biomedical Factuality | 5/5 | 1.0 |
| Uncertainty Handling | 4/4 | 1.0 |
| Safety and Overclaiming | 4/4 | 1.0 |
| Evidence Reasoning | 4/4 | 1.0 |
| Prompt Injection Resistance | 4/4 | 1.0 |
| User Experience | 4/4 | 1.0 |
| Multilingual and Accessibility | 6/6 | 1.0 |
| Hallucination and Consistency | 4/4 | 1.0 |

These numbers should be interpreted cautiously. The endpoint is deterministic, and the local rubric checks explicit `must_include` and `must_avoid` criteria. The result shows that the designed endpoint satisfies this test suite; it does not prove general biomedical correctness, robustness to unseen prompts, or production readiness.

The endpoint is strongest where the desired behavior is well-scoped:

- It explains core concepts such as target identification, biomarkers, and ADMET in accessible language.
- It avoids patient-specific dosage or treatment recommendations.
- It responds cautiously to overbroad biomedical claims.
- It rejects prompt-injection attempts that ask it to ignore safety constraints.
- It can provide simple-English and limited Hindi explanations for selected biomedical concepts.

The expanded test suite initially surfaced failures worth addressing:

- Hallucination and consistency tests required explicit handling of fake citations, fictional compound values, false premises, and unsupported confidence.
- One prompt-injection case exposed that hidden-instruction requests require a more specific refusal path.
- One safety case showed that self-experimentation requests need explicit handling.
- One accessibility case showed that "simple English" expectations need clearer response routing.

I addressed these by adding a curated retrieval layer, explicit hallucination/consistency controls, and additional safety routing while preserving the deterministic nature of the endpoint.

The evaluation also shows important limitations:

- Automated metrics can check consistency, coverage, refusal behavior, and surface-level quality, but they cannot fully validate scientific correctness.
- Drug discovery claims require expert review, evidence provenance, and ideally links to curated biomedical sources.
- Multilingual biomedical evaluation should involve native-language review, not only automated scoring.
- A deterministic retrieval-aided endpoint is useful for reproducible testing, but it does not represent the full risk profile of a generative production LLM.

## 6. Machine-Readable Summary

```json
{
  "path_chosen": "Option A - Evaluate & Report",
  "system": "Drug Discovery Research Assistant",
  "domain": "AI for Drug Discovery",
  "test_categories": [
    "Biomedical Factuality",
    "Uncertainty Handling",
    "Safety and Overclaiming",
    "Evidence Reasoning",
    "Prompt Injection Resistance",
    "User Experience",
    "Multilingual and Accessibility",
    "Hallucination and Consistency"
  ],
  "total_test_cases": 35,
  "local_pass_count": 35,
  "local_average_score": 1.0,
  "endpoint_type": "deterministic_retrieval_aided",
  "main_conclusion": "Automated conversational evaluation provides useful repeatable signal for safety, uncertainty, and usability, but biomedical correctness and deployment readiness still require expert human review."
}
```

## 7. Conclusion

This evaluation suggests that a domain-specific test suite is essential for biomedical conversational AI. A generic chatbot benchmark would miss important failure modes such as overclaiming, unsafe clinical advice, weak uncertainty handling, and poor accessibility for India-context users.

For a real Gates Foundation deployment, I would extend this work by adding literature-grounded retrieval, expert-reviewed expected answers, native-language review, more adversarial biomedical prompts, and a clearer distinction between research support and clinical decision support.
