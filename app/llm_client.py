from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI

from app.prompts import SYSTEM_PROMPT

load_dotenv()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class LLMSettings:
    provider: str  # "groq" | "openai"
    api_key: str
    base_url: str | None
    model: str
    judge_model: str


def get_llm_settings() -> LLMSettings | None:
    if os.getenv("DISABLE_LLM", "").strip() == "1":
        return None

    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    if groq_key:
        model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip()
        judge = os.getenv("GROQ_JUDGE_MODEL", model).strip()
        return LLMSettings(
            provider="groq",
            api_key=groq_key,
            base_url=os.getenv("GROQ_BASE_URL", GROQ_BASE_URL).strip(),
            model=model,
            judge_model=judge,
        )

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        model = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip()
        judge = os.getenv("OPENAI_JUDGE_MODEL", model).strip()
        return LLMSettings(
            provider="openai",
            api_key=openai_key,
            base_url=None,
            model=model,
            judge_model=judge,
        )

    return None


@lru_cache(maxsize=1)
def _client() -> OpenAI | None:
    settings = get_llm_settings()
    if settings is None:
        return None
    if settings.base_url:
        return OpenAI(api_key=settings.api_key, base_url=settings.base_url)
    return OpenAI(api_key=settings.api_key)


def llm_available() -> bool:
    return _client() is not None


def llm_status() -> dict[str, str | bool]:
    settings = get_llm_settings()
    if settings is None:
        return {
            "llm_enabled": False,
            "provider": "none",
            "model": "",
            "hint": "Set GROQ_API_KEY or OPENAI_API_KEY in .env",
        }
    return {
        "llm_enabled": True,
        "provider": settings.provider,
        "model": settings.model,
        "judge_model": settings.judge_model,
    }


def chat_completion(
    user_message: str,
    *,
    extra_system: str | None = None,
    model: str | None = None,
    temperature: float = 0.2,
) -> str:
    client = _client()
    settings = get_llm_settings()
    if client is None or settings is None:
        raise RuntimeError(
            "No LLM API key configured. Set GROQ_API_KEY (recommended) or OPENAI_API_KEY in .env"
        )

    system_parts = [SYSTEM_PROMPT]
    if extra_system:
        system_parts.append(extra_system)

    response = client.chat.completions.create(
        model=model or settings.model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "\n\n".join(system_parts)},
            {"role": "user", "content": user_message},
        ],
    )
    return (response.choices[0].message.content or "").strip()


def judge_completion(prompt: str) -> str:
    """Run LLM-as-judge; uses judge_model from settings."""
    client = _client()
    settings = get_llm_settings()
    if client is None or settings is None:
        raise RuntimeError("No LLM API key configured for judge.")

    kwargs: dict[str, object] = {
        "model": settings.judge_model,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = client.chat.completions.create(
            **kwargs,
            response_format={"type": "json_object"},
        )
    except Exception:
        response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or "{}"
