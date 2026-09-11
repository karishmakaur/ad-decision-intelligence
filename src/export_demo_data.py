import json
from pathlib import Path

import pandas as pd

SUMMARY = "data/processed/2025_mayor_media_summary.csv"
OUTPUT = "web/public/data/summary.json"

df = pd.read_csv(SUMMARY)

df["supportive_media_spend"] = (
    df["direct_media_spend"]
    + df["independent_support_spend"]
)

df["opposition_media_spend"] = df["independent_oppose_spend"]

total_supportive = df["supportive_media_spend"].sum()
total_opposition = df["opposition_media_spend"].sum()

mamdani = df[df["canonical_name"] == "Zohran Kwame Mamdani"].iloc[0]

insight = {
    "candidate": "Zohran Kwame Mamdani",
    "supportive_media_share": float(
        mamdani["supportive_media_spend"] / total_supportive
    ),
    "opposition_media_share": float(
        mamdani["opposition_media_spend"] / total_opposition
    ),
    "vote_share": float(mamdani["vote_share"]),
}

data = {
    "featured_insight": insight,
    "total_media_activity": round(float(df["total_media_activity"].sum()), 2),
    "total_votes": int(df["votes"].sum()),
    "candidates": (
        df[
            [
                "canonical_name",
                "supportive_media_spend",
                "opposition_media_spend",
                "total_media_activity",
                "votes",
                "vote_share",
            ]
        ]
        .sort_values("votes", ascending=False)
        .to_dict(orient="records")
    ),
}

Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w") as f:
    json.dump(data, f, indent=2)

print(f"Created {OUTPUT}")
print(f"Candidates: {len(data['candidates'])}")
print(f"Media activity: ${data['total_media_activity']:,.2f}")