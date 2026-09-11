# Architecture

## System Overview

```mermaid
flowchart TD
    A[NYC Campaign Finance Board] --> D[Python ingestion and normalization]
    B[NYC Board of Elections] --> D
    C[Wikimedia Pageviews API] --> D

    D --> E[Curated analytical datasets]
    E --> F[Deterministic metrics]
    F --> G[Structured evidence bundle]

    G --> H[Local LLM via Ollama]
    H --> I[Grounding validator]

    I -->|Pass| J[Versioned investigation JSON]
    I -->|Fail| H

    J --> K[Static Next.js application]
    K --> L[GitHub Pages]

