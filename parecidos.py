import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv("players_data_light-2026_2027.csv")
df = df[df["90s"] >= 4].reset_index(drop=True)

excluir = ["Rk", "Age", "Born", "MP", "Starts", "Min", "90s"]
num = df.select_dtypes("number").drop(columns=excluir, errors="ignore")
num = num.dropna(axis=1, how="all").fillna(0)

conteos = [c for c in num.columns if "/" not in c and "%" not in c]
num[conteos] = num[conteos].div(df["90s"], axis=0)

nombre = input("Jugador: ")
posicion = input("Posición a comparar (FW, MF o DF): ").upper()

if nombre not in df["Player"].values:
    raise SystemExit("Jugador no encontrado (o con menos de 4 partidos de 90).")

grupo = df["Pos"].str.contains(posicion, na=False) & (df["Player"] != nombre)
scaler = StandardScaler().fit(num[grupo])
modelo = NearestNeighbors(n_neighbors=5).fit(scaler.transform(num[grupo]))

i = df.index[df["Player"] == nombre][0]
_, vecinos = modelo.kneighbors(scaler.transform(num.loc[[i]]))
print(df[grupo].iloc[vecinos[0]][["Player", "Squad", "Pos"]])