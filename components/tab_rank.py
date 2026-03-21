import streamlit as st
import plotly.express as px


def render_aba_rank(gdf_filtrado, modo_analise):
    st.markdown("### Top 10 Zonas de Alerta")

    ordem_var_int = "taxa_internacoes" if modo_analise == "Taxa por 100 mil hab. (Recomendado)" else "nu_ocorrencias_internacoes"
    ordem_var_amb = "taxa_ambulatorio" if modo_analise == "Taxa por 100 mil hab. (Recomendado)" else "nu_ocorrencias_ambulatorio"

    col_g1, col_g2 = st.columns(2)

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
        fig_int.update_layout(yaxis={'categoryorder': 'total ascending'})
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
        fig_amb.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_amb, use_container_width=True)

    st.markdown("---")

    st.markdown("### 🎯 Matriz de Risco: Prevenção vs. Agravamento")
    st.info(
        "**💡 Insight Analítico:** Municípios no quadrante superior esquerdo (altas internações e baixos atendimentos "
        "ambulatoriais) indicam possíveis falhas na **saúde preventiva**. Os pacientes não estão recebendo "
        "acompanhamento primário e chegam ao sistema já em estado grave. Este é um alvo prioritário para políticas públicas."
    )

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