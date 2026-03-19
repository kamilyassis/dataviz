import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
import plotly.express as px
import plotly.graph_objects as go

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Saúde Cardiovascular", layout="wide", initial_sidebar_state="expanded")

st.title("🫀 Saúde Cardiovascular no Brasil (2025)")
st.markdown("---")

# ---------------- FUNÇÕES ----------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv('data/dataset.csv')
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    df["co_ibge"] = df["co_ibge"].astype(int)
    df["nu_ocorrencias_internacoes"] = pd.to_numeric(df["nu_ocorrencias_internacoes"], errors='coerce')
    df["nu_ocorrencias_ambulatorio"] = pd.to_numeric(df["nu_ocorrencias_ambulatorio"], errors='coerce')

    df['geometry'] = df['mp_municipio'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry').set_crs(epsg=4326, inplace=False)
    gdf["id"] = gdf.index.astype(str)
    return gdf

def aplicar_filtro(gdf, estado, metrica):
    gdf_filtrado = gdf.copy()
    if estado != "Todos":
        gdf_filtrado = gdf_filtrado[gdf_filtrado["uf"] == estado].copy()
    
    if metrica == "Internações":
        gdf_filtrado["valor"] = gdf_filtrado["nu_ocorrencias_internacoes"].fillna(0)
        escala = "Reds"
    elif metrica == "Ambulatórios":
        gdf_filtrado["valor"] = gdf_filtrado["nu_ocorrencias_ambulatorio"].fillna(0)
        escala = "Blues"
    else:
        gdf_filtrado["valor"] = (
            gdf_filtrado["nu_ocorrencias_internacoes"].fillna(0) + 
            gdf_filtrado["nu_ocorrencias_ambulatorio"].fillna(0)
        )
        escala = "Purples"
    return gdf_filtrado, escala

def plotar_mapa(gdf_filtrado, escala, municipio_destacado=None):
    if len(gdf_filtrado) == 0:
        fig = go.Figure()
        fig.update_layout(title="Sem dados para exibir")
        return fig
    
    geojson = gdf_filtrado.__geo_interface__
    fig = px.choropleth(
        gdf_filtrado,
        geojson=geojson,
        locations="id",
        featureidkey="properties.id",
        color="valor",
        hover_name="no_municipio",
        hover_data={
            "nu_ocorrencias_internacoes": ":.0f",
            "nu_ocorrencias_ambulatorio": ":.0f",
            "id": False,
            "valor": False
        },
        color_continuous_scale=escala,
        color_continuous_midpoint=gdf_filtrado["valor"].median()
    )

    
    # Define zoom baseado na seleção
    if municipio_destacado:
        dados_mun = gdf_filtrado[gdf_filtrado["no_municipio"] == municipio_destacado]
        if not dados_mun.empty:
            geom = dados_mun.geometry.iloc[0]
            minx, miny, maxx, maxy = geom.bounds
            fig.update_geos(
                projection_type="mercator",
                lonaxis=dict(range=[minx, maxx]),
                lataxis=dict(range=[miny, maxy]),
                showcountries=True,
                showcoastlines=True,
                showland=True,
                landcolor="rgb(245,245,245)",
                countrycolor="gray",
                coastlinecolor="gray"
            )
    else:
        # Vista geral do Brasil
        fig.update_geos(
            projection_type="mercator",
            lonaxis=dict(range=[-73.99, -28.83]),
            lataxis=dict(range=[-33.77, 5.27]),
            showcountries=True,
            showcoastlines=True,
            showland=True,
            landcolor="rgb(245,245,245)",
            countrycolor="gray",
            coastlinecolor="gray"
        )
    
    fig.update_layout(
        height=600,
        margin={"r":0, "t":0, "l":0, "b":0},
        coloraxis_colorbar=dict(title="Ocorrências", thickness=15, len=1),
        clickmode='event+select'
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>" +
            "Internações: %{customdata[0]:,.0f}<br>" +
            "Ambulatórios: %{customdata[1]:,.0f}<br>" +
            "<extra></extra>"
        )
    )
    return fig

def gerar_insights(gdf_filtrado):
    if len(gdf_filtrado) == 0:
        return {"top_nome": "N/A", "top_valor": 0, "media": 0, "total": 0}
    top = gdf_filtrado.loc[gdf_filtrado["valor"].idxmax()]
    media = gdf_filtrado["valor"].mean()
    total = gdf_filtrado["valor"].sum()
    return {"top_nome": top["no_municipio"], "top_valor": int(top["valor"]), "media": int(media), "total": int(total)}

