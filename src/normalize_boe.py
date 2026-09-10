import pandas as pd

SOURCE = "data/raw/boe/00000100000Citywide Mayor Citywide EDLevel.csv"
OUTPUT = "data/processed/2025_mayor_candidate_ed_results.csv"

NON_CANDIDATE_UNITS = {
    "Public Counter",
    "Manually Counted Emergency",
    "Absentee / Military",
    "Affidavit",
    "Scattered",
}

raw = pd.read_csv(SOURCE, header=None, dtype=str)

columns = raw.iloc[0, :11].tolist()

df = raw.iloc[:, 11:22].copy()
df.columns = columns

df["Tally"] = pd.to_numeric(
    df["Tally"].str.replace(",", "", regex=False),
    errors="coerce",
)

# Keep candidate rows only
df = df[
    df["Unit Name"].notna()
    & ~df["Unit Name"].isin(NON_CANDIDATE_UNITS)
].copy()

# Separate candidate name from ballot line
df[["Candidate", "Ballot Line"]] = df["Unit Name"].str.extract(
    r"^(.*?)\s*\((.*?)\)\s*$"
)

# Combine multiple ballot lines for each candidate
results = (
    df.groupby(
        ["AD", "ED", "County", "Candidate"],
        as_index=False
    )["Tally"]
    .sum()
)

results.to_csv(OUTPUT, index=False)

print("Rows:", len(results))
print("Candidates:", results["Candidate"].unique().tolist())

print("\nCitywide vote totals:")
print(
    results.groupby("Candidate")["Tally"]
    .sum()
    .sort_values(ascending=False)
)