import pandas as pd

# Load the Excel file
file_path = "cpus.xlsx"
df = pd.read_excel(file_path)

# Clean and filter the data
df_clean = df.copy()
df_clean = df_clean.dropna(subset=["Score", "Score/EUR"])
df_clean = df_clean[df_clean["Score/EUR"] > 0]

df_clean["Score Rank"] = df_clean["Score"].rank(ascending=False, method="min")
df_clean["Score/EUR Rank"] = df_clean["Score/EUR"].rank(ascending=False, method="min")

df_clean["Total Rank"] = df_clean["Score Rank"] + df_clean["Score/EUR Rank"]
df_ranked = df_clean.sort_values(by=["Total Rank", "Score"], ascending=[True, False])

df_ranked.to_excel("ranked_cpus.xlsx", index=False)
print("\nData has been analysed and exported to 'ranked_cpus.xlsx'.")