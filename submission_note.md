# Submission Note

Repository URL: https://github.com/harshit21-shah/drug-discovery-eval

Live endpoint URL: https://drug-discovery-eval.onrender.com/

I chose **Option B: Critique & Rebuild**. I initially attempted the intended CeRAI evaluation path for a drug-discovery conversational endpoint, but the official local importer was blocked by a concrete dependency conflict between `googletrans==4.0.0rc1` and the modern OpenAI SDK expected by CeRAI's Interface Manager. Instead of presenting a custom runner as a completed official CeRAI run, I documented the blocker, created issue drafts for the CeRAI repository, critiqued the missing biomedical evaluation capabilities, and built a minimal CeRAI-aligned alternative. The repo includes a live drug-discovery assistant endpoint, OpenAI-compatible `/v1/chat/completions`, CeRAI datapoint exports, a 35-case evaluation suite, a separate 50-item held-out benchmark, failure analysis, and optional LLM-as-judge scoring when `GROQ_API_KEY` or `OPENAI_API_KEY` is configured.

AI use: I used AI tools to brainstorm evaluation dimensions, draft documentation, implement scripts, and identify edge cases, but I manually reviewed the biomedical safety criteria, CeRAI mapping, failure analysis, and limitation statements. AI initially suggested a generic chatbot as the evaluation target; I redirected it to a drug-discovery assistant because the fellowship project area is AI for Drug Discovery. AI-generated safety rules initially matched broad medical terms too aggressively, so I narrowed them to patient-specific treatment, self-experimentation, prompt injection, fabricated citations, and unsupported-confidence patterns. AI-generated multilingual prompts were also revised toward simpler Hindi/Hinglish appropriate for non-technical stakeholders.
