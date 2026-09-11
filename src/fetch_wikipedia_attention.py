import requests
import pandas as pd

PAGES = {
    "Zohran Kwame Mamdani": "Zohran_Mamdani",
    "Andrew M. Cuomo": "Andrew_Cuomo",
    "Curtis A. Sliwa": "Curtis_Sliwa",
    "Eric L. Adams": "Eric_Adams",
}

START = "20250101"
END = "20251104"

rows = []

for candidate, page in PAGES.items():
    url = (
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"en.wikipedia/all-access/user/{page}/daily/{START}/{END}"
    )

    response = requests.get(
        url,
        headers={"User-Agent": "ad-decision-intelligence/1.0"},
        timeout=30,
    )
    response.raise_for_status()

    for item in response.json()["items"]:
        rows.append({
            "candidate": candidate,
            "date": item["timestamp"][:8],
            "pageviews": item["views"],
        })

df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

df.to_csv(
    "data/processed/2025_mayor_wikipedia_attention.csv",
    index=False,
)

print("Rows:", len(df))
print(df.groupby("candidate")["pageviews"].sum())