# ---------------- APP ----------------
try:
    gdf = carregar_dados()
except FileNotFoundError:
    st.error("Arquivo 'data/dataset.csv' não encontrado!")
    st.stop()

if "municipio_selecionado" not in st.session_state:
    st.session_state.municipio_selecionado = None
if "estado_anterior" not in st.session_state:
    st.session_state.estado_anterior = "Todos"

# SIDEBAR
st.sidebar.header("🔧 Filtros")
estado_options = ["Todos"] + sorted(gdf["uf"].unique().tolist())
estado_sel = st.sidebar.selectbox("Estado", estado_options, key="estado_key")
metrica = st.sidebar.radio("Métrica", ["Internações", "Ambulatórios", "Ambos"], key="metrica_key")

if estado_sel != st.session_state.estado_anterior:
    st.session_state.municipio_selecionado = None
    st.session_state.estado_anterior = estado_sel

gdf_filtrado, escala = aplicar_filtro(gdf, estado_sel, metrica)

# MÉTRICAS GLOBAIS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Municípios", len(gdf_filtrado))
col2.metric("Internações", f"{gdf_filtrado['nu_ocorrencias_internacoes'].sum():,.0f}")
col3.metric("Ambulatórios", f"{gdf_filtrado['nu_ocorrencias_ambulatorio'].sum():,.0f}")

st.markdown("---")

# MUNICÍPIO
municipio_options = ["Todos"] + sorted(gdf_filtrado["no_municipio"].dropna().unique().tolist())
selected_index = 0
if (st.session_state.municipio_selecionado and st.session_state.municipio_selecionado in municipio_options):
    selected_index = municipio_options.index(st.session_state.municipio_selecionado)

municipio_sel = st.selectbox("🔍 Município", municipio_options, index=selected_index, key="municipio_key")
st.session_state.municipio_selecionado = None if municipio_sel == "Todos" else municipio_sel

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["🗺️ Mapa Interativo", "📊 Ranking"])

with tab1:
    col_mapa, col_info = st.columns([2.5, 1])
    with col_mapa:
        fig = plotar_mapa(gdf_filtrado, escala, st.session_state.municipio_selecionado)
        selected_points = st.plotly_chart(fig, use_container_width=True, key="mapa_chart")
    
    with col_info:
        st.subheader("📍 Detalhes")
        if st.session_state.municipio_selecionado:
            dados_mun = gdf_filtrado[gdf_filtrado["no_municipio"] == st.session_state.municipio_selecionado]
            if not dados_mun.empty:
                dados = dados_mun.iloc[0]
                total_mun = dados['nu_ocorrencias_internacoes'] + dados['nu_ocorrencias_ambulatorio']
                st.markdown(f"**🏙️ {st.session_state.municipio_selecionado}**")
                col1, col2 = st.columns(2)
                col1.metric("Internações", f"{dados['nu_ocorrencias_internacoes']:,.0f}")
                col2.metric("Ambulatórios", f"{dados['nu_ocorrencias_ambulatorio']:,.0f}")        
            else:
                st.warning("Município não encontrado")
        else:
            st.info("👆 Selecione um município para ver detalhes")
with tab2:
    insights = gerar_insights(gdf_filtrado)
    if insights['top_nome'] != "N/A":
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏆 Top Município", insights['top_nome'])
            st.metric("Total Ocorrências", f"{insights['total']:,.0f}")
        with col2:
            st.metric("📊 Média", f"{insights['media']:,.0f}")
        
        # Top 10 gráficos
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            top_int = gdf_filtrado.nlargest(10, 'nu_ocorrencias_internacoes')
            fig_int = px.bar(
                top_int, x='nu_ocorrencias_internacoes', y='no_municipio',
                orientation='h', color='nu_ocorrencias_internacoes',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_int, use_container_width=True)
        
        with col_g2:
            top_amb = gdf_filtrado.nlargest(10, 'nu_ocorrencias_ambulatorio')
            fig_amb = px.bar(
                top_amb, x='nu_ocorrencias_ambulatorio', y='no_municipio',
                orientation='h', color='nu_ocorrencias_ambulatorio',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_amb, use_container_width=True)
    else:
        st.warning("Sem dados para exibir")
