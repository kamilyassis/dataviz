import os
import streamlit as st
import streamlit.components.v1 as components

from utils.data_loader import converter_para_csv
from utils.map_utils import aplicar_filtro, preparar_geojson, calcular_view

_MAPA_DIR = os.path.join(os.path.dirname(__file__), "mapa_deck")
_mapa_deck = components.declare_component("mapa_deck", path=_MAPA_DIR)

_METRICAS = ["Internações", "Ambulatórios", "Ambos"]
_MODOS    = ["Números Absolutos", "Taxa / 100k hab.", "Ambos"]

_COLUNAS = {
    ("Internações",  "Taxa / 100k hab."):    "taxa_internacoes",
    ("Internações",  "Números Absolutos"):   "nu_ocorrencias_internacoes",
    ("Internações",  "Ambos"):               "taxa_internacoes",
    ("Ambulatórios", "Taxa / 100k hab."):    "taxa_ambulatorio",
    ("Ambulatórios", "Números Absolutos"):   "nu_ocorrencias_ambulatorio",
    ("Ambulatórios", "Ambos"):               "taxa_ambulatorio",
    ("Ambos",        "Taxa / 100k hab."):    "valor",
    ("Ambos",        "Números Absolutos"):   "valor",
    ("Ambos",        "Ambos"):               "valor",
}


def _render_coluna_filtros(gdf_filtrado):
    col_titulo, col_fechar = st.columns([3, 1])
    col_titulo.markdown("#### 🔧 Filtros")
    if col_fechar.button("✕", use_container_width=True, key="btn_fechar_filtros"):
        st.session_state.mostrar_filtros = False
        st.rerun()

    st.radio(
        "Métrica",
        _METRICAS,
        index=_METRICAS.index(st.session_state.metrica),
        key="_filtro_metrica",
        on_change=lambda: setattr(st.session_state, "metrica", st.session_state._filtro_metrica),
    )
    st.markdown("---")
    st.radio(
        "Modo de Visualização",
        _MODOS,
        index=_MODOS.index(st.session_state.modo_analise),
        key="_filtro_modo",
        on_change=lambda: setattr(st.session_state, "modo_analise", st.session_state._filtro_modo),
    )
    st.markdown("---")
    st.download_button(
        label="📥 Baixar CSV",
        data=converter_para_csv(gdf_filtrado),
        file_name="relatorio_cardiovascular.csv",
        mime="text/csv",
        use_container_width=True,
    )


def _render_detalhes_locais(gdf_filtrado):
    st.markdown("#### 📍 Detalhes Locais")

    if st.session_state.municipio_selecionado == "Todos":
        st.info("👆 Clique em um município no mapa ou use a busca acima.")
        if not st.session_state.mostrar_filtros:
            st.markdown("---")
            if st.button("＋ Mais Detalhes", use_container_width=True, key="btn_mais_detalhes"):
                st.session_state.mostrar_filtros = True
                st.rerun()
        return

    dados_mun = gdf_filtrado[gdf_filtrado["no_municipio"] == st.session_state.municipio_selecionado]
    if dados_mun.empty:
        st.warning("Município não encontrado nos dados filtrados.")
        return

    d    = dados_mun.iloc[0]
    modo = st.session_state.modo_analise

    st.markdown(f"**🏙️ {st.session_state.municipio_selecionado}**")
    st.caption(f"👥 Pop.: {d['populacao']:,.0f}".replace(',', '.'))
    st.markdown("---")

    def _bloco(emoji, label, taxa, absoluto):
        st.markdown(f"**{emoji} {label}**")
        if modo == "Taxa / 100k hab.":
            st.metric("Taxa / 100k", f"{taxa:,.1f}".replace(',', '.'))
            st.caption(f"Absoluto: {absoluto:,.0f}".replace(',', '.'))
        elif modo == "Números Absolutos":
            st.metric("Valor Absoluto", f"{absoluto:,.0f}".replace(',', '.'))
            st.caption(f"Taxa / 100k: {taxa:,.1f}".replace(',', '.'))
        else:  # Ambos
            c1, c2 = st.columns(2)
            c1.metric("Taxa / 100k", f"{taxa:,.1f}".replace(',', '.'))
            c2.metric("Absoluto",    f"{absoluto:,.0f}".replace(',', '.'))

    metrica = st.session_state.metrica
    if metrica in ("Internações", "Ambos"):
        _bloco("🏥", "Internações", d["taxa_internacoes"], d["nu_ocorrencias_internacoes"])
    if metrica == "Ambos":
        st.markdown("---")
    if metrica in ("Ambulatórios", "Ambos"):
        _bloco("🩺", "Ambulatórios", d["taxa_ambulatorio"], d["nu_ocorrencias_ambulatorio"])

    if not st.session_state.mostrar_filtros:
        st.markdown("---")
        if st.button("＋ Mais Detalhes", use_container_width=True, key="btn_mais_detalhes"):
            st.session_state.mostrar_filtros = True
            st.rerun()


def render_aba_mapa(gdf):
    st.session_state.setdefault("mostrar_filtros", False)

    gdf_filtrado = aplicar_filtro(gdf, st.session_state.metrica, st.session_state.modo_analise)

    st.caption("🗓️ Período de coleta: janeiro a agosto de 2025")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Municípios",      len(gdf_filtrado))
    col_m2.metric("Internações",     f"{gdf_filtrado['nu_ocorrencias_internacoes'].sum():,.0f}".replace(',', '.'))
    col_m3.metric("Ambulatórios",    f"{gdf_filtrado['nu_ocorrencias_ambulatorio'].sum():,.0f}".replace(',', '.'))
    col_m4.metric("População", f"{gdf_filtrado['populacao'].sum():,.0f}".replace(',', '.'))
    st.markdown("---")

    municipio_options = ["Todos"] + sorted(gdf_filtrado["no_municipio"].dropna().unique().tolist())
    if st.session_state.municipio_selecionado not in municipio_options:
        st.session_state.municipio_selecionado = "Todos"

    municipio_sel = st.selectbox(
        "município", municipio_options,
        index=municipio_options.index(st.session_state.municipio_selecionado),
        label_visibility="collapsed",
        placeholder="🔍 Buscar município...",
    )
    if municipio_sel != st.session_state.municipio_selecionado:
        st.session_state.municipio_selecionado = municipio_sel
        st.rerun()

    if st.session_state.mostrar_filtros:
        col_mapa, col_info, col_filtros = st.columns([2.5, 1, 1])
    else:
        col_mapa, col_info = st.columns([2.5, 1])
        col_filtros = None

    with col_mapa:
        mun_destaque = None if st.session_state.municipio_selecionado == "Todos" else st.session_state.municipio_selecionado
        coluna = _COLUNAS[(st.session_state.metrica, st.session_state.modo_analise)]

        municipio_clicado = _mapa_deck(
            geojson=preparar_geojson(gdf_filtrado, coluna, mun_destaque),
            viewState=calcular_view(gdf_filtrado, mun_destaque),
            selectedMunicipio=mun_destaque,
            height=480,
            default=None,
            key="mapa_deck_widget",
        )
        if municipio_clicado and municipio_clicado != st.session_state.municipio_selecionado:
            st.session_state.municipio_selecionado = municipio_clicado
            st.rerun()

    with col_info:
        _render_detalhes_locais(gdf_filtrado)

    if col_filtros:
        with col_filtros:
            _render_coluna_filtros(gdf_filtrado)