import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv("players_data_light-2026_2027.csv")
df = df[(df["90s"] >= 2.5) & (df["Pos"] != "GK")].copy()
df = df[df["Pos"].str.contains("MF", na=False)]
df["Gls_90"] = df["Gls"] / df["90s"]
df["Ast_90"] = df["Ast"] / df["90s"]
df["Crs_90"] = df["Crs"] / df["90s"]

cols = ["Gls_90", "Ast_90", "Sh/90", "SoT/90", "Crs_90"]
df = df.dropna(subset=cols).reset_index(drop=True)

X = StandardScaler().fit_transform(df[cols])
modelo = NearestNeighbors(n_neighbors=6).fit(X)

nombre = input("Jugador: ")
i = df.index[df["Player"] == nombre][0]
_, vecinos = modelo.kneighbors(X[[i]])
print(df.loc[vecinos[0][1:], ["Player", "Squad", "Pos"]])