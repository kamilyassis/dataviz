import streamlit as st

from components.tab_doc import render_aba_doc
from components.tab_mapa import render_aba_mapa
from components.tab_rank import render_aba_rank
from utils.data_loader import carregar_dados
from utils.map_utils import aplicar_filtro


def init_session_state():
    st.session_state.setdefault("municipio_selecionado", "Todos")
    st.session_state.setdefault("estado_anterior", "Todos")
    st.session_state.setdefault("metrica",      "Ambos")  # padrão: Ambos
    st.session_state.setdefault("modo_analise", "Ambos")  # padrão: Ambos


def load_data():
    try:
        return carregar_dados()
    except FileNotFoundError:
        st.error("🚨 O ficheiro 'dataset.csv' não foi encontrado!")
        st.stop()


def main():
    st.set_page_config(
        page_title="ECVD - Saúde Cardiovascular",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    init_session_state()
    gdf = load_data()

    st.title("🫀 Estudo de Caso: Saúde Cardiovascular no Brasil (2025)")
    st.markdown("---")

    aba_doc, aba_mapa, aba_rank = st.tabs(
        ["📝 Relatório do Projeto", "🗺️ Mapa Interativo", "📊 Análise e Ranking"]
    )

    with aba_doc:
        render_aba_doc()

    with aba_mapa:
        render_aba_mapa(gdf)

    with aba_rank:
        # Traduz modo_analise do novo formato para o formato esperado por aplicar_filtro
        modo_interno = (
            "Taxa por 100 mil hab. (Recomendado)"
            if st.session_state.modo_analise in ("Taxa / 100k hab.", "Ambos")
            else "Números Absolutos"
        )
        gdf_filtrado, _ = aplicar_filtro(
            gdf,
            "Todos",
            st.session_state.metrica,
            modo_interno,
        )
        render_aba_rank(gdf_filtrado, modo_interno)


if __name__ == "__main__":
    main()