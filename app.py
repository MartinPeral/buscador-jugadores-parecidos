import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


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

grupo = df["Pos"].str.contains(posicion, na=False) & (df["Player"] != nombre)
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