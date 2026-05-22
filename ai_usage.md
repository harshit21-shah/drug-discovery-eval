# AI Use Disclosure

## Tools Used

- AI assistants for brainstorming evaluation dimensions, documentation structure, code organization, and edge-case identification.
- The repository supports Groq/OpenAI APIs for the conversational endpoint and LLM-as-judge scoring, but no API key is committed.
- CeRAI AI Evaluation Tool (IIT Madras) was used as the mandated framework reference: documentation review, datapoint export, Docker validation, and setup-blocker documentation.

## Human Review

I manually reviewed and revised:

- All 35 test prompts and rubric criteria
- The 50-item benchmark
- Safety routing rules and system prompt
- Results interpretation and limitation statements in `report.md`
- CeRAI mapping, datapoint export schema, and issue drafts

## Course Corrections

- Replaced the initial single deterministic endpoint with an LLM-capable endpoint plus curated retrieval and safety routing.
- Added LLM-as-judge hooks so evaluation can move beyond keyword-only checks when credentials are configured.
- Documented CeRAI progress and blockers instead of claiming a completed official run.
- Added `/v1/chat/completions` for CeRAI LOCAL/OpenAI-compatible integration.
- Removed local `.env` containing a secret-like key and added `SECURITY.md`.

AI was used as a drafting and implementation assistant, not as a substitute for technical judgment about biomedical safety and evaluation design.

