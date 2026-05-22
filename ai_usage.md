# AI Use Disclosure

## Tools Used

- AI assistants for brainstorming evaluation dimensions, documentation structure, code organization, and edge-case identification.
- Groq/OpenAI API support for the conversational endpoint and LLM-as-judge scoring, when a local key is configured.
- CeRAI AI Evaluation Tool as the mandated framework reference: documentation review, datapoint export, Docker validation, setup-blocker documentation, and critique.

## Human Review

I manually reviewed and revised:

- All 35 test prompts and rubric criteria
- The 50-item held-out benchmark
- Safety routing rules and system prompt
- Results interpretation and limitation statements in `report.md`
- CeRAI mapping, datapoint export schema, setup notes, and issue drafts

## Course Corrections

- AI initially suggested evaluating a generic chatbot. I redirected the project to a drug-discovery assistant because the fellowship project area is AI for Drug Discovery.
- AI-generated safety rules initially matched medical terms too broadly and risked flagging legitimate research questions such as "What is a drug target?" as clinical advice. I narrowed the triggers to patient-specific treatment, dosing, self-experimentation, prompt injection, fabricated citations, false premises, and unsupported-confidence requests.
- AI-generated hallucination checks initially used exact prompt strings. I replaced those with category-level pattern matching so the safety router is not tuned to verbatim test prompts.
- AI-generated multilingual examples initially used formal academic Hindi. I simplified the framing toward Hindi/Hinglish explanations a non-technical stakeholder or program officer might ask for.
- I documented CeRAI progress and blockers instead of claiming a completed official CeRAI run. Because the official path remained blocked, I reframed the submission as Option B: critique and rebuild.
- I removed a local `.env` containing a secret-like value, added `.env.example`, and added `SECURITY.md`.

AI was used as a drafting and implementation assistant, not as a substitute for technical judgment about biomedical safety, evaluation integrity, or limitation reporting.
