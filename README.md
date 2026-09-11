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
```

## AI Guardrails

The AI workflow explicitly prevents unsupported claims such as:

- Causal claims
- Correlation claims without calculated statistics
- Claims of advertising effectiveness
- Unsupported statistical significance
- Invented metrics

Only validated output is published to the public application.

## Data Sources

- NYC Campaign Finance Board
- NYC Board of Elections
- Wikimedia Pageviews API

Only public data is used.

No proprietary advertising datasets, schemas, models, or business logic are included.

## Current Case Study

The current investigation examines how Zohran Mamdani's analyzed paid-media environment compared with:

- Electoral performance
- Supportive paid-media activity
- Opposition paid-media activity
- Public attention measured through Wikipedia pageviews

The analysis is descriptive and does not claim that advertising caused election outcomes.

## Technology

- Python
- pandas
- Next.js
- TypeScript
- Ollama
- Llama 3.2
- GitHub Actions
- GitHub Pages

## Product Principles

1. Calculations stay deterministic.
2. AI synthesizes evidence rather than inventing it.
3. Counter-evidence is surfaced alongside findings.
4. Uncertainty is explicit.
5. Human decision-making remains authoritative.
6. Public outputs are reproducible and auditable.

## Repository Structure

```text
data/
  raw/
  processed/
  reference/

src/
  data processing
  analytics
  AI evidence generation
  AI synthesis
  grounding validation

web/
  Next.js public application

.github/workflows/
  GitHub Pages deployment
```

## Local Development

Create and activate the Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the web application:

```bash
cd web
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Disclaimer

This project is a portfolio demonstration of advertising decision-intelligence architecture using public election data.

Observed relationships between media activity, public attention, and election results do not establish causation.
