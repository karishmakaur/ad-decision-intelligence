import pandas as pd
import matplotlib.pyplot as plt

SOURCE = "data/processed/2025_mayor_media_attention.csv"
OUTPUT = "data/processed/mamdani_media_attention.png"

df = pd.read_csv(SOURCE)
df["week_start"] = pd.to_datetime(df["week_start"])

df = df[df["candidate"] == "Zohran Kwame Mamdani"].copy()

df = df.sort_values("week_start")

df["media_share_4w"] = (
    df["media_share"]
    .rolling(4, min_periods=1)
    .mean()
)

df["attention_share_4w"] = (
    df["attention_share"]
    .rolling(4, min_periods=1)
    .mean()
)

plt.figure(figsize=(11, 6))

plt.plot(
    df["week_start"],
    df["media_share_4w"],
    label="Media activity share (4-week avg)",
)

plt.plot(
    df["week_start"],
    df["attention_share_4w"],
    label="Wikipedia attention share (4-week avg)",
)

plt.axvline(
    pd.Timestamp("2025-06-24"),
    label="Democratic primary",
)

plt.axvline(
    pd.Timestamp("2025-11-04"),
    label="General election",
)

plt.title("Mamdani: Paid Media Activity vs Public Attention")
plt.xlabel("Week")
plt.ylabel("Share among tracked mayoral candidates")
plt.legend()
plt.tight_layout()

plt.savefig(OUTPUT, dpi=150)
plt.show()