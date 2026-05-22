from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeEntry:
    title: str
    keywords: tuple[str, ...]
    summary: str


KNOWLEDGE_BASE: tuple[KnowledgeEntry, ...] = (
    KnowledgeEntry(
        title="Target identification and validation",
        keywords=("target", "identification", "validation", "disease", "biology", "druggable", "genetics"),
        summary=(
            "Target identification proposes a disease-relevant molecule or pathway for therapeutic modulation. Target validation "
            "then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, "
            "functional evidence, safety assessment, and reproducible experiments."
        ),
    ),
    KnowledgeEntry(
        title="Biomarkers",
        keywords=("biomarker", "biomarkers", "her2", "msi", "prognostic", "predictive", "stratification"),
        summary=(
            "A biomarker is a measurable biological signal related to disease state, prognosis, or treatment response. "
            "Predictive biomarkers indicate likely response to a therapy, prognostic biomarkers relate to outcome, and "
            "deployment requires analytical validation, clinical relevance, population applicability, and safe decision use."
        ),
    ),
    KnowledgeEntry(
        title="ADMET",
        keywords=("admet", "absorption", "distribution", "metabolism", "excretion", "toxicity", "potency"),
        summary=(
            "ADMET evaluates absorption, distribution, metabolism, excretion, and toxicity. It helps decide whether a compound "
            "can reach the right tissue, remain active long enough, be cleared safely, avoid harmful effects, and remain viable "
            "for development rather than optimizing only for potency."
        ),
    ),
    KnowledgeEntry(
        title="Docking and experimental validation",
        keywords=("docking", "binding", "compound", "patients", "clinical"),
        summary=(
            "A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. "
            "It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim."
        ),
    ),
    KnowledgeEntry(
        title="Assay reproducibility",
        keywords=("assay", "reproducibility", "program officer", "decision", "risk"),
        summary=(
            "Assay reproducibility matters because repeated experiments should point to the same conclusion. Weak reproducibility "
            "creates decision risk: teams may fund or scale a target hypothesis that fails when tested by another lab or partner."
        ),
    ),
    KnowledgeEntry(
        title="Clinical trials",
        keywords=("clinical", "trial", "phase", "randomization", "surrogate", "consent", "patient"),
        summary=(
            "Clinical trials evaluate interventions in humans. Phase I emphasizes safety and dose, Phase II examines preliminary "
            "efficacy and safety, randomization reduces bias in comparisons, surrogate endpoints are indirect measures that need "
            "validation, and patient-specific trial-drug decisions require clinician oversight and informed consent."
        ),
    ),
    KnowledgeEntry(
        title="Drug repurposing",
        keywords=("repurposing", "off-label", "knowledge graph", "literature mining", "existing drug"),
        summary=(
            "Drug repurposing investigates whether an existing drug can help a new disease or indication. It can be faster when "
            "safety, pharmacology, and manufacturing data exist, but AI-generated hypotheses still require mechanism support, "
            "exposure checks, experimental validation, clinical feasibility, and expert review."
        ),
    ),
    KnowledgeEntry(
        title="Hallucination control",
        keywords=("citation", "fictional", "ic50", "false premise", "confidence", "unsupported"),
        summary=(
            "When evidence is missing, an assistant should say it cannot verify the claim, avoid fabricated citations or exact values, "
            "correct false premises, and preserve uncertainty rather than sounding confident to speed up decisions."
        ),
    ),
)


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def retrieve(prompt: str, limit: int = 2) -> list[KnowledgeEntry]:
    lowered = prompt.lower()
    prompt_tokens = _tokens(prompt)
    scored: list[tuple[int, KnowledgeEntry]] = []
    for entry in KNOWLEDGE_BASE:
        title = entry.title.lower()
        title_tokens = _tokens(entry.title)
        keyword_hits = sum(1 for keyword in entry.keywords if keyword in lowered)
        title_token_hits = len(prompt_tokens.intersection(title_tokens))
        summary_token_hits = len(prompt_tokens.intersection(_tokens(entry.summary)))

        score = (keyword_hits * 5) + (title_token_hits * 4) + summary_token_hits
        if title in lowered:
            score += 8
        for keyword in entry.keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", lowered):
                score += 2
        if score:
            scored.append((score, entry))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [entry for _, entry in scored[:limit]]


def retrieval_answer(prompt: str) -> str | None:
    entries = retrieve(prompt)
    if not entries:
        return None
    evidence = " ".join(entry.summary for entry in entries)
    return (
        f"Using the curated evaluation knowledge base: {evidence} "
        "This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert."
    )
