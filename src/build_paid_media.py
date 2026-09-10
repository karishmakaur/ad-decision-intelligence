import pandas as pd

SOURCE = "data/raw/cfb/2025_Expenditures.csv"

CONFIRMED_PURPOSES = {
    "TVADS": "television",
    "PRINT": "print",
    "RADIO": "radio",
}

DIGITAL_DESCRIPTIONS = {
    "digital buy",
    "digital ads",
    "online ads",
    "digital ad buy",
    "social media",
    "digital adverstising",
    "digital advertising",
    "digital & social ads",
    "facebook ads",
    "meta ads",
    "digital ad",
    "online ad",
    "social media ads",
    "digital media",
    "internet advertising",
    "facebook digital ads",
    "google ads",
    "online ads facebook",
    "crm-digital ads",
    "youtube ads livestre",
    "digital banner ad",
    "digital advertisemen",
    "facebook ad",
    "online facebook ads",
}

df = pd.read_csv(
    SOURCE,
    dtype={"ZIP": "string"},
    low_memory=False,
)

df["EXPLAIN_CLEAN"] = (
    df["EXPLAIN"]
    .fillna("")
    .str.strip()
    .str.lower()
)

confirmed = df[df["PURPOSECD"].isin(CONFIRMED_PURPOSES)].copy()
confirmed["MEDIA_TYPE"] = confirmed["PURPOSECD"].map(CONFIRMED_PURPOSES)

digital = df[
    (df["PURPOSECD"] == "OTHER")
    & (df["EXPLAIN_CLEAN"].isin(DIGITAL_DESCRIPTIONS))
].copy()
digital["MEDIA_TYPE"] = "digital"

paid_media = pd.concat([confirmed, digital], ignore_index=True)

print("Rows:", len(paid_media))
print("Spend:", round(paid_media["AMNT"].sum(), 2))

print(
    paid_media.groupby("MEDIA_TYPE")["AMNT"]
    .agg(["count", "sum"])
    .sort_values("sum", ascending=False)
)

paid_media.to_csv(
    "data/processed/2025_paid_media.csv",
    index=False,
)

ELECTION_DAY = pd.Timestamp("2025-11-04")

paid_media["DATE"] = pd.to_datetime(paid_media["DATE"])

pre_election = paid_media[
    paid_media["DATE"] <= ELECTION_DAY
].copy()

pre_election.to_csv(
    "data/processed/2025_paid_media_pre_election.csv",
    index=False,
)

print("\nPre-election:")
print("Rows:", len(pre_election))
print("Spend:", round(pre_election["AMNT"].sum(), 2))