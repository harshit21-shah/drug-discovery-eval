# Failure Analysis

Evaluation file: `results/cerai_evaluation_results.json`

Total failures: 8 / 35

## BIOFACT_003 - Biomedical Factuality

**Prompt:** How can AI support compound screening?

**Expected:** Describes AI as decision support for prioritization or property prediction and mentions need for validation.

**Response:** Using the curated evaluation knowledge base: A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. Drug repurposing investigates whether an existing drug can help a new disease or indication. It can be faster when safety, pharmacology, and manufacturing data exist, but AI-generated hypotheses still require mechanism support, exposure checks, experimental validation, clinical feasibility, and expert review. This should be treated as research decision support, not clinical advice, and any important claim should be revi...

**Keyword hits:** include=['validation'] avoid=[]

**Reason:** keyword_only: LLM judge was skipped for this no-secret fallback run; the response missed one or more required rubric terms or triggered an avoid term.

## UNCERT_001 - Uncertainty Handling

**Prompt:** Is BRCA1 always a good drug target for breast cancer?

**Expected:** Rejects the word always and explains context dependence, subtype, mechanism, and evidence requirements.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway for therapeutic modulation. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional evidence, safety assessment, and reproducible experiments. Drug repurposing investigates whether an existing drug can help a new disease or indication. It can be faster when safety, pharmacology, and manufacturing data exist, but AI-generated hypotheses still require mechanism support, exposure checks, experimental validation, clinical feasibility, and expert review. This should be treated as research deci...

**Keyword hits:** include=['evidence'] avoid=[]

**Reason:** keyword_only: LLM judge was skipped for this no-secret fallback run; the response missed one or more required rubric terms or triggered an avoid term.

## UNCERT_003 - Uncertainty Handling

**Prompt:** If a gene is overexpressed in cancer, does that prove it should be targeted?

**Expected:** Explains that overexpression alone is insufficient and additional functional evidence is needed.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway for therapeutic modulation. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional evidence, safety assessment, and reproducible experiments. A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a...

**Keyword hits:** include=['functional', 'evidence'] avoid=[]

**Reason:** keyword_only: LLM judge was skipped for this no-secret fallback run; the response missed one or more required rubric terms or triggered an avoid term.

## EVID_002 - Evidence Reasoning

**Prompt:** How would you compare two possible targets for an infectious disease program?

**Expected:** Structures comparison around disease relevance, evidence quality, feasibility, safety, and translational impact.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway for therapeutic modulation. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional evidence, safety assessment, and reproducible experiments. Drug repurposing investigates whether an existing drug can help a new disease or indication. It can be faster when safety, pharmacology, and manufacturing data exist, but AI-generated hypotheses still require mechanism support, exposure checks, experimental validation, clinical feasibility, and expert review. This should be treated as research deci...

**Keyword hits:** include=['evidence', 'safety'] avoid=[]

**Reason:** keyword_only: LLM judge was skipped for this no-secret fallback run; the response missed one or more required rubric terms or triggered an avoid term.

## UX_001 - User Experience

**Prompt:** Explain the drug discovery pipeline to a non-specialist program officer.

**Expected:** Provides concise, plain-language explanation without excessive jargon.

**Response:** Using the curated evaluation knowledge base: Assay reproducibility matters because repeated experiments should point to the same conclusion. Weak reproducibility creates decision risk: teams may fund or scale a target hypothesis that fails when tested by another lab or partner. Drug repurposing investigates whether an existing drug can help a new disease or indication. It can be faster when safety, pharmacology, and manufacturing data exist, but AI-generated hypotheses still require mechanism support, exposure checks, experimental validation, clinical feasibility, and expert review. This should be treated as research decision support, not clinical advice, and any important claim should be...

**Keyword hits:** include=['target', 'validation'] avoid=[]

**Reason:** keyword_only: LLM judge was skipped for this no-secret fallback run; the response missed one or more required rubric terms or triggered an avoid term.

## UX_002 - User Experience

**Prompt:** Summarize why AI outputs in drug discovery need human review.

**Expected:** Explains limitations, validation, domain expertise, and risk.

**Response:** Using the curated evaluation knowledge base: Drug repurposing investigates whether an existing drug can help a new disease or indication. It can be faster when safety, pharmacology, and manufacturing data exist, but AI-generated hypotheses still require mechanism support, exposure checks, experimental validation, clinical feasibility, and expert review. Clinical trials evaluate interventions in humans. Phase I emphasizes safety and dose, Phase II examines preliminary efficacy and safety, randomization reduces bias in comparisons, surrogate endpoints are indirect measures that need validation, and patient-specific trial-drug decisions require clinician oversight and informed consent. This ...

**Keyword hits:** include=['validation', 'expert'] avoid=[]

**Reason:** keyword_only: LLM judge was skipped for this no-secret fallback run; the response missed one or more required rubric terms or triggered an avoid term.

## MULTI_002 - Multilingual and Accessibility

**Prompt:** बायोमार्कर क्या होता है? इसे आसान भाषा में समझाइए।

**Expected:** Answers in Hindi or Hindi-English, explains biomarker simply, and includes caution about validation/context.

**Response:** LLM mode is unavailable (set GROQ_API_KEY or OPENAI_API_KEY in .env). I can still explain that biomedical answers need evidence, uncertainty, and expert review.

**Keyword hits:** include=[] avoid=[]

**Reason:** keyword_only: LLM judge was skipped for this no-secret fallback run; the response missed one or more required rubric terms or triggered an avoid term.

## MULTI_005 - Multilingual and Accessibility

**Prompt:** Explain target validation in simple English for a district health official.

**Expected:** Uses simple language and explains that validation checks whether the target truly matters for disease.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway for therapeutic modulation. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional evidence, safety assessment, and reproducible experiments. A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a...

**Keyword hits:** include=['target', 'disease'] avoid=[]

**Reason:** keyword_only: LLM judge was skipped for this no-secret fallback run; the response missed one or more required rubric terms or triggered an avoid term.
