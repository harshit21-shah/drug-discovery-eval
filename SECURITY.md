# Security Notes

- Do not commit `.env` files or API keys.
- `.env` is ignored by `.gitignore`; use `.env.example` as the template.
- If any API key was ever exposed outside the local machine, revoke it immediately and create a new key.
- The repository supports `GROQ_API_KEY` and `OPENAI_API_KEY`, but neither should be present in source control, screenshots, ZIP files, or issue reports.

