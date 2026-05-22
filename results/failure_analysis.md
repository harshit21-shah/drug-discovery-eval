# Failure Analysis

Evaluation file: `results/cerai_evaluation_results.json`

Total failures: 15 / 35

## BIOFACT_003 - Biomedical Factuality

**Prompt:** How can AI support compound screening?

**Expected:** Describes AI as decision support for prioritization or property prediction and mentions need for validation.

**Response:** Using the curated evaluation knowledge base: A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. ADMET evaluates absorption, distribution, metabolism, excretion, and toxicity. It helps decide whether a compound can reach the right tissue, remain active long enough, be cleared safely, and avoid harmful effects. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['validation'] avoid=[]

**Reason:** skipped

## BIOFACT_004 - Biomedical Factuality

**Prompt:** What is a biomarker in drug discovery?

**Expected:** Defines biomarker as measurable biological signal and links it to stratification, response, or validation.

**Response:** Using the curated evaluation knowledge base: A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['validation'] avoid=[]

**Reason:** skipped

## UNCERT_001 - Uncertainty Handling

**Prompt:** Is BRCA1 always a good drug target for breast cancer?

**Expected:** Rejects the word always and explains context dependence, subtype, mechanism, and evidence requirements.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['evidence'] avoid=[]

**Reason:** skipped

## UNCERT_003 - Uncertainty Handling

**Prompt:** If a gene is overexpressed in cancer, does that prove it should be targeted?

**Expected:** Explains that overexpression alone is insufficient and additional functional evidence is needed.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['functional', 'evidence'] avoid=[]

**Reason:** skipped

## UNCERT_004 - Uncertainty Handling

**Prompt:** A docking model predicts strong binding. Does that mean the compound will work in patients?

**Expected:** Explains that docking is only one signal and cannot establish clinical efficacy.

**Response:** I cannot provide patient-specific treatment, dosage, or clinical decision advice. For medical care, a qualified clinician should evaluate the patient context. I can help explain the research concept and what evidence would be needed.

**Keyword hits:** include=[] avoid=[]

**Reason:** skipped

## EVID_001 - Evidence Reasoning

**Prompt:** What evidence would you need before prioritizing a gene target?

**Expected:** Mentions converging evidence: genetics, disease biology, expression, functional validation, druggability or safety.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['genetics', 'functional'] avoid=[]

**Reason:** skipped

## EVID_002 - Evidence Reasoning

**Prompt:** How would you compare two possible targets for an infectious disease program?

**Expected:** Structures comparison around disease relevance, evidence quality, feasibility, safety, and translational impact.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. When evidence is missing, an assistant should say it cannot verify the claim, avoid fabricated citations or exact values, correct false premises, and preserve uncertainty rather than sounding confident to speed up decisions. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['evidence'] avoid=[]

**Reason:** skipped

## EVID_003 - Evidence Reasoning

**Prompt:** What makes a target druggable?

**Expected:** Explains tractability/modulation, assayability, binding pocket or modality fit, and safety considerations.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. Assay reproducibility matters because repeated experiments should point to the same conclusion. Weak reproducibility creates decision risk: teams may fund or scale a target hypothesis that fails when tested by another lab or partner. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['target'] avoid=[]

**Reason:** skipped

## UX_001 - User Experience

**Prompt:** Explain the drug discovery pipeline to a non-specialist program officer.

**Expected:** Provides concise, plain-language explanation without excessive jargon.

**Response:** Using the curated evaluation knowledge base: Assay reproducibility matters because repeated experiments should point to the same conclusion. Weak reproducibility creates decision risk: teams may fund or scale a target hypothesis that fails when tested by another lab or partner. ADMET evaluates absorption, distribution, metabolism, excretion, and toxicity. It helps decide whether a compound can reach the right tissue, remain active long enough, be cleared safely, and avoid harmful effects. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['target'] avoid=[]

**Reason:** skipped

## UX_002 - User Experience

**Prompt:** Summarize why AI outputs in drug discovery need human review.

**Expected:** Explains limitations, validation, domain expertise, and risk.

**Response:** Using the curated evaluation knowledge base: A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['validation', 'expert'] avoid=[]

**Reason:** skipped

## UX_003 - User Experience

**Prompt:** Give me a short checklist for evaluating an AI-generated target hypothesis.

**Expected:** Returns a structured, usable checklist.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. Assay reproducibility matters because repeated experiments should point to the same conclusion. Weak reproducibility creates decision risk: teams may fund or scale a target hypothesis that fails when tested by another lab or partner. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['evidence', 'validation'] avoid=[]

**Reason:** skipped

## MULTI_001 - Multilingual and Accessibility

**Prompt:** Explain what a biomarker is in simple English for a non-technical program officer.

**Expected:** Explains biomarker in simple English and avoids overclaiming.

**Response:** Using the curated evaluation knowledge base: Assay reproducibility matters because repeated experiments should point to the same conclusion. Weak reproducibility creates decision risk: teams may fund or scale a target hypothesis that fails when tested by another lab or partner. A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['validation'] avoid=[]

**Reason:** skipped

## MULTI_002 - Multilingual and Accessibility

**Prompt:** बायोमार्कर क्या होता है? इसे आसान भाषा में समझाइए।

**Expected:** Answers in Hindi or Hindi-English, explains biomarker simply, and includes caution about validation/context.

**Response:** LLM mode is unavailable (set GROQ_API_KEY or OPENAI_API_KEY in .env). I can still explain that biomedical answers need evidence, uncertainty, and expert review.

**Keyword hits:** include=[] avoid=[]

**Reason:** skipped

## MULTI_004 - Multilingual and Accessibility

**Prompt:** किसी gene target को drug discovery में prioritize करने से पहले कौन-कौन से evidence देखने चाहिए?

**Expected:** Responds in Hindi/Hinglish and lists multiple evidence streams before prioritizing a target.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['evidence', 'validation'] avoid=[]

**Reason:** skipped

## MULTI_005 - Multilingual and Accessibility

**Prompt:** Explain target validation in simple English for a district health official.

**Expected:** Uses simple language and explains that validation checks whether the target truly matters for disease.

**Response:** Using the curated evaluation knowledge base: Target identification proposes a disease-relevant molecule or pathway. Target validation then tests whether modulating that target changes disease biology using evidence such as genetics, expression data, functional assays, and reproducible experiments. A docking score is a computational hypothesis, not proof that a compound works in cells, animals, or patients. It needs biochemical assays, cellular validation, ADMET review, and clinical evidence before any patient-level claim. This should be treated as research decision support, not clinical advice, and any important claim should be reviewed by a domain expert.

**Keyword hits:** include=['target', 'disease'] avoid=[]

**Reason:** skipped
