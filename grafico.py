import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("players_data_light-2026_2027.csv")
df = df[df["90s"] >= 3]
df["Gls_90"] = df["Gls"] / df["90s"]
df["Ast_90"] = df["Ast"] / df["90s"]

jugadores = ["Raphinha", "Lamine Yamal"]
datos = df[df["Player"].isin(jugadores)].set_index("Player")

datos[["Gls_90", "Ast_90"]].T.plot(kind="bar", color=["#e63946", "#1d3557"])
plt.title("Goles y asistencias por 90")
plt.xticks(rotation=0)
plt.savefig("comparativa.png")
plt.show()