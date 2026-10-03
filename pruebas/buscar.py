import pandas as pd

df = pd.read_csv("players_data_light-2026_2027.csv")
print(df[df["Player"].str.contains("Lorenzo", na=False)][["Player", "Pos", "90s"]])