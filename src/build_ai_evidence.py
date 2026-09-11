import json
from pathlib import Path

import pandas as pd

SUMMARY = "data/processed/2025_mayor_media_summary.csv"
ATTENTION = "data/processed/2025_mayor_media_attention.csv"
OUTPUT = "data/processed/ai_evidence_mamdani.json"

summary = pd.read_csv(SUMMARY)
attention = pd.read_csv(ATTENTION)

summary["supportive_media_spend"] = (
    summary["direct_media_spend"]
    + summary["independent_support_spend"]
)

mamdani = summary[
    summary["canonical_name"] == "Zohran Kwame Mamdani"
].iloc[0]

total_supportive = summary["supportive_media_spend"].sum()
total_opposition = summary["independent_oppose_spend"].sum()

mamdani_attention = attention[
    attention["candidate"] == "Zohran Kwame Mamdani"
].copy()

largest_divergence = (
    mamdani_attention
    .dropna(subset=["attention_minus_media_share"])
    .sort_values("attention_minus_media_share", ascending=False)
    .iloc[0]
)

evidence = {
    "question": (
        "How did Mamdani's paid-media environment compare with "
        "his electoral performance and public attention?"
    ),
    "candidate": "Zohran Kwame Mamdani",
    "facts": {
        "votes": int(mamdani["votes"]),
        "vote_share": round(float(mamdani["vote_share"]), 4),
        "direct_media_spend": round(float(mamdani["direct_media_spend"]), 2),
        "independent_support_spend": round(
            float(mamdani["independent_support_spend"]), 2
        ),
        "independent_oppose_spend": round(
            float(mamdani["independent_oppose_spend"]), 2
        ),
        "supportive_media_share": round(
            float(mamdani["supportive_media_spend"] / total_supportive), 4
        ),
        "opposition_media_share": round(
            float(mamdani["independent_oppose_spend"] / total_opposition), 4
        ),
    },
    "attention_signal": {
        "largest_divergence_week": str(
            largest_divergence["week_start"]
        )[:10],
        "media_share": round(
            float(largest_divergence["media_share"]), 4
        ),
        "wikipedia_attention_share": round(
            float(largest_divergence["attention_share"]), 4
        ),
    },
    "limitations": [
        "Wikipedia pageviews measure attention, not voter sentiment.",
        "Observed relationships do not establish causation.",
        "Paid-media data does not capture all campaign activity or earned media.",
    ],
}

Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w") as f:
    json.dump(evidence, f, indent=2)

print(f"Created {OUTPUT}")
print(json.dumps(evidence, indent=2))