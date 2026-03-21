import streamlit as st

from components.tab_doc import render_aba_doc
from components.tab_mapa import render_aba_mapa
from components.tab_rank import render_aba_rank
from utils.data_loader import carregar_dados
from utils.map_utils import aplicar_filtro
from styles import inject_css


def init_session_state():
    st.session_state.setdefault("municipio_selecionado", "Todos")
    st.session_state.setdefault("estado_anterior", "Todos")
    st.session_state.setdefault("metrica",      "Ambos")
    st.session_state.setdefault("modo_analise", "Ambos")


def load_data():
    try:
        return carregar_dados()
    except FileNotFoundError:
        st.error("🚨 O ficheiro 'dataset.csv' não foi encontrado!")
        st.stop()


def main():
    st.set_page_config(
        page_title="ECVD — Saúde Cardiovascular",
        page_icon="🫀",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_css()
    init_session_state()
    gdf = load_data()

    st.markdown('<span class="title-badge">Estudo de Caso · Brasil 2025</span>', unsafe_allow_html=True)
    st.title("Saúde Cardiovascular no Brasil")
    st.markdown(
        "<p style='color:var(--text-muted);font-size:0.92rem;margin-top:-0.4rem;margin-bottom:1.2rem'>"
        "Análise espacial e epidemiológica de internações e atendimentos ambulatoriais · "
        "Dados INDE · Janeiro – Agosto 2025"
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    aba_doc, aba_mapa, aba_rank = st.tabs(
        ["📝  Relatório", "🗺️  Mapa Interativo", "📊  Análise & Ranking"]
    )

    with aba_doc:
        render_aba_doc()

    with aba_mapa:
        render_aba_mapa(gdf)

    with aba_rank:
        modo_rank = (
            "Taxa por 100 mil hab. (Recomendado)"
            if st.session_state.modo_analise != "Números Absolutos"
            else "Números Absolutos"
        )
        gdf_filtrado = aplicar_filtro(gdf, st.session_state.metrica, st.session_state.modo_analise)
        render_aba_rank(gdf_filtrado, modo_rank)


if __name__ == "__main__":
    main()