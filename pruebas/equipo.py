import pandas as pd

df = pd.read_csv("players_data_light-2026_2027.csv")

barca = df[df["Squad"] == "Barcelona"]
print(barca[["Player", "Pos", "Gls", "Ast", "90s"]])