# Evaluation Report: Drug Discovery Research Assistant

## 1. System Evaluated

I evaluated a lightweight conversational endpoint called **Drug Discovery Research Assistant**. The endpoint is designed to answer drug-discovery research questions, explain biomedical concepts, structure evidence for target prioritization, and avoid patient-specific medical advice.

I chose this system because the fellowship introduction I received was for the **AI for Drug Discovery** project. Evaluating a domain-relevant assistant makes the assignment more representative of the judgment required in that project area than evaluating a generic chatbot.

## 2. Evaluation Question

The central question was:

> Can a drug-discovery-oriented conversational assistant provide useful, cautious, and accessible responses under realistic biomedical conversation scenarios?

## 3. Test Suite

The test suite contains 23 prompts across 7 categories:

1. Biomedical Factuality
2. Uncertainty Handling
3. Safety and Overclaiming
4. Evidence Reasoning
5. Prompt Injection Resistance
6. User Experience
7. Multilingual and Accessibility

The multilingual/accessibility category was included because the India Country Office context makes language accessibility part of responsible deployment. These prompts are not intended to certify full multilingual biomedical ability. They probe whether the assistant can preserve clarity, caution, and basic scientific correctness when asked to explain drug discovery concepts in simple English or Hindi.

## 4. Evaluation Method

The assignment asks candidates to install, assess, and build on the CeRAI AI Evaluation Tool. I reviewed CeRAI's documentation and mapped my test categories to its responsible AI, safety, language support, conversational quality, and task performance metric areas.

I also included a small local evaluator that sends the same prompts to the endpoint and checks responses against transparent `must_include` and `must_avoid` criteria. This local evaluator is not a replacement for CeRAI. It is a reproducible sanity check that makes the test design and endpoint behavior easy to inspect.

## 5. Key Findings

The endpoint is strongest where the desired behavior is well-scoped:

- It explains core concepts such as target identification, biomarkers, and ADMET in accessible language.
- It avoids patient-specific dosage or treatment recommendations.
- It responds cautiously to overbroad biomedical claims.
- It rejects prompt-injection attempts that ask it to ignore safety constraints.
- It can provide simple-English and limited Hindi explanations for selected biomedical concepts.

The evaluation also shows important limitations:

- Automated metrics can check consistency, coverage, refusal behavior, and surface-level quality, but they cannot fully validate scientific correctness.
- Drug discovery claims require expert review, evidence provenance, and ideally links to curated biomedical sources.
- Multilingual biomedical evaluation should involve native-language review, not only automated scoring.
- A deterministic endpoint is useful for reproducible testing, but it does not represent the full risk profile of a generative production LLM.

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
    "Multilingual and Accessibility"
  ],
  "total_test_cases": 23,
  "main_conclusion": "Automated conversational evaluation provides useful repeatable signal for safety, uncertainty, and usability, but biomedical correctness and deployment readiness still require expert human review."
}
```

## 7. Conclusion

This evaluation suggests that a domain-specific test suite is essential for biomedical conversational AI. A generic chatbot benchmark would miss important failure modes such as overclaiming, unsafe clinical advice, weak uncertainty handling, and poor accessibility for India-context users.

For a real Gates Foundation deployment, I would extend this work by adding literature-grounded retrieval, expert-reviewed expected answers, native-language review, more adversarial biomedical prompts, and a clearer distinction between research support and clinical decision support.

