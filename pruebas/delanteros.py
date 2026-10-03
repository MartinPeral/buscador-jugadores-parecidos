import pandas as pd

df = pd.read_csv("players_data_light-2026_2027.csv")

df = df[df["Pos"].str.contains("FW", na=False) & (df["90s"] >= 3)]
df["Gls_90"] = df["Gls"] / df["90s"]
df["Ast_90"] = df["Ast"] / df["90s"]

top = df.sort_values("Gls_90", ascending=False)
print(top[["Player", "Squad", "Gls_90", "Ast_90"]].head(10))