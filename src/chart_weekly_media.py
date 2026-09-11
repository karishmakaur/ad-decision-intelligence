import pandas as pd
import matplotlib.pyplot as plt

SOURCE = "data/processed/2025_mayor_weekly_media.csv"
OUTPUT = "data/processed/2025_mayor_weekly_media.png"

df = pd.read_csv(SOURCE)
df["week_start"] = pd.to_datetime(df["week_start"])

weekly = (
    df.groupby(["week_start", "spend_context"])["spend"]
    .sum()
    .unstack(fill_value=0)
)

weekly.plot(figsize=(11, 6))

plt.title("2025 NYC Mayoral Race: Weekly Paid Media Activity")
plt.xlabel("Week")
plt.ylabel("Spend ($)")
plt.tight_layout()
plt.savefig(OUTPUT, dpi=150)
plt.show()