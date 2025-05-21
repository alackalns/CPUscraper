import pandas as pd

# Load the Excel file
file_path = "cpus.xlsx"  # Update path if needed
df = pd.read_excel(file_path)

# Clean and filter the data
df_clean = df.copy()
df_clean = df_clean.dropna(subset=["Score", "Score/EUR"])
df_clean = df_clean[df_clean["Score/EUR"] > 0]

# Step 1: Rank based on benchmark score (higher is better)
df_clean["Score Rank"] = df_clean["Score"].rank(ascending=False, method="min")

# Step 2: Rank based on score per euro (higher is better)
df_clean["Score/EUR Rank"] = df_clean["Score/EUR"].rank(ascending=False, method="min")

# Step 3: Total rank is the sum of both ranks
df_clean["Total Rank"] = df_clean["Score Rank"] + df_clean["Score/EUR Rank"]

# Step 4: Sort by total rank, then by benchmark score (descending)
df_ranked = df_clean.sort_values(by=["Total Rank", "Score"], ascending=[True, False])

# Optional: Save to Excel
df_ranked.to_excel("ranked_cpus.xlsx", index=False)

# Show top 10
print(df_ranked[["CPU Name", "Score", "Score/EUR", "Score Rank", "Score/EUR Rank", "Total Rank"]].head(10))
