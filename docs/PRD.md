# Product Requirements Document

## Product

AI Advertising Decision Intelligence

## Problem

Advertising teams have access to increasingly sophisticated dashboards, planning systems, measurement platforms, and AI assistants.

The remaining challenge is decision quality: determining what the available evidence supports when multiple signals disagree, data is incomplete, and causal conclusions are uncertain.

## Objective

Build an evidence-grounded decision workflow that helps a user:

- identify meaningful signal divergence
- inspect supporting evidence
- surface counter-evidence
- understand uncertainty
- distinguish observations from hypotheses
- retain human ownership of the final decision

## Target Users

Primary users:

- media planners
- advertising product managers
- measurement teams
- strategy teams
- data-product users

## Core User Story

As an advertising decision-maker, I want AI to synthesize multiple evidence sources so that I can investigate a decision without losing visibility into the underlying data, uncertainty, or contradictory signals.

## V1 Scope

The first demonstration uses public 2025 NYC mayoral election data.

V1 includes:

- candidate-controlled paid-media activity
- independent support and opposition activity
- election outcomes
- Wikipedia attention signals
- deterministic analytical metrics
- structured evidence generation
- local LLM synthesis
- automated grounding validation
- static public presentation

## Out of Scope

V1 does not attempt to provide:

- causal attribution
- media-mix modeling
- reach or frequency measurement
- voter persuasion measurement
- sentiment analysis
- live campaign recommendations
- real-time LLM inference
- proprietary advertising data integration

## AI Responsibilities

The AI may:

- summarize observed evidence
- describe differences between signals
- surface counter-evidence
- communicate limitations
- produce evidence-grounded interpretations

The AI may not:

- calculate core metrics
- invent evidence
- infer causation
- claim advertising effectiveness without evidence
- claim statistical significance without a statistical test
- treat attention as sentiment or persuasion

## Product Architecture

```text
Public Sources
    ↓
Data Validation
    ↓
Normalized Data
    ↓
Deterministic Analytics
    ↓
Evidence Bundle
    ↓
Local LLM
    ↓
Grounding Validator
    ↓
Versioned Output
    ↓
Static Product Experience