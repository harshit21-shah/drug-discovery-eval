# Model-Backed Run Status

Completed.

Result file:

```text
results/model_backed_results.json
```

Summary:

| Dataset | Provider | Passed | Average score |
| --- | --- | ---: | ---: |
| 12-case model-backed subset | Groq | 12/12 | 0.888 |

The subset covers biomedical factuality, uncertainty, safety, evidence reasoning, prompt injection, UX, multilingual accessibility, and hallucination. A subset was used to avoid provider rate limits while still demonstrating that the endpoint can be evaluated with a real model and LLM-as-judge scoring.
