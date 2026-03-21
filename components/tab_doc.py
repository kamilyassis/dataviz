import streamlit as st

def render_aba_doc():
    st.header("Documentação do Projeto")

    col_texto1, col_texto2 = st.columns(2)

    with col_texto1:
        st.subheader("1. Escopo e Desafio")
        st.write(
            "O projeto mapeia as internações hospitalares e atendimentos ambulatoriais causados por doenças "
            "cardiovasculares em 2025. O desafio principal é identificar aglomerados geográficos com incidência "
            "anormal (outliers) e fornecer dados claros para a gestão de saúde pública."
        )

        st.subheader("2. Rigor Técnico e Tratamento de Dados (ETL)")
        st.success(
            "**Diferencial do Projeto:** Para evitar o enviesamento populacional (onde cidades maiores parecem sempre "
            "piores em números absolutos), a aplicação consome a **API do IBGE em tempo real** para baixar dados do "
            "Censo 2022. É calculada a taxa de incidência por 100 mil habitantes, permitindo uma comparação científica "
            "e proporcional entre os municípios."
        )

        st.subheader("3. Representação Visual")
        st.write(
            "O mapa coroplético possui navegação interativa e zoom, respondendo ativamente à seleção da métrica. "
            "O painel inclui também uma matriz de risco (scatter plot) para correlação bivariada entre prevenção e urgência."
        )

    with col_texto2:
        st.subheader("4. Principais Conclusões (Takeaways)")
        st.markdown("""
        * **O Perigo do Viés Populacional:** A análise comprovou que olhar apenas para números absolutos cria um
          "ponto cego" na gestão. Ao calcularmos a taxa por 100 mil habitantes, descobrimos que epidemias silenciosas
          estão muitas vezes escondidas em municípios de pequeno porte.
        * **O Alerta da Atenção Básica (Prevenção vs. Urgência):** A Matriz de Risco revelou um padrão alarmante:
          cidades com baixo volume de atendimentos ambulatoriais (prevenção) frequentemente lideram as taxas de
          internações (urgência). Isso indica que o paciente só tem contato com o SUS quando a doença já está em
          estágio crítico.
        * **Inteligência na Alocação de Recursos:** Em vez de distribuir verbas de forma linear, gestores podem usar
          este painel para direcionar recursos financeiros, campanhas de conscientização e mutirões de exames para
          as "zonas vermelhas" de maior risco proporcional.
        """)