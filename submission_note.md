# Submission Note For Drew

## Path Choice Paragraph

I chose Option A because I wanted to evaluate a conversational endpoint in the intended spirit of the CeRAI assignment, while aligning the endpoint and test suite with the AI for Drug Discovery project area. I built a drug-discovery research assistant that can run with Groq or OpenAI when an API key is configured, exposes both `/chat` and OpenAI-compatible `/v1/chat/completions` endpoints, and includes curated retrieval plus safety routing for biomedical edge cases. I created a 35-case evaluation suite and a separate 50-item benchmark covering target identification, biomarkers, ADMET, clinical trials, drug repurposing, safety, and hallucination. I attempted official CeRAI integration: Docker Compose validation and the MariaDB service worked, datapoints were exported in CeRAI format, and the local importer reached CeRAI code but was blocked by a concrete dependency conflict documented in the repo. Because of that, I also included a CeRAI-aligned runner with keyword rubric and optional LLM-as-judge scoring.

## AI Use Paragraph

I used AI tools to help brainstorm evaluation dimensions, draft documentation, implement the endpoint and evaluation scripts, and identify conversational edge cases. I manually reviewed the biomedical safety criteria, test prompts, CeRAI mapping, failure analysis, and limitations. No API keys are committed; the model-backed run requires configuring `GROQ_API_KEY` or `OPENAI_API_KEY` locally or in deployment.

## Email Template

Hi Drew,

Thank you for sharing the technical assignment. I chose Option A: Evaluate & Report.

Repository: https://github.com/harshit21-shah/drug-discovery-eval  
Live endpoint: https://drug-discovery-eval.onrender.com/  
Health check: https://drug-discovery-eval.onrender.com/health  
Chat endpoint: https://drug-discovery-eval.onrender.com/chat

I chose Option A because I wanted to evaluate a conversational endpoint in the intended spirit of the CeRAI assignment, while aligning the endpoint and test suite with the AI for Drug Discovery project area. The repo includes a drug-discovery research assistant, CeRAI-compatible datapoints, a 35-case evaluation suite, a 50-item benchmark, issue drafts for CeRAI limitations, failure analysis, and a CeRAI-aligned runner with optional LLM-as-judge scoring.

AI use: I used AI tools to help brainstorm evaluation dimensions, draft documentation, implement the endpoint/evaluation scripts, and identify edge cases. I manually reviewed the biomedical safety criteria, test design, CeRAI mapping, and limitations. No API keys are committed; model-backed evaluation runs when `GROQ_API_KEY` or `OPENAI_API_KEY` is configured.

Best,  
Harshit

