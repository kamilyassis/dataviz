import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Saúde Cardiovascular", layout="wide")

st.title("🫀 Saúde Cardiovascular no Brasil (2025)")
st.markdown("---")

# ---------------- CACHE ----------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv('data/dataset.csv')

    # remover coluna lixo
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # garantir tipos corretos
    df["co_ibge"] = df["co_ibge"].astype(int)
    df["nu_ocorrencias_internacoes"] = pd.to_numeric(df["nu_ocorrencias_internacoes"])
    df["nu_ocorrencias_ambulatorio"] = pd.to_numeric(df["nu_ocorrencias_ambulatorio"])

    # geometria
    df['geometry'] = df['mp_municipio'].apply(wkt.loads)

    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf = gdf.set_crs(epsg=4326)

    # ID único (ESSENCIAL pro mapa)
    gdf["id"] = gdf.index.astype(str)

    return gdf

gdf = carregar_dados()

# ---------------- SESSION STATE ----------------
if "municipio" not in st.session_state:
    st.session_state.municipio = None

# ---------------- FILTROS TOPO ----------------
col_filtro1, col_filtro2 = st.columns([2,1])

with col_filtro1:
    estados = ["Todos"] + sorted(gdf["uf"].unique())
    estado_sel = st.selectbox("Estado", estados)

with col_filtro2:
    metrica = st.radio("Métrica", ["Internações", "Ambulatórios", "Ambos"])

# ---------------- FILTRO ----------------
if estado_sel != "Todos":
    gdf_filtrado = gdf[gdf["uf"] == estado_sel].copy()
else:
    gdf_filtrado = gdf.copy()

# ---------------- MÉTRICA ----------------
if metrica == "Internações":
    gdf_filtrado["valor"] = gdf_filtrado["nu_ocorrencias_internacoes"]
    escala = "Reds"
elif metrica == "Ambulatórios":
    gdf_filtrado["valor"] = gdf_filtrado["nu_ocorrencias_ambulatorio"]
    escala = "Blues"
else:
    gdf_filtrado["valor"] = (
        gdf_filtrado["nu_ocorrencias_internacoes"] +
        gdf_filtrado["nu_ocorrencias_ambulatorio"]
    )
    escala = "Purples"

# ---------------- MÉTRICAS ----------------
col1, col2, col3 = st.columns(3)
col1.metric("Municípios", len(gdf_filtrado))
col2.metric("Internações", f"{gdf_filtrado['nu_ocorrencias_internacoes'].sum():,.0f}")
col3.metric("Ambulatórios", f"{gdf_filtrado['nu_ocorrencias_ambulatorio'].sum():,.0f}")

st.markdown("---")

# ---------------- SELECT MUNICÍPIO ----------------
municipio_opcoes = ["Todos"] + sorted(gdf_filtrado["no_municipio"].unique())

municipio_sel = st.selectbox(
    "Município",
    municipio_opcoes,
    index=municipio_opcoes.index(st.session_state.municipio)
    if st.session_state.municipio in municipio_opcoes else 0
)

if municipio_sel != "Todos":
    st.session_state.municipio = municipio_sel
else:
    st.session_state.municipio = None
# ---------------- LAYOUT PRINCIPAL ----------------
col_mapa, col_info = st.columns([2, 1])

with col_mapa:

    geojson_filtrado = gdf_filtrado.__geo_interface__

    fig = px.choropleth(
        gdf_filtrado,
        geojson=geojson_filtrado,
        locations="id",
        featureidkey="properties.id",
        color="valor",
        hover_name="no_municipio",
        hover_data={
            "nu_ocorrencias_internacoes": True,
            "nu_ocorrencias_ambulatorio": True
        },
        color_continuous_scale=escala
    )

    # 🌍 MAPA BASE VISÍVEL (mundi)
    fig.update_geos(
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor="rgb(240,240,240)",
        countrycolor="gray"
    )

    # 🎯 ZOOM SUAVE
    if st.session_state.municipio:
        geom = gdf_filtrado[
            gdf_filtrado["no_municipio"] == st.session_state.municipio
        ].geometry.iloc[0]

        fig.update_geos(
            center=dict(lat=geom.centroid.y, lon=geom.centroid.x),
            projection_scale=10
        )
    else:
        fig.update_geos(fitbounds="locations")

    fig.update_layout(
        height=600,
        margin={"r":0,"t":0,"l":0,"b":0},
        transition={"duration": 800, "easing": "quad-in-out"}  # mais suave
    )

    evento = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

    # ---------------- CLICK ----------------
    if evento and evento.selection.points:
        point = evento.selection.points[0]

        if "location" in point:
            id_clicado = point["location"]

            municipio_clicado = gdf_filtrado[
                gdf_filtrado["id"] == id_clicado
            ]["no_municipio"].iloc[0]

            st.session_state.municipio = municipio_clicado
            st.rerun()

# ---------------- PAINEL DIREITA ----------------
with col_info:

    st.markdown("### 📍 Informações")

    st.markdown(f"**Estado:** {estado_sel}")

    if st.session_state.municipio:
        dados = gdf_filtrado[
            gdf_filtrado["no_municipio"] == st.session_state.municipio
        ].iloc[0]

        st.markdown(f"**Município:** {st.session_state.municipio}")

        st.metric(
            "Internações",
            f"{dados['nu_ocorrencias_internacoes']:,.0f}"
        )

        st.metric(
            "Ambulatórios",
            f"{dados['nu_ocorrencias_ambulatorio']:,.0f}"
        )

    else:
        st.info("Selecione um município no mapa")

    st.markdown("---")

    # 📊 Ranking compacto
    st.markdown("### Top Municípios")

    top5 = gdf_filtrado.sort_values("valor", ascending=False).head(5)

    for _, row in top5.iterrows():
        st.write(f"{row['no_municipio']} — {int(row['valor'])}")

# ---------------- RANKING ----------------
st.markdown("### Top 10 Municípios")

top10 = gdf_filtrado.sort_values("valor", ascending=False).head(10)

fig_bar = px.bar(
    top10,
    x="no_municipio",
    y="valor"
)

st.plotly_chart(fig_bar, use_container_width=True)