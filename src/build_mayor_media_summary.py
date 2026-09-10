import pandas as pd

DIRECT = "data/processed/2025_paid_media_pre_election.csv"
INDEPENDENT = "data/processed/2025_independent_paid_media.csv"
CANDIDATES = "data/reference/mayor_candidates.csv"
RESULTS = "data/processed/2025_mayor_candidate_ed_results.csv"
OUTPUT = "data/processed/2025_mayor_media_summary.csv"

candidates = pd.read_csv(CANDIDATES, dtype={"cfb_candidate_id": str})
direct = pd.read_csv(DIRECT, dtype={"CANDID": str})
independent = pd.read_csv(INDEPENDENT, dtype={"CANDID": str})
results = pd.read_csv(RESULTS)

# Candidate-controlled paid media
direct_spend = (
    direct.groupby("CANDID")["AMNT"]
    .sum()
    .rename("direct_media_spend")
)

# Independent media by support/oppose
ie = (
    independent
    .pivot_table(
        index="CANDID",
        columns="POSITION",
        values="ALLOCATION",
        aggfunc="sum",
        fill_value=0,
    )
    .rename(columns={
        "Support": "independent_support_spend",
        "Oppose": "independent_oppose_spend",
    })
)

# Election results
votes = (
    results.groupby("Candidate")["Tally"]
    .sum()
    .rename("votes")
)

summary = candidates.copy()

summary = summary.merge(
    direct_spend,
    left_on="cfb_candidate_id",
    right_index=True,
    how="left",
)

summary = summary.merge(
    ie,
    left_on="cfb_candidate_id",
    right_index=True,
    how="left",
)

summary = summary.merge(
    votes,
    left_on="canonical_name",
    right_index=True,
    how="left",
)

spend_cols = [
    "direct_media_spend",
    "independent_support_spend",
    "independent_oppose_spend",
]

summary[spend_cols] = summary[spend_cols].fillna(0)

summary["total_media_activity"] = (
    summary["direct_media_spend"]
    + summary["independent_support_spend"]
    + summary["independent_oppose_spend"]
)

summary["vote_share"] = summary["votes"] / summary["votes"].sum()

summary.to_csv(OUTPUT, index=False)

print(
    summary[
        [
            "canonical_name",
            "direct_media_spend",
            "independent_support_spend",
            "independent_oppose_spend",
            "total_media_activity",
            "votes",
            "vote_share",
        ]
    ].to_string(index=False)
)