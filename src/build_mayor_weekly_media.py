import pandas as pd

DIRECT = "data/processed/2025_paid_media_pre_election.csv"
INDEPENDENT = "data/processed/2025_independent_paid_media.csv"
CANDIDATES = "data/reference/mayor_candidates.csv"
OUTPUT = "data/processed/2025_mayor_weekly_media.csv"

candidates = pd.read_csv(
    CANDIDATES,
    dtype={"cfb_candidate_id": str},
)

# Candidate-controlled media
direct = pd.read_csv(DIRECT, dtype={"CANDID": str})
direct["DATE"] = pd.to_datetime(direct["DATE"])

direct = direct.merge(
    candidates,
    left_on="CANDID",
    right_on="cfb_candidate_id",
    how="inner",
)

direct = direct.assign(
    spend_context="candidate",
    spend=direct["AMNT"],
    date=direct["DATE"],
    media_type=direct["MEDIA_TYPE"],
)

# Independent media
independent = pd.read_csv(
    INDEPENDENT,
    dtype={"CANDID": str},
)
independent["COMM_DATE"] = pd.to_datetime(independent["COMM_DATE"])

independent = independent.merge(
    candidates,
    left_on="CANDID",
    right_on="cfb_candidate_id",
    how="inner",
)

independent = independent.assign(
    spend_context=independent["POSITION"].str.lower(),
    spend=independent["ALLOCATION"],
    date=independent["COMM_DATE"],
    media_type=independent["MEDIA_TYPE"],
)

combined = pd.concat(
    [
        direct[
            [
                "canonical_name",
                "date",
                "media_type",
                "spend_context",
                "spend",
            ]
        ],
        independent[
            [
                "canonical_name",
                "date",
                "media_type",
                "spend_context",
                "spend",
            ]
        ],
    ],
    ignore_index=True,
)

# Monday-starting week
combined["week_start"] = (
    combined["date"]
    .dt.to_period("W-SUN")
    .dt.start_time
)

weekly = (
    combined.groupby(
        [
            "week_start",
            "canonical_name",
            "media_type",
            "spend_context",
        ],
        as_index=False,
    )["spend"]
    .sum()
)

weekly.to_csv(OUTPUT, index=False)

print("Rows:", len(weekly))
print("\nSpend by media type:")
print(
    weekly.groupby("media_type")["spend"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSpend by context:")
print(
    weekly.groupby("spend_context")["spend"]
    .sum()
    .sort_values(ascending=False)
)