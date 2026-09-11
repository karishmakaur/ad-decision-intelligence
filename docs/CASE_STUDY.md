# Case Study: AI Advertising Decision Intelligence

## Problem

Advertising decision-makers increasingly have access to large datasets, dashboards, forecasting tools, and AI assistants.

The harder problem is deciding what the evidence actually supports when signals disagree.

This project explores how AI can help synthesize advertising evidence while preserving provenance, uncertainty, counter-evidence, and human judgment.

## Product Question

How can an AI system help explain differences between paid-media activity, public attention, and observed outcomes without inventing evidence or overstating causality?

## Demonstration Environment

The 2025 NYC mayoral election was selected because high-quality public data exists across multiple independent sources:

- NYC Campaign Finance Board advertising expenditures
- Independent expenditure support and opposition
- NYC Board of Elections results
- Wikimedia pageview attention signals

No proprietary advertising data or business logic is used.

## Product Approach

The system separates calculation from interpretation.

### Deterministic Layer

Python pipelines:

- normalize public datasets
- classify high-confidence paid-media activity
- calculate candidate and independent spending
- aggregate election results
- calculate media-share and attention-share metrics
- construct structured evidence bundles

### AI Layer

A local LLM receives only the structured evidence bundle.

The model is responsible for:

- synthesizing observed patterns
- explaining evidence
- surfacing counter-evidence
- communicating uncertainty

The model is not responsible for calculating metrics.

### Validation Layer

AI output is checked before publication.

The validator rejects unsupported language including:

- causal claims
- unsupported correlation claims
- advertising-effectiveness claims
- unsupported statistical significance
- ungrounded analytical statements

Only validated output is copied into the public application.

## Example Finding

In the analyzed dataset, Zohran Mamdani received 50.9% of candidate votes while accounting for 28.2% of analyzed supportive paid-media spending.

He was also the target of 86.6% of analyzed opposition paid-media spending.

Wikipedia attention and paid-media activity also diverged during several periods.

These observations identify a decision-relevant pattern, but they do not establish that advertising caused the electoral outcome.

## Product Decision

The public application does not make live LLM calls.

AI analysis is generated locally, validated, versioned, and then published as static JSON.

This design provides:

- zero incremental inference cost
- reproducible outputs
- predictable public demos
- clear auditability
- reduced hallucination risk
- separation between model reasoning and production presentation

## Architecture

```text
Public Data
    ↓
Normalization
    ↓
Deterministic Analytics
    ↓
Evidence Bundle
    ↓
Local LLM
    ↓
Grounding Validation
    ↓
Versioned AI Output
    ↓
Static Next.js Product