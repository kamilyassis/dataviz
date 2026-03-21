import os
import streamlit as st
import streamlit.components.v1 as components

from utils.data_loader import converter_para_csv
from utils.map_utils import aplicar_filtro, preparar_geojson, calcular_view

_MAPA_DIR = os.path.join(os.path.dirname(__file__), "mapa_deck")
_mapa_deck = components.declare_component("mapa_deck", path=_MAPA_DIR)

# Métrica → coluna de cor/elevação do mapa
_COLUNAS = {
    ("Internações",  "taxa"):     "taxa_internacoes",
    ("Internações",  "absoluto"): "nu_ocorrencias_internacoes",
    ("Ambulatórios", "taxa"):     "taxa_ambulatorio",
    ("Ambulatórios", "absoluto"): "nu_ocorrencias_ambulatorio",
    ("Ambos",        "taxa"):     "valor",
    ("Ambos",        "absoluto"): "valor",
}

_METRICAS   = ["Internações", "Ambulatórios", "Ambos"]
_MODOS      = ["Taxa / 100k hab.", "Ambos", "Números Absolutos"]


def _coluna_mapa(metrica, modo):
    chave = "taxa" if modo == "Taxa / 100k hab." else ("absoluto" if modo == "Números Absolutos" else "taxa")
    return _COLUNAS[(metrica, chave)]


# ── Coluna de filtros ─────────────────────────────────────────────────────────
def _render_coluna_filtros(gdf_filtrado):
    col_titulo, col_fechar = st.columns([3, 1])
    col_titulo.markdown("#### 🔧 Filtros")
    if col_fechar.button("✕", use_container_width=True, key="btn_fechar_filtros"):
        st.session_state.mostrar_filtros = False
        st.rerun()

    def _on_metrica_change():
        st.session_state.metrica = st.session_state._filtro_metrica

    def _on_modo_change():
        st.session_state.modo_analise = st.session_state._filtro_modo

    st.radio(
        "Métrica",
        _METRICAS,
        index=_METRICAS.index(st.session_state.metrica),
        key="_filtro_metrica",
        on_change=_on_metrica_change,
    )
    st.markdown("---")
    st.radio(
        "Modo de Visualização",
        _MODOS,
        index=_MODOS.index(st.session_state.modo_analise),
        help="'Ambos' exibe taxa e valor absoluto lado a lado nos detalhes.",
        key="_filtro_modo",
        on_change=_on_modo_change,
    )
    st.markdown("---")
    st.download_button(
        label="📥 Baixar CSV",
        data=converter_para_csv(gdf_filtrado),
        file_name="relatorio_cardiovascular.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ── Coluna de detalhes locais ─────────────────────────────────────────────────
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
    modo = st.session_state.modo_analise  # "Taxa / 100k hab." | "Ambos" | "Números Absolutos"

    st.markdown(f"**🏙️ {st.session_state.municipio_selecionado}**")
    st.caption(f"👥 Pop.: {d['populacao']:,.0f}".replace(',', '.'))
    st.markdown("---")

    def _bloco(label_emoji, label, taxa, absoluto):
        st.markdown(f"**{label_emoji} {label}**")
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


# ── Função principal ──────────────────────────────────────────────────────────
def render_aba_mapa(gdf):
    st.session_state.setdefault("mostrar_filtros", False)

    # gdf_filtrado calculado com estado atual do session_state
    gdf_filtrado, _ = aplicar_filtro(
        gdf,
        "Todos",                          # filtro por estado removido
        st.session_state.metrica,
        # aplicar_filtro ainda espera o formato antigo internamente
        "Taxa por 100 mil hab. (Recomendado)"
        if st.session_state.modo_analise in ("Taxa / 100k hab.", "Ambos")
        else "Números Absolutos",
    )

    # ── Cabeçalho compacto ──
    st.caption("🗓️ Período de coleta: janeiro a agosto de 2025")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Municípios",      len(gdf_filtrado))
    col_m2.metric("Internações",     f"{gdf_filtrado['nu_ocorrencias_internacoes'].sum():,.0f}".replace(',', '.'))
    col_m3.metric("Ambulatórios",    f"{gdf_filtrado['nu_ocorrencias_ambulatorio'].sum():,.0f}".replace(',', '.'))
    col_m4.metric("População Total", f"{gdf_filtrado['populacao'].sum():,.0f}".replace(',', '.'))
    st.markdown("---")

    # ── Busca de município (compacta) ──
    municipio_options = ["Todos"] + sorted(gdf_filtrado["no_municipio"].dropna().unique().tolist())
    if st.session_state.municipio_selecionado not in municipio_options:
        st.session_state.municipio_selecionado = "Todos"

    municipio_sel = st.selectbox(
        "🔍 Buscar município",
        municipio_options,
        index=municipio_options.index(st.session_state.municipio_selecionado),
        label_visibility="collapsed",
        placeholder="🔍 Buscar município...",
    )
    if municipio_sel != st.session_state.municipio_selecionado:
        st.session_state.municipio_selecionado = municipio_sel
        st.rerun()

    # ── Layout dinâmico ──
    if st.session_state.mostrar_filtros:
        col_mapa, col_info, col_filtros = st.columns([2.5, 1, 1])
    else:
        col_mapa, col_info = st.columns([2.5, 1])
        col_filtros = None

    with col_mapa:
        mun_destaque = (
            None if st.session_state.municipio_selecionado == "Todos"
            else st.session_state.municipio_selecionado
        )
        coluna = _coluna_mapa(st.session_state.metrica, st.session_state.modo_analise)

        municipio_clicado = _mapa_deck(
            geojson=preparar_geojson(gdf_filtrado, coluna, mun_destaque),
            viewState=calcular_view(gdf_filtrado, mun_destaque),
            selectedMunicipio=mun_destaque,
            height=480,   # reduzido para caber bem em 750px de altura
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