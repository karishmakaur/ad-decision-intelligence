import pandas as pd
from pathlib import Path

SOURCE = next(Path("data/raw/cfb").glob("CFB-IE-COMM_*.csv"))
OUTPUT = "data/processed/2025_independent_paid_media.csv"

PAID_MEDIA_TYPES = {
    "TVADS": "television",
    "INTVID": "digital_video",
    "INTAD": "digital_display",
    "SRADIO": "audio",
    "RADIO": "audio",
    "PRINT": "print",
    "BILLBD": "billboard",
}

ELECTION_DAY = pd.Timestamp("2025-11-04")

df = pd.read_csv(SOURCE, low_memory=False)

df["COMM_DATE"] = pd.to_datetime(df["COMM_DATE"], errors="coerce")

media = df[
    df["COMM_PURPOSECD"].isin(PAID_MEDIA_TYPES)
    & (df["COMM_DATE"] <= ELECTION_DAY)
].copy()

media["MEDIA_TYPE"] = media["COMM_PURPOSECD"].map(PAID_MEDIA_TYPES)

print("Rows:", len(media))
print("Communications:", media["COMMUNICATION_ID"].nunique())
print("Allocated spend:", round(media["ALLOCATION"].sum(), 2))

print("\nBy media type:")
print(
    media.groupby("MEDIA_TYPE")["ALLOCATION"]
    .agg(["count", "sum"])
    .sort_values("sum", ascending=False)
)

print("\nBy position:")
print(
    media.groupby("POSITION")["ALLOCATION"]
    .agg(["count", "sum"])
)

media.to_csv(OUTPUT, index=False)