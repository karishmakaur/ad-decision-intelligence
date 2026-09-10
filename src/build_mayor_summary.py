import pandas as pd

MEDIA_FILE = "data/processed/2025_paid_media_pre_election.csv"
RESULTS_FILE = "data/processed/2025_mayor_candidate_ed_results.csv"
CANDIDATE_FILE = "data/reference/mayor_candidates.csv"
OUTPUT = "data/processed/2025_mayor_summary.csv"

media = pd.read_csv(MEDIA_FILE, dtype={"CANDID": str})
results = pd.read_csv(RESULTS_FILE)
candidates = pd.read_csv(CANDIDATE_FILE, dtype={"cfb_candidate_id": str})

# Paid-media spend by candidate
spend = (
    media.groupby("CANDID", as_index=False)["AMNT"]
    .sum()
    .rename(columns={
        "CANDID": "cfb_candidate_id",
        "AMNT": "paid_media_spend",
    })
)

# Citywide votes
votes = (
    results.groupby("Candidate", as_index=False)["Tally"]
    .sum()
    .rename(columns={
        "Candidate": "canonical_name",
        "Tally": "votes",
    })
)

summary = (
    candidates
    .merge(spend, on="cfb_candidate_id", how="left")
    .merge(votes, on="canonical_name", how="left")
)

summary["paid_media_spend"] = summary["paid_media_spend"].fillna(0)
summary["votes"] = summary["votes"].fillna(0).astype(int)

summary["vote_share"] = (
    summary["votes"] / summary["votes"].sum()
)

summary.to_csv(OUTPUT, index=False)

print(
    summary[
        ["canonical_name", "paid_media_spend", "votes", "vote_share"]
    ].to_string(index=False)
)