import shutil
from pathlib import Path
import json
import re

EVIDENCE_FILE = "data/processed/ai_evidence_mamdani.json"
INVESTIGATION_FILE = "data/processed/ai_investigation_mamdani.json"
WEB_OUTPUT_FILE = "web/public/data/investigation.json"

with open(EVIDENCE_FILE) as f:
    evidence = json.load(f)

with open(INVESTIGATION_FILE) as f:
    investigation = json.load(f)

errors = []

required_fields = {
    "question",
    "finding",
    "evidence",
    "interpretation",
    "counter_evidence",
    "limitations",
    "confidence",
}

missing = required_fields - investigation.keys()

if missing:
    errors.append(f"Missing fields: {sorted(missing)}")

if investigation.get("confidence") not in {"low", "medium", "high"}:
    errors.append("Invalid confidence value")

text = json.dumps(investigation).lower()

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

for phrase in prohibited_phrases:
    if phrase in text:
        errors.append(f"Unsupported analytical claim: '{phrase}'")

# Supporting evidence should contain concrete observed values.
for item in investigation.get("evidence", []):
    if not re.search(r"\d", item):
        errors.append(
            f"Evidence statement lacks a concrete metric: {item}"
        )

if errors:
    print("GROUNDING CHECK FAILED\n")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

Path(WEB_OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(INVESTIGATION_FILE, WEB_OUTPUT_FILE)

print("GROUNDING CHECK PASSED")
print(f"Published {WEB_OUTPUT_FILE}")