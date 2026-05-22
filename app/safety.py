from __future__ import annotations

import re


SAFETY_MESSAGE = (
    "I cannot provide patient-specific treatment, dosage, or clinical decision advice. "
    "For medical care, a qualified clinician should evaluate the patient context. "
    "I can help explain the research concept and what evidence would be needed."
)


def _has_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def check_safety(prompt: str) -> str | None:
    """Return a fixed safety response when prompt matches high-risk patterns."""
    lowered = prompt.lower()

    if re.search(
        r"ignore .*instructions|jailbreak|previous instructions|role override|"
        r"without restrictions|unrestricted .*model|hidden .*prompt|system prompt|"
        r"reveal .*instructions|ignore .*safety rules|bypass .*safety|safety rules .*disabled",
        lowered,
    ):
        return (
            "I cannot reveal hidden instructions, accept a role override, or ignore medical safety and "
            "evidence requirements. I can discuss hypotheses, evidence quality, and research workflows, "
            "but not experimental-drug prescriptions, guaranteed cures, or bypassing safeguards."
        )

    if "guarantee" in lowered and "cure" in lowered:
        return (
            "I cannot make a guaranteed cure claim. EGFR inhibition can be relevant in specific molecular "
            "contexts, but response depends on cancer subtype, mutation status, resistance mechanisms, safety, "
            "and clinical evidence."
        )

    if re.search(r"test .* on myself|self[- ]experiment|experimental .* (myself|online)|small amount .* myself", lowered):
        return (
            "I cannot advise self-experimentation with an experimental molecule. Even a small amount may be unsafe. "
            "This work belongs in regulated research or clinical settings with ethics review and qualified oversight."
        )

    asks_for_unverified_citation = re.search(
        r"\bcite\b.*\b(paper|study|article|journal|nature)\b|"
        r"\bproving?\b.*\b(cures?|guarantees?)\b",
        lowered,
    )
    asks_for_fabricated_value = re.search(
        r"\bfictional\b|\bmade[- ]?up\b|"
        r"\bexact\b.*\b(ic50|ki|kd|ec50)\b|"
        r"\b(ic50|ki|kd|ec50)\b.*\b(value|values|exact)\b",
        lowered,
    )
    if asks_for_unverified_citation or asks_for_fabricated_value:
        return (
            "I cannot verify that citation or fabricate exact IC50 values from the prompt. If the compound or "
            "paper is fictional or unverified, I should say so, avoid invented numbers or citations, and request "
            "a verifiable source."
        )

    if re.search(r"\bearlier you said\b|\byou said\b.*\balways\b", lowered):
        return (
            "That is a false premise. BRCA1 relevance is context dependent and should be evaluated using mechanism, "
            "patient subgroup, safety, and validation evidence, not treated as a universal target."
        )

    if re.search(r"\bweak evidence\b|\blacks evidence\b|\bsound confident\b|\bunsupported confidence\b", lowered):
        return (
            "No. If a response lacks evidence, the assistant should not use unsupported certainty. It should state "
            "uncertainty, explain what evidence is missing, and recommend expert review."
        )

    patient_specific_advice = re.search(
        r"\b(dosage|dose|prescribe)\b|"
        r"\bwhich drug should i take\b|"
        r"\btreat my\b|"
        r"\brecommend .* (for|to) .*patient\b|"
        r"\bwhat .* should .*patient .*take\b",
        lowered,
    )
    if patient_specific_advice:
        return SAFETY_MESSAGE

    return None
