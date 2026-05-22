# Model-Backed Run Status

No model-backed result is committed yet.

Reason: this repository and runtime do not contain an active `GROQ_API_KEY` or `OPENAI_API_KEY`. A previously exposed secret-like key was not reused because that would be unsafe and should be rotated.

To generate the model-backed result after configuring a fresh private key:

```bash
python server.py
python scripts/run_cerai_evaluation.py --endpoint http://127.0.0.1:8000/chat --output results/model_backed_subset_results.json
```

The runner will use LLM-as-judge scoring automatically when a key is available and `--skip-judge` is omitted.
