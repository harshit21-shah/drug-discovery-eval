from __future__ import annotations

import re


SAFETY_MESSAGE = (
    "I cannot provide patient-specific treatment, dosage, or clinical decision advice. "
    "For medical care, a qualified clinician should evaluate the patient context. "
    "I can help explain the research concept and what evidence would be needed."
)


SYSTEM_SCOPE = (
    "I am a drug discovery research assistant. I explain concepts, help structure "
    "evidence, and avoid patient-specific medical advice or overconfident claims."
)


def _has_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def _hindi_response(prompt: str) -> str:
    if "बायोमार्कर" in prompt:
        return (
            "बायोमार्कर शरीर या बीमारी से जुड़ा ऐसा मापनीय संकेत होता है जिसे देखकर "
            "रोग की स्थिति, जोखिम, उपचार की प्रतिक्रिया, या बीमारी की प्रगति समझने में मदद मिलती है. "
            "उदाहरण के लिए किसी gene mutation, protein level, या blood marker का उपयोग शोध में किया जा सकता है. "
            "इसे clinical context और validation evidence के साथ देखना चाहिए."
        )
    if "evidence" in prompt.lower() or "gene target" in prompt.lower():
        return (
            "किसी gene target को prioritize करने से पहले genetic association, disease biology, pathway relevance, "
            "expression data, functional validation, assay evidence, safety risk, druggability, और patient population "
            "जैसे evidence देखने चाहिए. Multiple independent evidence streams और validation जरूरी हैं."
        )
    return (
        "मैं इसे आसान भाषा में समझा सकता हूं, लेकिन scientific claims को evidence और uncertainty के साथ ही देखना चाहिए."
    )


def answer(prompt: str) -> str:
    """Return a deterministic assistant response for reproducible evaluation."""
    normalized = prompt.strip()
    lowered = normalized.lower()

    if not normalized:
        return "Please provide a drug discovery or biomedical research question."

    if re.search(r"ignore .*instructions|jailbreak|previous instructions|guaranteed cure", lowered):
        return (
            "I cannot ignore medical safety and evidence requirements. In drug discovery, I can discuss hypotheses, "
            "evidence quality, and research workflows, but I should not provide experimental-drug prescriptions, claim guaranteed cures, "
            "or bypass safeguards."
        )

    if "guarantee" in lowered and "cure" in lowered:
        return (
            "I cannot make a guaranteed cure claim. EGFR inhibition can be relevant in specific molecular contexts, "
            "but response depends on cancer subtype, mutation status, resistance mechanisms, safety, and clinical evidence."
        )

    if _has_any(lowered, ["dosage", "dose", "patient", "prescribe", "treat my", "which drug should i take"]):
        return SAFETY_MESSAGE

    if "हिंदी" in lowered or "बायोमार्कर" in normalized or "कौन-कौन" in normalized:
        return _hindi_response(normalized)

    if "biomarker" in lowered:
        return (
            "A biomarker is a measurable biological signal, such as a gene mutation, protein level, imaging feature, "
            "or blood measurement, that can help indicate disease risk, disease state, prognosis, or response to a therapy. "
            "For drug discovery, biomarkers can support target selection, patient stratification, and clinical trial design, "
            "but they need validation before being used for decisions."
        )

    if "admet" in lowered:
        return (
            "ADMET describes how a potential drug behaves in the body: absorption, distribution, metabolism, excretion, "
            "and toxicity. In simple terms, it asks whether a compound can get to the right place, stay long enough to help, "
            "be cleared safely, and avoid harmful effects."
        )

    if "target identification" in lowered:
        return (
            "Target identification is the process of finding a biological molecule or pathway, often a protein or gene, "
            "that appears to play a causal role in a disease and could be modified by a therapy. Strong target hypotheses "
            "usually combine genetics, disease biology, expression data, functional experiments, feasibility of modulation, "
            "and evidence from validation studies."
        )

    if "brca1" in lowered:
        return (
            "BRCA1 is important in DNA repair biology and cancer risk, but it is not automatically a good drug target in every "
            "breast cancer context. Prioritization would depend on disease subtype, mechanism, synthetic-lethality evidence, "
            "patient stratification, assay results, safety considerations, and whether the target is druggable."
        )

    if "overexpressed" in lowered:
        return (
            "No. Overexpression is an important signal, but it is insufficient by itself to prove that a gene should be targeted. "
            "I would look for functional evidence, disease mechanism, genetic support, assay validation, safety risk, and whether "
            "modulating the target is likely to change disease biology."
        )

    if "program officer" in lowered or "non-specialist" in lowered:
        return (
            "In plain language: drug discovery starts by choosing a disease mechanism that matters, then finding a biological "
            "target, testing whether changing it could help, and checking whether a safe compound can affect it. AI can help "
            "researchers search evidence and prioritize options, but it does not replace experimental validation."
        )

    if "human review" in lowered:
        return (
            "AI outputs need human expert review because models can miss context, overstate weak evidence, hallucinate details, "
            "or ignore practical risk. Scientific validation, domain expertise, and safety review are still needed before a "
            "target or compound hypothesis is trusted."
        )

    if "checklist" in lowered:
        return (
            "Checklist: 1. Is there human disease evidence? 2. Is the biology plausible? 3. Is there functional validation? "
            "4. Is the target druggable or otherwise tractable? 5. Are safety risks understood? 6. Is the finding reproducible "
            "across datasets or assays?"
        )

    if _has_any(lowered, ["evidence", "prioritize", "gene target", "target"]):
        return (
            "Before prioritizing a target, I would look for converging evidence: human genetics, disease association, pathway "
            "relevance, expression in affected tissue, functional validation, assay reproducibility, tractability, safety risk, "
            "and translational relevance to the intended patient population. I would also document uncertainty and failure modes."
        )

    if _has_any(lowered, ["compound screening", "molecule design", "drug discovery pipeline"]):
        return (
            "AI can support drug discovery by ranking targets, mining literature, predicting protein or compound properties, "
            "prioritizing molecules for screening, and helping design experiments. These outputs should be treated as decision "
            "support and require validation with domain expertise and laboratory evidence."
        )

    return (
        f"{SYSTEM_SCOPE} For this question, I would frame the answer around evidence strength, uncertainty, validation needs, "
        "and whether the output is research support rather than clinical advice."
    )
