import pandas as pd

MEDIA = "data/processed/2025_mayor_weekly_media.csv"
ATTENTION = "data/processed/2025_mayor_weekly_attention.csv"
OUTPUT = "data/processed/2025_mayor_media_attention.csv"

media = pd.read_csv(MEDIA)
attention = pd.read_csv(ATTENTION)

media["week_start"] = pd.to_datetime(media["week_start"])
attention["week_start"] = pd.to_datetime(attention["week_start"])

tracked_candidates = attention["candidate"].unique()

media = media[
    media["canonical_name"].isin(tracked_candidates)
].copy()

media = (
    media.groupby(
        ["week_start", "canonical_name", "spend_context"],
        as_index=False,
    )["spend"]
    .sum()
)

media = (
    media.pivot_table(
        index=["week_start", "canonical_name"],
        columns="spend_context",
        values="spend",
        aggfunc="sum",
        fill_value=0,
    )
    .reset_index()
)

# Avoid collision with attention's "candidate" column
media = media.rename(
    columns={
        "candidate": "candidate_spend",
        "support": "support_spend",
        "oppose": "oppose_spend",
    }
)

for column in [
    "candidate_spend",
    "support_spend",
    "oppose_spend",
]:
    if column not in media.columns:
        media[column] = 0

media["supportive_media_spend"] = (
    media["candidate_spend"]
    + media["support_spend"]
)

media["total_media_activity"] = (
    media["candidate_spend"]
    + media["support_spend"]
    + media["oppose_spend"]
)

weekly_total = media.groupby("week_start")[
    "total_media_activity"
].transform("sum")

weekly_totals = (
    media.groupby("week_start", as_index=False)["total_media_activity"]
    .sum()
    .rename(columns={"total_media_activity": "weekly_total_media_activity"})
)

media = media.merge(weekly_totals, on="week_start", how="left")

media["media_share"] = (
    media["total_media_activity"]
    / media["weekly_total_media_activity"]
)

combined = attention.merge(
    media,
    left_on=["week_start", "candidate"],
    right_on=["week_start", "canonical_name"],
    how="left",
)

numeric_columns = [
    "candidate_spend",
    "support_spend",
    "oppose_spend",
    "supportive_media_spend",
    "total_media_activity",
]

combined[numeric_columns] = combined[numeric_columns].fillna(0)

combined["attention_minus_media_share"] = (
    combined["attention_share"] - combined["media_share"]
)

combined.to_csv(OUTPUT, index=False)

print("Rows:", len(combined))

print("\nLargest attention/media divergences:")
print(
    combined[
        [
            "week_start",
            "candidate",
            "media_share",
            "attention_share",
            "attention_minus_media_share",
        ]
    ]
    .sort_values(
        "attention_minus_media_share",
        ascending=False,
    )
    .head(10)
    .to_string(index=False)
)