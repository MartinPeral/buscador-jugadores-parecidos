import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("players_data_light-2026_2027.csv")
df["Ast_90"] = df["Ast"] / df["90s"]

jugadores = ["Dani Olmo", "Paulo Dybala"]
datos = df[df["Player"].isin(jugadores)].set_index("Player")
datos = datos.loc[jugadores, ["Sh/90", "SoT/90", "Ast_90"]].T

datos.plot(kind="bar", color=["#e63946", "#1d3557"])
plt.title("Olmo vs. Dybala (por 90 minutos)")
plt.xticks(rotation=0)
plt.savefig("olmo_dybala.png")
plt.show()