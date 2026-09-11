# AI Advertising Decision Intelligence

Evidence-grounded AI decision intelligence built from public advertising, election, and attention data.

**Live demo:**  
https://karishmakaur.github.io/ad-decision-intelligence/

## Product Goal

Advertising platforms provide increasingly sophisticated data, planning, optimization, and AI interfaces.

This project explores a complementary problem:

**How can AI help decision-makers interpret multiple signals while preserving evidence, uncertainty, counter-evidence, and human judgment?**

The 2025 NYC mayoral election is used as a public-data demonstration environment.

## What the Product Does

The application combines:

- Candidate-controlled paid-media activity
- Independent expenditure support and opposition
- Election results
- Wikipedia attention signals
- AI-generated evidence synthesis
- Automated grounding validation

The AI is not allowed to perform the underlying calculations or invent evidence.

Deterministic Python pipelines calculate the metrics first. The local LLM receives a structured evidence bundle and produces an interpretation that must pass validation before publication.

## Architecture

```text
Public Data Sources
        ↓
Python Ingestion + Validation
        ↓
Normalized Analytical Dataset
        ↓
Deterministic Metrics
        ↓
Structured Evidence Bundle
        ↓
Local LLM
        ↓
Grounding Validator
        ↓
Versioned JSON
        ↓
Static Next.js Application
