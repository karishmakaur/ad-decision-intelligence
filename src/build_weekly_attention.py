import pandas as pd

SOURCE = "data/processed/2025_mayor_wikipedia_attention.csv"
OUTPUT = "data/processed/2025_mayor_weekly_attention.csv"

df = pd.read_csv(SOURCE)
df["date"] = pd.to_datetime(df["date"])

df["week_start"] = (
    df["date"]
    .dt.to_period("W-SUN")
    .dt.start_time
)

weekly = (
    df.groupby(["week_start", "candidate"], as_index=False)["pageviews"]
    .sum()
)

weekly["attention_share"] = (
    weekly["pageviews"]
    / weekly.groupby("week_start")["pageviews"].transform("sum")
)

weekly.to_csv(OUTPUT, index=False)

print("Rows:", len(weekly))

print("\nTotal pageviews:")
print(
    weekly.groupby("candidate")["pageviews"]
    .sum()
    .sort_values(ascending=False)
)

print("\nPeak weekly attention:")
print(
    weekly.loc[
        weekly.groupby("candidate")["pageviews"].idxmax(),
        ["candidate", "week_start", "pageviews"]
    ].to_string(index=False)
)