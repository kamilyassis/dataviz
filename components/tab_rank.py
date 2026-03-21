import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def _rank_pos(series, value):
    """Retorna a posição (1-based) de um valor em uma série ordenada desc. None se não encontrado."""
    ranking = series.rank(ascending=False, method='min')
    try:
        pos = int(ranking[series == value].iloc[0])
        return pos
    except (IndexError, KeyError):
        return None


def _tabela_cruzada(top_df, gdf_completo, col_ranking_oposto, label_oposto, label_pos):
    """
    Dado o top 10 de uma métrica, mostra a posição desses municípios na métrica oposta.
    """
    rows = []
    total = len(gdf_completo)
    for _, row in top_df.iterrows():
        mun = row["no_municipio"]
        val_oposto = gdf_completo.loc[gdf_completo["no_municipio"] == mun, col_ranking_oposto]
        if val_oposto.empty:
            continue
        val = val_oposto.iloc[0]
        pos = _rank_pos(gdf_completo[col_ranking_oposto], val)
        rows.append({
            "Município": mun,
            label_oposto: f"{val:,d}".replace(",", "."),
            label_pos: f"#{pos} de {total:,d}".replace(",", ".") if pos else "—",
        })
    return pd.DataFrame(rows)


def render_aba_rank(gdf_filtrado, modo_analise):
    usar_taxa = modo_analise == "Taxa por 100 mil habitantes"

    ordem_var_int = "taxa_internacoes"        if usar_taxa else "nu_ocorrencias_internacoes"
    ordem_var_amb = "taxa_ambulatorio"         if usar_taxa else "nu_ocorrencias_ambulatorio"
    label_int     = "Taxa Internações/100k"   if usar_taxa else "Internações (Absoluto)"
    label_amb     = "Taxa Ambulatório/100k"   if usar_taxa else "Ambulatórios (Absoluto)"

    # Top 10 — Barras─
    st.markdown("### Top 10 Zonas de Alerta")

    col_g1, col_g2 = st.columns(2)

    top_int = gdf_filtrado.nlargest(10, ordem_var_int)
    top_amb = gdf_filtrado.nlargest(10, ordem_var_amb)

    with col_g1:
        st.markdown("#### 🏥 Maiores Vítimas (Internações)")
        fig_int = px.bar(
            top_int,
            x=ordem_var_int,
            y="no_municipio",
            orientation="h",
            color=ordem_var_int,
            color_continuous_scale="Reds",
            labels={ordem_var_int: label_int, "no_municipio": ""},
        )
        fig_int.update_traces(hovertemplate="<b>%{y}</b><br>" + label_int + ": %{x:,d}<extra></extra>")
        fig_int.update_xaxes(tickformat=",d")
        fig_int.update_layout(
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False,
            margin=dict(l=0, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_int, use_container_width=True)

    with col_g2:
        st.markdown("#### 🩺 Maior Demanda (Ambulatórios)")
        fig_amb = px.bar(
            top_amb,
            x=ordem_var_amb,
            y="no_municipio",
            orientation="h",
            color=ordem_var_amb,
            color_continuous_scale="Blues",
            labels={ordem_var_amb: label_amb, "no_municipio": ""},
        )
        fig_amb.update_traces(hovertemplate="<b>%{y}</b><br>" + label_amb + ": %{x:,d}<extra></extra>")
        fig_amb.update_xaxes(tickformat=",d")
        fig_amb.update_layout(
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False,
            margin=dict(l=0, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_amb, use_container_width=True)

    # Tabelas cruzadas
    st.markdown("---")
    st.markdown("### 🔀 Análise Cruzada")
    st.caption(
        "Os municípios do Top 10 de cada métrica são localizados no ranking da métrica oposta, "
        "revelando se líderes em atendimento ambulatorial também lideram em internações — e vice-versa."
    )

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown("##### Top 10 em Internações → posição em Ambulatórios")
        df_cruz_int = _tabela_cruzada(
            top_int, gdf_filtrado,
            col_ranking_oposto=ordem_var_amb,
            label_oposto=label_amb,
            label_pos="Ranking Ambulatório",
        )
        st.dataframe(df_cruz_int, use_container_width=True, hide_index=True)

    with col_t2:
        st.markdown("##### Top 10 em Ambulatórios → posição em Internações")
        df_cruz_amb = _tabela_cruzada(
            top_amb, gdf_filtrado,
            col_ranking_oposto=ordem_var_int,
            label_oposto=label_int,
            label_pos="Ranking Internações",
        )
        st.dataframe(df_cruz_amb, use_container_width=True, hide_index=True)

    # Top 10 Urgência / 100k
    st.markdown("---")
    st.markdown("### 🚨 Muita Demanda, Pouca Disponibilidade!")
    st.caption(
        "Proporção de internações sobre atendimentos ambulatoriais por 100k habitantes "
        "Municípios com alto índice concentram casos graves com baixa prevenção prévia."
    )

    gdf_urg = gdf_filtrado.copy()
    # Índice de urgência = taxa de internações / (taxa ambulatório + 1) para evitar divisão por zero
    gdf_urg["indice_urgencia"] = (
        gdf_urg["taxa_internacoes"] / (gdf_urg["taxa_ambulatorio"] + 1)
    ).round(4)

    top_urg = gdf_urg.nlargest(10, "indice_urgencia")[
        ["no_municipio", "taxa_internacoes", "taxa_ambulatorio", "indice_urgencia", "populacao"]
    ].copy()

    fig_urg = go.Figure()
    top_urg_sorted = top_urg.sort_values("indice_urgencia", ascending=True)

    fig_urg.add_trace(go.Bar(
        x=top_urg_sorted["indice_urgencia"],
        y=top_urg_sorted["no_municipio"],
        orientation="h",
        marker=dict(
            color=top_urg_sorted["indice_urgencia"],
            colorscale="Oranges",
            showscale=True,
            colorbar=dict(title="Índice"),
        ),
        customdata=top_urg_sorted[["taxa_internacoes", "taxa_ambulatorio", "populacao"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Índice de Urgência: %{x:,d}<br>"
            "%{customdata[0]:,d}<br>"
            "%{customdata[1]:,d}<br>"
            "População: %{customdata[2]:,d}<extra></extra>"
        ),
    ))

    fig_urg.update_layout(
        xaxis_title="Índice de Urgência (Internações / Ambulatório por 100k)",
        yaxis_title="",
        height=420,
        margin=dict(l=0, r=20, t=10, b=40),
        plot_bgcolor="rgba(245, 245, 245, 0.6)",
        xaxis=dict(showgrid=True, gridcolor="white"),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_urg, use_container_width=True)

    # Scatter Plot
    st.markdown("---")
    st.markdown("### 🎯 Matriz de Risco: Prevenção vs. Agravamento")
    st.info(
        "**💡 Insight Analítico:** Municípios no quadrante superior esquerdo (altas internações e baixos atendimentos "
        "ambulatoriais) indicam possíveis falhas na **saúde preventiva**. Os pacientes não estão recebendo "
        "acompanhamento primário e chegam ao sistema já em estado grave. Este é um alvo prioritário para políticas públicas."
    )

    # Limites baseados nos percentis para evitar distorção por outliers extremos
    x_max = gdf_filtrado[ordem_var_amb].quantile(0.98)
    y_max = gdf_filtrado[ordem_var_int].quantile(0.98)
    x_med = gdf_filtrado[ordem_var_amb].median()
    y_med = gdf_filtrado[ordem_var_int].median()

    fig_scatter = px.scatter(
        gdf_filtrado,
        x=ordem_var_amb,
        y=ordem_var_int,
        hover_name="no_municipio",
        hover_data={"populacao": ":,d"},
        size="populacao",
        size_max=30,
        color=ordem_var_int,
        color_continuous_scale="Purples",
        labels={
            ordem_var_amb: "Atendimentos Ambulatoriais (Prevenção)",
            ordem_var_int: "Internações Hospitalares (Urgência)",
        },
        height=520,
        opacity=0.75,
    )

    # Linhas de mediana como referência de quadrantes
    fig_scatter.add_vline(
        x=x_med, line_dash="dash", line_color="gray", line_width=1,
        annotation_text="Mediana Amb.", annotation_position="top right",
        annotation_font_size=10,
    )
    fig_scatter.add_hline(
        y=y_med, line_dash="dash", line_color="gray", line_width=1,
        annotation_text="Mediana Int.", annotation_position="top right",
        annotation_font_size=10,
    )

    fig_scatter.update_layout(
        plot_bgcolor="rgba(240, 240, 240, 0.5)",
        xaxis=dict(
            showgrid=True, gridcolor="white",
            range=[0, x_max * 1.05],
        ),
        yaxis=dict(
            showgrid=True, gridcolor="white",
            range=[0, y_max * 1.05],
        ),
        margin=dict(l=0, r=0, t=10, b=10),
    )

    st.plotly_chart(fig_scatter, use_container_width=True)
    st.caption(
        "⚠️ Eixos limitados ao percentil 98 para melhor legibilidade. "
        "Outliers extremos podem estar fora da área visível."
    )