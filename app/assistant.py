from __future__ import annotations

from app.knowledge_base import retrieval_answer
from app.llm_client import chat_completion, llm_available
from app.safety import check_safety


def answer(prompt: str) -> str:
    """Return a drug-discovery research response using LLM + RAG, with safety routing."""
    normalized = prompt.strip()
    if not normalized:
        return "Please provide a drug discovery or biomedical research question."

    safety = check_safety(normalized)
    if safety:
        return safety

    context = retrieval_answer(normalized)
    extra_system = None
    if context:
        extra_system = f"Retrieved context (curated, not live literature):\n{context}"

    if llm_available():
        try:
            return chat_completion(normalized, extra_system=extra_system)
        except Exception as exc:
            return (
                f"I encountered an error calling the language model ({exc}). "
                "Please verify GROQ_API_KEY or OPENAI_API_KEY in .env and retry."
            )

    return _deterministic_fallback(normalized, context)


def _deterministic_fallback(prompt: str, context: str | None) -> str:
    """Offline fallback when no API key is configured."""
    lowered = prompt.lower()

    if "admet" in lowered:
        return (
            "ADMET describes absorption, distribution, metabolism, excretion, and toxicity—how a compound "
            "behaves in the body. It is an early filter, not proof of clinical benefit."
        )
    if "target identification" in lowered:
        return (
            "Target identification finds a disease-relevant molecule or pathway; strong hypotheses combine "
            "genetics, disease biology, expression, functional data, and validation evidence."
        )
    if context:
        return context

    return (
        "LLM mode is unavailable (set GROQ_API_KEY or OPENAI_API_KEY in .env). "
        "I can still explain that biomedical answers need evidence, uncertainty, and expert review."
    )
