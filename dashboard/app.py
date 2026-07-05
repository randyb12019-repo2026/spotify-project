# Guardar como app.py y lanzar con: streamlit run app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #121212 0%, #191414 70%, #000000 100%);
    color: white;
}

h1, h2, h3, h4, h5, h6, p, label, span {
    color: white !important;
}

[data-testid="stSidebar"] {
    background-color: #000000;
}

div[data-testid="stMetric"] {
    background-color: #181818;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #282828;
}

.spotify-title {
    color: #1DB954;
    font-size: 46px;
    font-weight: 900;
    margin-bottom: 5px;
}

.spotify-subtitle {
    color: #b3b3b3;
    font-size: 18px;
    margin-bottom: 25px;
}

.insight-card {
    background-color: #181818;
    padding: 16px;
    border-left: 5px solid #1DB954;
    border-radius: 12px;
    margin-bottom: 25px;
    color: #b3b3b3;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    return pd.read_pickle("dataset/dataset_analitico_limpio.pkl")


df = load_data()

st.markdown(
    '<div class="spotify-title">Spotify Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="spotify-subtitle">Análisis interactivo de canciones, artistas, popularidad, energía y seguidores.</div>',
    unsafe_allow_html=True
)

st.sidebar.title("Filtros")

rango_anios = st.sidebar.slider(
    "Año de lanzamiento",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (int(df["release_year"].min()), int(df["release_year"].max()))
)

popularidad_min = st.sidebar.slider(
    "Popularidad mínima",
    0,
    100,
    0
)

contenido = st.sidebar.selectbox(
    "Contenido explícito",
    ["Todos", "Sí", "No"]
)

df_f = df[
    (df["release_year"] >= rango_anios[0]) &
    (df["release_year"] <= rango_anios[1]) &
    (df["track_popularity"] >= popularidad_min)
]

if contenido == "Sí":
    df_f = df_f[df_f["explicit"] == True]
elif contenido == "No":
    df_f = df_f[df_f["explicit"] == False]

st.subheader("Métricas principales")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Canciones", f"{len(df_f):,}")
col2.metric("Artistas", f"{df_f['id_artists'].nunique():,}")
col3.metric("Popularidad media", round(df_f["track_popularity"].mean(), 2))
col4.metric("Energía media", round(df_f["energy"].mean(), 2))

st.subheader("Visualizaciones principales")

fig1 = px.histogram(
    df_f,
    x="track_popularity",
    nbins=30,
    title="Distribución de popularidad de canciones",
    template="plotly_dark",
    labels={"track_popularity": "Popularidad"}
)

fig1.update_layout(
    paper_bgcolor="#181818",
    plot_bgcolor="#181818",
    font_color="white",
    title_font_color="#1DB954"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
<div class="insight-card">
Este gráfico muestra cómo se distribuye la popularidad de las canciones.
Permite observar si predominan canciones con popularidad baja, media o alta dentro del rango seleccionado.
</div>
""", unsafe_allow_html=True)

fig2 = px.scatter(
    df_f,
    x="energy",
    y="track_popularity",
    opacity=0.35,
    title="Relación entre energía y popularidad",
    template="plotly_dark",
    labels={
        "energy": "Energía",
        "track_popularity": "Popularidad"
    }
)

fig2.update_layout(
    paper_bgcolor="#181818",
    plot_bgcolor="#181818",
    font_color="white",
    title_font_color="#1DB954"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class="insight-card">
Este gráfico permite analizar si las canciones con mayor energía tienden también a tener mayor popularidad.
En el análisis exploratorio no se observa una relación lineal fuerte entre ambas variables.
</div>
""", unsafe_allow_html=True)

canciones_anio = (
    df_f.groupby("release_year")
    .size()
    .reset_index(name="cantidad")
)

fig3 = px.line(
    canciones_anio,
    x="release_year",
    y="cantidad",
    title="Cantidad de canciones por año",
    template="plotly_dark",
    labels={
        "release_year": "Año",
        "cantidad": "Cantidad de canciones"
    }
)

fig3.update_traces(line_color="#1DB954")

fig3.update_layout(
    paper_bgcolor="#181818",
    plot_bgcolor="#181818",
    font_color="white",
    title_font_color="#1DB954"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
<div class="insight-card">
Este gráfico muestra la evolución temporal del número de canciones.
Permite identificar los años o periodos con mayor presencia de canciones dentro del dataset.
</div>
""", unsafe_allow_html=True)

top_artistas = (
    df_f.groupby("artist_name")["followers"]
    .max()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_artistas,
    x="followers",
    y="artist_name",
    orientation="h",
    title="Top 10 artistas con más seguidores",
    template="plotly_dark",
    labels={
        "followers": "Seguidores",
        "artist_name": "Artista"
    }
)

fig4.update_traces(marker_color="#1DB954")

fig4.update_layout(
    paper_bgcolor="#181818",
    plot_bgcolor="#181818",
    font_color="white",
    title_font_color="#1DB954",
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
<div class="insight-card">
Este gráfico muestra los artistas con mayor cantidad de seguidores.
Se observa una concentración importante de seguidores en un grupo reducido de artistas destacados.
</div>
""", unsafe_allow_html=True)

st.subheader("Conclusiones")

st.markdown("""
- La popularidad de las canciones se concentra principalmente en valores bajos y medios.
- El volumen de canciones aumenta en años recientes.
- No se observa una relación lineal fuerte entre energía y popularidad.
- Los seguidores se concentran en un grupo reducido de artistas destacados.
""")