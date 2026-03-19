import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
import plotly.express as px

# 1. Configuração da Página (Layout mais largo e título)
st.set_page_config(page_title="ECVD", layout="wide", initial_sidebar_state="expanded")

# Título Principal
st.title("Estudo de Caso: Internações por Doenças Cardiovasculares(2025)")
st.markdown("---")

# 2. Carregamento de Dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv('data/dados.csv', sep=',') # Ajuste o sep se precisar
    df['geometry'] = df['mp_municipio'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.set_crs(epsg=4326, inplace=True)
    return gdf

gdf = carregar_dados()

# 3. Criando Abas para separar a Teoria da Prática
aba1, aba2 = st.tabs(["📝 Relatório do Projeto (ECVD)", "📊 Dashboard Interativo"])

# ==========================================
# ABA 1: DOCUMENTAÇÃO
# ==========================================
with aba1:
    st.header("Documentação do Projeto")
    
    col_texto1, col_texto2 = st.columns(2)
    
    with col_texto1:
        st.subheader("1. Escopo")
        st.write("O projeto analisa a saúde pública brasileira, focando no mapeamento das internações hospitalares causadas por doenças cardiovasculares em 2025. A base de dados do INDE(Infraestrutura Nacional de Dados Espaciais) contém registros em nível municipal (5.572 municípios), incluindo geometria espacial.")
        
        st.subheader("2. Desafio")
        st.write("Visualizar a distribuição espacial das internações no Brasil para identificar padrões de concentração. A pergunta norteadora é: *Existem aglomerados geográficos com incidência excepcionalmente alta de internações no território nacional?*")
        
        st.subheader("3. Projeto de Visualização")
        st.write("**Categoria:** Informativo e Explicativo.\n\n**Estratégia:** Desenvolvimento de um painel interativo contendo um Mapa Coroplético para visão macro e gráficos complementares para análise de extremos (outliers).")
        
        st.subheader("4. Mapeamento")
        st.markdown("""
        * **Marcador:** Polígonos (limites dos municípios).
        * **Canal de Posição:** Coordenadas de latitude/longitude.
        * **Canal de Cor:** A variável `nu_ocorrencias` foi mapeada para um gradiente de cor sequencial (Reds). Tons escuros = maior volume.
        """)

    with col_texto2:
        st.subheader("5. Representação Visual")
        st.info("A representação visual prática encontra-se na aba 'Dashboard Interativo', feita com Python utilizando as bibliotecas Streamlit, GeoPandas e Plotly.")
        
        st.subheader("6. Análise dos Dados")
        st.write("A análise evidencia que números absolutos tendem a destacar grandes metrópoles. Observa-se uma concentração esperada nas capitais, mas o mapa permite identificar municípios do interior com volumes anormais de internação.")
        
        st.subheader("7. Takeaways")
        st.markdown("""
        * Cidades mais populosas lideram o ranking absoluto.
        * O uso de cores quentes facilita a rápida identificação de zonas de alerta.
        * A visualização serve como triagem rápida para alocação de verbas do SUS.
        """)
        
        st.subheader("8. Análise de Viabilidade")
        st.success("Produto altamente viável. Transformou-se uma base de dados estática em uma aplicação web interativa, que pode ser hospedada gratuitamente na nuvem e consumida por gestores de saúde.")

# ==========================================
# ABA 2: DASHBOARD COM PLOTS
# ==========================================
with aba2:
    # Sidebar de Filtros
    st.sidebar.header("Filtros do Dashboard")
    min_casos = st.sidebar.slider("Ocultar cidades com menos de X casos:", 
                                  min_value=0, 
                                  max_value=int(gdf['nu_ocorrencias'].max()), 
                                  value=0, step=10)
    
    gdf_filtrado = gdf[gdf['nu_ocorrencias'] >= min_casos]

    # Indicadores (Métricas no topo)
    st.markdown("### Visão Geral")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total de Municípios no Filtro", value=len(gdf_filtrado))
    kpi2.metric(label="Total de Internações (Soma)", value=f"{gdf_filtrado['nu_ocorrencias'].sum():,}".replace(',','.'))
    cidade_max = gdf_filtrado.loc[gdf_filtrado['nu_ocorrencias'].idxmax()]['no_municipio'] if not gdf_filtrado.empty else "N/A"
    kpi3.metric(label="Cidade com Mais Casos", value=cidade_max)
    
    st.markdown("---")

    # Linha com o Mapa e o Gráfico de Barras lado a lado
    col_mapa, col_grafico = st.columns([3, 2]) # O mapa fica um pouco mais largo (proporção 3 para 2)

    with col_mapa:
        st.markdown("#### Mapa Espacial de Internações")
        if not gdf_filtrado.empty:
            fig_mapa = px.choropleth_mapbox(
                gdf_filtrado, geojson=gdf_filtrado.geometry, locations=gdf_filtrado.index,
                color='nu_ocorrencias', hover_name='no_municipio',
                color_continuous_scale="Reds", mapbox_style="carto-positron",
                zoom=3, center={"lat": -14.235, "lon": -51.925}, opacity=0.8,
                labels={'nu_ocorrencias': 'Internações'}
            )
            fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_mapa, use_container_width=True)
        else:
            st.warning("Nenhum dado encontrado para esse filtro.")

    with col_grafico:
        st.markdown("#### Top 10 Municípios (Em volume absoluto)")
        if not gdf_filtrado.empty:
            # Pega as 10 maiores cidades
            top10 = gdf_filtrado.nlargest(10, 'nu_ocorrencias')
            
            # Gráfico de barras horizontais do Plotly
            fig_barras = px.bar(
                top10, x='nu_ocorrencias', y='no_municipio', 
                orientation='h', color='nu_ocorrencias', 
                color_continuous_scale="Reds", text='nu_ocorrencias',
                labels={'nu_ocorrencias': 'Qtd. Internações', 'no_municipio': 'Município'}
            )
            fig_barras.update_layout(yaxis={'categoryorder':'total ascending'}, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_barras, use_container_width=True)