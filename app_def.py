import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
import plotly.express as px
import plotly.graph_objects as go
import requests

# ---------------- 1. CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(page_title="ECVD - Saúde Cardiovascular", layout="wide", initial_sidebar_state="expanded")

# ---------------- 2. FUNÇÕES DO SISTEMA ----------------
@st.cache_data(show_spinner="A extrair dados populacionais da API do IBGE...")
def obter_populacao_ibge():
    url = "https://servicodados.ibge.gov.br/api/v3/agregados/4709/periodos/2022/variaveis/93?localidades=N6[all]"
    resposta = requests.get(url)
    dados_json = resposta.json()
    
    registos = []
    for serie in dados_json[0]['resultados'][0]['series']:
        cod_ibge = serie['localidade']['id']
        populacao = serie['serie']['2022']
        registos.append({
            "co_ibge_join": str(cod_ibge)[:6],
            "populacao": int(populacao)
        })
    return pd.DataFrame(registos)

@st.cache_data
def carregar_dados():
    df = pd.read_csv('dataset.csv', sep=',')
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    df["co_ibge"] = df["co_ibge"].astype(int)
    df["nu_ocorrencias_internacoes"] = pd.to_numeric(df["nu_ocorrencias_internacoes"], errors='coerce').fillna(0)
    df["nu_ocorrencias_ambulatorio"] = pd.to_numeric(df["nu_ocorrencias_ambulatorio"], errors='coerce').fillna(0)

    df_pop = obter_populacao_ibge()
    df['co_ibge_join'] = df['co_ibge'].astype(str).str[:6]
    df = df.merge(df_pop, on='co_ibge_join', how='left')
    
    df['populacao'] = df['populacao'].fillna(df['populacao'].median())

    df["taxa_internacoes"] = (df["nu_ocorrencias_internacoes"] / df["populacao"]) * 100000
    df["taxa_ambulatorio"] = (df["nu_ocorrencias_ambulatorio"] / df["populacao"]) * 100000

    df['geometry'] = df['mp_municipio'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry').set_crs(epsg=4326, inplace=False)
    gdf["id"] = gdf.index.astype(str)
    
    return gdf

def aplicar_filtro(gdf, estado, metrica, modo_analise):
    gdf_filtrado = gdf.copy()
    if estado != "Todos":
        gdf_filtrado = gdf_filtrado[gdf_filtrado["uf"] == estado].copy()
    
    prefixo = "taxa_" if modo_analise == "Taxa por 100 mil hab. (Recomendado)" else "nu_ocorrencias_"
    
    if metrica == "Internações":
        gdf_filtrado["valor"] = gdf_filtrado[f"{prefixo}internacoes"].fillna(0)
        escala = "Reds"
    elif metrica == "Ambulatórios":
        gdf_filtrado["valor"] = gdf_filtrado[f"{prefixo}ambulatorio"].fillna(0)
        escala = "Blues"
    else:
        gdf_filtrado["valor"] = (
            gdf_filtrado[f"{prefixo}internacoes"].fillna(0) + 
            gdf_filtrado[f"{prefixo}ambulatorio"].fillna(0)
        )
        escala = "Purples"
    return gdf_filtrado, escala

def plotar_mapa(gdf_filtrado, escala, municipio_destacado=None, modo_analise=None):
    if len(gdf_filtrado) == 0:
        fig = go.Figure()
        fig.update_layout(title="Sem dados para exibir")
        return fig
    
    titulo_legenda = "Taxa / 100k hab." if modo_analise == "Taxa por 100 mil hab. (Recomendado)" else "Ocorrências (Absoluto)"

    geojson = gdf_filtrado.__geo_interface__
    fig = px.choropleth(
        gdf_filtrado,
        geojson=geojson,
        locations="id",
        featureidkey="properties.id",
        color="valor",
        hover_name="no_municipio",
        hover_data={
            "populacao": ":.0f",
            "nu_ocorrencias_internacoes": ":.0f",
            "taxa_internacoes": ":.1f",
            "id": False,
            "valor": False
        },
        color_continuous_scale=escala,
        color_continuous_midpoint=gdf_filtrado["valor"].median()
    )

    if municipio_destacado and municipio_destacado != "Todos":
        dados_mun = gdf_filtrado[gdf_filtrado["no_municipio"] == municipio_destacado]
        if not dados_mun.empty:
            geom = dados_mun.geometry.iloc[0]
            minx, miny, maxx, maxy = geom.bounds
            fig.update_geos(
                projection_type="mercator",
                lonaxis=dict(range=[minx, maxx]), lataxis=dict(range=[miny, maxy]),
                showcountries=True, showcoastlines=True, showland=True,
                landcolor="rgb(245,245,245)", countrycolor="gray", coastlinecolor="gray"
            )
    else:
        fig.update_geos(
            projection_type="mercator",
            lonaxis=dict(range=[-73.99, -28.83]), lataxis=dict(range=[-33.77, 5.27]),
            showcountries=True, showcoastlines=True, showland=True,
            landcolor="rgb(245,245,245)", countrycolor="gray", coastlinecolor="gray"
        )
    
    fig.update_layout(
        height=600, margin={"r":0, "t":0, "l":0, "b":0},
        coloraxis_colorbar=dict(title=titulo_legenda, thickness=15, len=1),
        clickmode='event+select'
    )
    return fig

# ---------------- 3. INÍCIO DO APLICATIVO E SESSÃO ----------------
try:
    gdf = carregar_dados()
except FileNotFoundError:
    st.error("🚨 O ficheiro 'dataset.csv' não foi encontrado!")
    st.stop()

if "municipio_selecionado" not in st.session_state:
    st.session_state.municipio_selecionado = "Todos"
if "estado_anterior" not in st.session_state:
    st.session_state.estado_anterior = "Todos"

st.title("🫀 Estudo de Caso: Saúde Cardiovascular no Brasil (2025)")
st.markdown("---")

# ---------------- 4. MENU LATERAL (SIDEBAR) ----------------
st.sidebar.header("🔧 Filtros do Dashboard")
estado_options = ["Todos"] + sorted(gdf["uf"].dropna().unique().tolist())
estado_sel = st.sidebar.selectbox("Estado", estado_options, key="estado_key")
metrica = st.sidebar.radio("Métrica", ["Internações", "Ambulatórios", "Ambos"], key="metrica_key")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧬 Rigor Analítico")
modo_analise = st.sidebar.radio(
    "Modo de Visualização", 
    ["Taxa por 100 mil hab. (Recomendado)", "Números Absolutos"],
    help="Números absolutos destacam cidades populosas. A taxa por 100 mil habitantes revela o risco real proporcional em cada região."
)

if estado_sel != st.session_state.estado_anterior:
    st.session_state.municipio_selecionado = "Todos"
    st.session_state.estado_anterior = estado_sel

gdf_filtrado, escala = aplicar_filtro(gdf, estado_sel, metrica, modo_analise)

# ---------------- 5. ESTRUTURA DE ABAS ----------------
aba_doc, aba_mapa, aba_rank = st.tabs(["📝 Relatório do Projeto", "🗺️ Mapa Interativo", "📊 Análise e Ranking"])

# ==========================================
# ABA 1: DOCUMENTAÇÃO 
# ==========================================
with aba_doc:
    st.header("Documentação do Projeto")
    
    col_texto1, col_texto2 = st.columns(2)
    
    with col_texto1:
        st.subheader("1. Escopo e Desafio")
        st.write("O projeto mapeia as internações hospitalares e atendimentos ambulatoriais causados por doenças cardiovasculares em 2025. O desafio principal é identificar aglomerados geográficos com incidência anormal (outliers) e fornecer dados claros para a gestão de saúde pública.")
        
        st.subheader("2. Rigor Técnico e Tratamento de Dados (ETL)")
        st.success("**Diferencial do Projeto:** Para evitar o enviesamento populacional (onde cidades maiores parecem sempre piores em números absolutos), a aplicação consome a **API do IBGE em tempo real** para baixar dados do Censo 2022. É calculada a taxa de incidência por 100 mil habitantes, permitindo uma comparação científica e proporcional entre os municípios.")
        
        st.subheader("3. Representação Visual")
        st.write("O mapa coroplético possui navegação interativa e zoom, respondendo ativamente à seleção da métrica. O painel inclui também uma matriz de risco (scatter plot) para correlação bivariada entre prevenção e urgência.")

    with col_texto2:
        st.subheader("4. Principais Conclusões (Takeaways)")
        st.markdown("""
        * **O Perigo do Viés Populacional:** A análise comprovou que olhar apenas para números absolutos cria um "ponto cego" na gestão. Ao calcularmos a taxa por 100 mil habitantes, descobrimos que epidemias silenciosas estão muitas vezes escondidas em municípios de pequeno porte.
        * **O Alerta da Atenção Básica (Prevenção vs. Urgência):** A Matriz de Risco revelou um padrão alarmante: cidades com baixo volume de atendimentos ambulatoriais (prevenção) frequentemente lideram as taxas de internações (urgência). Isso indica que o paciente só tem contato com o SUS quando a doença já está em estágio crítico.
        * **Inteligência na Alocação de Recursos:** Em vez de distribuir verbas de forma linear, gestores podem usar este painel para direcionar recursos financeiros, campanhas de conscientização e mutirões de exames para as "zonas vermelhas" de maior risco proporcional.
        """)

# ==========================================
# ABA 2: MAPA INTERATIVO
# ==========================================
with aba_mapa:
    st.markdown("### Visão Espacial da Saúde")
    col1, col2, col3 = st.columns(3)
    col1.metric("Municípios Filtrados", len(gdf_filtrado))
    col2.metric("Total de Internações", f"{gdf_filtrado['nu_ocorrencias_internacoes'].sum():,.0f}".replace(',','.'))
    col3.metric("População Abrangida", f"{gdf_filtrado['populacao'].sum():,.0f}".replace(',','.'))
    st.markdown("---")
    
    municipio_options = ["Todos"] + sorted(gdf_filtrado["no_municipio"].dropna().unique().tolist())
    if st.session_state.municipio_selecionado not in municipio_options:
        st.session_state.municipio_selecionado = "Todos"

    indice_atual = municipio_options.index(st.session_state.municipio_selecionado)
    municipio_sel = st.selectbox("🔍 Buscar Município Específico", municipio_options, index=indice_atual)

    if municipio_sel != st.session_state.municipio_selecionado:
        st.session_state.municipio_selecionado = municipio_sel
        st.rerun()

    col_mapa_plot, col_info_plot = st.columns([2.5, 1])
    
    with col_mapa_plot:
        mun_destaque = None if st.session_state.municipio_selecionado == "Todos" else st.session_state.municipio_selecionado
        fig = plotar_mapa(gdf_filtrado, escala, mun_destaque, modo_analise)
        evento = st.plotly_chart(fig, use_container_width=True, key="mapa_chart", on_select="rerun")
        
        if evento and hasattr(evento, 'selection') and evento.selection.points:
            ponto_clicado = evento.selection.points[0]
            if "location" in ponto_clicado:
                id_clicado = str(ponto_clicado["location"])
                mun_filtrado = gdf_filtrado[gdf_filtrado["id"] == id_clicado]
                if not mun_filtrado.empty:
                    municipio_clicado = mun_filtrado["no_municipio"].iloc[0]
                    if st.session_state.municipio_selecionado != municipio_clicado:
                        st.session_state.municipio_selecionado = municipio_clicado
                        st.rerun()
    
    with col_info_plot:
        st.markdown("### 📍 Detalhes Locais")
        if st.session_state.municipio_selecionado != "Todos":
            dados_mun = gdf_filtrado[gdf_filtrado["no_municipio"] == st.session_state.municipio_selecionado]
            if not dados_mun.empty:
                dados = dados_mun.iloc[0]
                st.markdown(f"**🏙️ {st.session_state.municipio_selecionado}**")
                st.write(f"👥 População: **{dados['populacao']:,.0f}**".replace(',','.'))
                st.metric("Internações (Absoluto)", f"{dados['nu_ocorrencias_internacoes']:,.0f}".replace(',','.'))
                st.metric("Taxa / 100k hab.", f"{dados['taxa_internacoes']:,.1f}".replace(',','.'))
            else:
                st.warning("Município não encontrado")
        else:
            st.info("👆 Clica numa cidade no ecrã do mapa para ver o detalhe de risco.")

# ==========================================
# ABA 3: RANKING E MATRIZ DE RISCO
# ==========================================
with aba_rank:
    st.markdown("### Top 10 Zonas de Alerta")
    
    col_g1, col_g2 = st.columns(2)
    ordem_var_int = "taxa_internacoes" if modo_analise == "Taxa por 100 mil hab. (Recomendado)" else "nu_ocorrencias_internacoes"
    ordem_var_amb = "taxa_ambulatorio" if modo_analise == "Taxa por 100 mil hab. (Recomendado)" else "nu_ocorrencias_ambulatorio"
    
    with col_g1:
        st.markdown("#### Maiores Vítimas (Internações)")
        top_int = gdf_filtrado.nlargest(10, ordem_var_int)
        fig_int = px.bar(
            top_int, 
            x=ordem_var_int, 
            y='no_municipio', 
            orientation='h', 
            color=ordem_var_int, 
            color_continuous_scale='Reds', 
            labels={ordem_var_int: 'Internações', 'no_municipio': ''}
        )
        fig_int.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_int, use_container_width=True)
        
    with col_g2:
        st.markdown("#### Maior Demanda (Ambulatórios)")
        top_amb = gdf_filtrado.nlargest(10, ordem_var_amb)
        fig_amb = px.bar(
            top_amb, 
            x=ordem_var_amb, 
            y='no_municipio', 
            orientation='h', 
            color=ordem_var_amb, 
            color_continuous_scale='Blues', 
            labels={ordem_var_amb: 'Ambulatórios', 'no_municipio': ''}
        )
        fig_amb.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_amb, use_container_width=True)

    st.markdown("---")
    
    # MATRIZ DE RISCO (SCATTER PLOT)
    st.markdown("### 🎯 Matriz de Risco: Prevenção vs. Agravamento")
    st.info("**💡 Insight Analítico:** Municípios no quadrante superior esquerdo (altas internações e baixos atendimentos ambulatoriais) indicam possíveis falhas na **saúde preventiva**. Os pacientes não estão recebendo acompanhamento primário e chegam ao sistema já em estado grave. Este é um alvo prioritário para políticas públicas.")
    
    fig_scatter = px.scatter(
        gdf_filtrado,
        x=ordem_var_amb,
        y=ordem_var_int,
        hover_name="no_municipio",
        hover_data={"populacao": ":.0f"},
        size="populacao" if modo_analise == "Taxa por 100 mil hab. (Recomendado)" else None,
        color=ordem_var_int,
        color_continuous_scale="Purples",
        labels={
            ordem_var_amb: "Atendimentos Ambulatoriais (Prevenção)",
            ordem_var_int: "Internações Hospitalares (Urgência)"
        },
        height=500
    )
    
    fig_scatter.update_layout(
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        xaxis=dict(showgrid=True, gridcolor='white'),
        yaxis=dict(showgrid=True, gridcolor='white')
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)