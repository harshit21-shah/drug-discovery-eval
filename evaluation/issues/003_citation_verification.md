# Issue: Add citation verification and evidence provenance checks

## Problem

Hallucination metrics can identify some unsupported claims, but biomedical deployment needs stronger citation and provenance checks.

## Impact

A model can sound cautious while still inventing a paper, trial, compound, or biomarker relationship.

## Suggested Fix

Add an optional evidence-grounding strategy:

1. Extract cited paper titles, identifiers, genes, compounds, and trials.
2. Verify them against trusted sources such as PubMed, ClinicalTrials.gov, or curated internal evidence stores.
3. Score citation quality and hallucination risk separately.

