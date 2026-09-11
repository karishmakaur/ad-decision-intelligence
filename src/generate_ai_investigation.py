import json
from pathlib import Path

import requests


EVIDENCE_FILE = "data/processed/ai_evidence_mamdani.json"
OUTPUT_FILE = "data/processed/ai_investigation_mamdani.json"


with open(EVIDENCE_FILE) as f:
    source = json.load(f)


facts = source["facts"]
attention = source["attention_signal"]


# These evidence statements are deterministic.
# The LLM is not allowed to invent or rewrite the numbers.
evidence_bullets = [
    (
        f"Mamdani received {facts['vote_share']:.1%} of the recorded "
        f"candidate vote ({facts['votes']:,} votes)."
    ),
    (
        f"He accounted for {facts['supportive_media_share']:.1%} "
        f"of analyzed supportive paid-media spending."
    ),
    (
        f"He was the target of {facts['opposition_media_share']:.1%} "
        f"of analyzed opposition paid-media spending."
    ),
    (
        f"In the week of {attention['largest_divergence_week']}, "
        f"his analyzed media-activity share was "
        f"{attention['media_share']:.1%}, while his Wikipedia "
        f"attention share was "
        f"{attention['wikipedia_attention_share']:.1%}."
    ),
]


# Claims we do not want the model making unless separately calculated.
prohibited_phrases = [
    "positively correlated",
    "negatively correlated",
    "effective in generating",
    "caused",
    "led to",
    "resulted in",
    "drove",
    "because of advertising",
    "statistically significant",
    "significantly higher",
    "significantly lower",
    "significant divergence",
    "significant disparity",
    "notable disparity",
]


prompt = f"""
You are producing an evidence-grounded advertising decision-intelligence
analysis.

Use ONLY the supplied evidence.

Rules:
- Do not use outside knowledge.
- Do not invent facts.
- Do not invent numbers.
- Do not claim causation.
- Do not claim correlation unless a correlation statistic is supplied.
- Do not say advertising was effective.
- Do not imply that advertising produced electoral results.
- Do not infer voter sentiment from Wikipedia pageviews.
- Treat Wikipedia pageviews only as an attention signal.
- Describe differences, divergence, gaps, and observed patterns only.
- Use neutral descriptive language.

Return valid JSON with exactly these fields:

{{
  "finding": "...",
  "interpretation": "...",
  "counter_evidence": ["...", "..."],
  "confidence": "low|medium|high"
}}

QUESTION:
{source["question"]}

OBSERVED EVIDENCE:
{json.dumps(evidence_bullets, indent=2)}

LIMITATIONS:
{json.dumps(source["limitations"], indent=2)}

FORBIDDEN PHRASES:
{json.dumps(prohibited_phrases, indent=2)}

Do not use any forbidden phrase.

Prefer descriptive wording such as:
- difference
- divergence
- gap
- observed pattern
- does not move proportionally
- cannot be explained by this evidence alone
"""


current_prompt = prompt
result = None


for attempt in range(3):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": current_prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0
            },
        },
        timeout=120,
    )

    response.raise_for_status()

    candidate = json.loads(response.json()["response"])

    required_fields = {
        "finding",
        "interpretation",
        "counter_evidence",
        "confidence",
    }

    missing_fields = required_fields - candidate.keys()

    if missing_fields:
        violations = [
            f"missing field: {field}"
            for field in sorted(missing_fields)
        ]
    else:
        text = json.dumps(candidate).lower()

        violations = [
            phrase
            for phrase in prohibited_phrases
            if phrase in text
        ]

    if not violations:
        result = candidate
        break

    print(
        f"Attempt {attempt + 1} rejected: "
        f"{', '.join(violations)}"
    )

    current_prompt += f"""

Your previous response was rejected for the following reasons:

{json.dumps(violations, indent=2)}

Rewrite the response.

Requirements:
- Remove every rejected phrase or issue.
- Use neutral descriptive language.
- Do not introduce new facts.
- Do not make causal claims.
- Do not claim statistical significance.
- Return valid JSON only.
"""


if result is None:
    raise ValueError(
        "AI output failed grounding rules after 3 attempts."
    )


if result["confidence"] not in {"low", "medium", "high"}:
    raise ValueError(
        f"Invalid confidence value: {result['confidence']}"
    )


final_result = {
    "question": source["question"],
    "finding": result["finding"],
    "evidence": evidence_bullets,
    "interpretation": result["interpretation"],
    "counter_evidence": result["counter_evidence"],
    "limitations": source["limitations"],
    "confidence": result["confidence"],
}


Path(OUTPUT_FILE).parent.mkdir(
    parents=True,
    exist_ok=True,
)


with open(OUTPUT_FILE, "w") as f:
    json.dump(
        final_result,
        f,
        indent=2,
    )


print(json.dumps(final_result, indent=2))
print(f"\nCreated {OUTPUT_FILE}")