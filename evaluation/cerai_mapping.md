# CeRAI Mapping Notes

This project follows Option A: Evaluate & Report. The assignment endpoint is a REST API target:

- Method: `POST`
- Local URL: `http://127.0.0.1:8000/chat`
- Request body: `{ "message": "<prompt>" }`
- Response field: `response`

The test suite in `evaluation/test_suite.json` maps to CeRAI concepts as follows:

| Project category | Relevant CeRAI test plan or metric area |
| --- | --- |
| Biomedical Factuality | Task Performance Metrics, Truthfulness, Accuracy |
| Uncertainty Handling | Responsible AI, Transparency, Hallucination Rate |
| Safety and Overclaiming | Guardrails and Safety, Privacy and Safety |
| Evidence Reasoning | Conversational Quality, Relevance and Information |
| Prompt Injection Resistance | Privacy and Safety, Jailbreak, Robustness against Adversarial Attacks |
| User Experience | Conversational Quality, Fluency, Dialogue Coherence |
| Multilingual and Accessibility | Language Support, Accuracy per Language, Fluency in Indian Languages |
| Hallucination and Consistency | Hallucination Rate, Truthfulness, Relevance and Information |

CeRAI v2.0 expects test data to be imported into its TDMS/database workflow and executed through the Interface Manager. For a full CeRAI run, convert each `test_case` into the CeRAI datapoint schema with:

- `PROMPT_ID`: test case id
- `SYSTEM_PROMPT`: drug discovery assistant scope and safety behavior
- `PROMPT`: test prompt
- `EXPECTED_OUTPUT`: expected behavior
- `DOMAIN`: healthcare or biomedical research
- `LLM_AS_JUDGE`: either `No` for lexical metrics or a concise judge instruction for responsible-AI metrics

This repository also includes `scripts/run_local_evaluation.py` as a transparent local sanity check. It is not a replacement for CeRAI; it is included to make the selected prompts, endpoint behavior, and interpretation reproducible if the full CeRAI Docker/database workflow is unavailable during review.
