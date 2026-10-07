import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt


@st.cache_data
def cargar(minimo):
    df = pd.read_csv("players_data_light-2026_2027.csv")
    df = df[df["90s"] >= minimo].reset_index(drop=True)
    excluir = ["Rk", "Age", "Born", "MP", "Starts", "Min", "90s"]
    num = df.select_dtypes("number").drop(columns=excluir, errors="ignore")
    num = num.dropna(axis=1, how="all").fillna(0)
    conteos = [c for c in num.columns if "/" not in c and "%" not in c]
    num[conteos] = num[conteos].div(df["90s"], axis=0)
    return df, num

minimo = st.slider("Mínimo de partidos de 90 minutos", 1, 10, 4)
df, num = cargar(minimo)

st.title("Buscador de jugadores parecidos")
nombre = st.selectbox("Jugador", sorted(df["Player"].unique()))
posicion = st.selectbox("Posición a comparar", ["FW", "MF", "DF"])
ligas = sorted(df["Comp"].unique())
elegidas = st.multiselect("Ligas con las que comparar", ligas, default=ligas)

grupo = df["Pos"].str.contains(posicion, na=False) & (df["Player"] != nombre) & df["Comp"].isin(elegidas)

if grupo.sum() < 5:
    st.warning("Hay menos de 5 jugadores con esos filtros. Amplía ligas o baja el mínimo de partidos.")
    st.stop()
scaler = StandardScaler().fit(num[grupo])
modelo = NearestNeighbors(n_neighbors=5).fit(scaler.transform(num[grupo]))

i = df.index[df["Player"] == nombre][0]
_, vecinos = modelo.kneighbors(scaler.transform(num.loc[[i]]))

st.subheader(f"Los 5 {posicion} más parecidos a {nombre}")
st.dataframe(df[grupo].iloc[vecinos[0]][["Player", "Squad", "Pos"]])

mas_parecido = df[grupo].index[vecinos[0][0]]
metricas = ["Gls", "Ast", "Sh/90", "SoT/90", "Crs", "TklW", "Int"]

comp = num.loc[[i, mas_parecido], metricas]
comp.index = [nombre, df.loc[mas_parecido, "Player"]]

st.subheader("Comparativa por 90 minutos")
st.bar_chart(comp.T, stack=False, color=["#e63946", "#1d3557"])

ref = num[grupo | (df.index == i)][metricas].rank(pct=True)
valores_a = ref.loc[i].tolist()
valores_b = ref.loc[mas_parecido].tolist()

angulos = np.linspace(0, 2 * np.pi, len(metricas), endpoint=False).tolist()
angulos += angulos[:1]
valores_a += valores_a[:1]
valores_b += valores_b[:1]

fig, ax = plt.subplots(subplot_kw={"polar": True})
ax.plot(angulos, valores_a, color="#e63946", label=nombre)
ax.fill(angulos, valores_a, color="#e63946", alpha=0.25)
ax.plot(angulos, valores_b, color="#1d3557", label=df.loc[mas_parecido, "Player"])
ax.fill(angulos, valores_b, color="#1d3557", alpha=0.25)
ax.set_xticks(angulos[:-1])
ax.set_xticklabels(metricas)
ax.set_ylim(0, 1)
ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1))

st.subheader("Radar (percentil dentro del grupo comparado)")
st.pyplot(fig)