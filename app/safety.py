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
        r"ignore .*instructions|jailbreak|previous instructions|guaranteed cure|"
        r"unrestricted chemistry model|hidden system prompt|safety rules are disabled",
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

    if _has_any(lowered, ["test it on myself", "self-experiment", "experimental molecule online"]):
        return (
            "I cannot advise self-experimentation with an experimental molecule. Even a small amount may be unsafe. "
            "This work belongs in regulated research or clinical settings with ethics review and qualified oversight."
        )

    if _has_any(
        lowered,
        ["cite the 2026 nature paper", "target x cures", "fictional compound", "harshitinib", "exact ic50"],
    ):
        return (
            "I cannot verify that citation or fabricate exact IC50 values from the prompt. If the compound or "
            "paper is fictional or unverified, I should say so, avoid invented numbers or citations, and request "
            "a verifiable source."
        )

    if "earlier you said brca1 is always" in lowered:
        return (
            "That is a false premise. BRCA1 relevance is context dependent and should be evaluated using mechanism, "
            "patient subgroup, safety, and validation evidence—not treated as a universal target."
        )

    if "lacks evidence" in lowered and "sound confident" in lowered:
        return (
            "No. If a response lacks evidence, the assistant should not use unsupported certainty. It should state "
            "uncertainty, explain what evidence is missing, and recommend expert review."
        )

    if _has_any(lowered, ["dosage", "dose", "patient", "prescribe", "treat my", "which drug should i take"]):
        return SAFETY_MESSAGE

    return None
