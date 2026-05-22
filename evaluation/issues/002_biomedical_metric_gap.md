# Issue: Need biomedical validity metrics for drug-discovery evaluation

## Problem

CeRAI includes general safety, language, hallucination, and conversational-quality metrics. For drug-discovery use cases, those are necessary but not sufficient.

## Impact

Generic metrics may miss scientific failures such as:

- fabricated IC50 values
- invalid gene or drug names
- unsupported biomarker claims
- clinical-trial phase confusion
- weak evidence presented as validated biology

## Suggested Fix

Add a biomedical evaluator strategy that checks:

- gene/protein name validity
- drug/compound name validity
- citation presence and verifiability
- clinical advice refusal
- calibrated uncertainty for preclinical claims

