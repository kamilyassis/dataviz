import streamlit as st

def render_aba_doc(gdf=None):
    total_casos     = 0
    total_mun       = 0
    internacoes_dia = 0

    if gdf is not None:
        total_casos     = int(
            gdf["nu_ocorrencias_internacoes"].sum()
        )
        total_mun       = int(gdf["no_municipio"].nunique())
        internacoes_dia = round(gdf["nu_ocorrencias_internacoes"].sum() / 243)

    casos_fmt = f"{total_casos:,}".replace(",", ".")
    mpd_fmt   = f"{internacoes_dia:,.0f}".replace(",", ".")
    mun_fmt   = str(total_mun)

    # Hero
    st.markdown(f"""
        <div class="doc-hero">
            <div class="doc-hero-glow"></div>
            <div class="doc-hero-badge">&#x1FAC0; Alerta de Sa&uacute;de P&uacute;blica</div>
            <h2 class="doc-hero-title">A doen&ccedil;a que mais mata no Brasil<br>ao longo dos anos</h2>
            <p class="doc-hero-lead">
                Apenas nos primeiros 8 meses de 2025, em
                <strong class="hl-white">{mun_fmt} munic&iacute;pios</strong> do pa&iacute;s,
                foram registrados <strong class="hl-red">{casos_fmt} casos</strong>
                de doen&ccedil;as cardiovasculares &mdash;
                provando uma realidade alarmante: quase
                <strong class="hl-red">{mpd_fmt} interna&ccedil;&otilde;es por dia</strong>.
            </p>
            <div class="doc-kpis">
                <div class="doc-kpi">
                    <div class="doc-kpi-label">Total de casos</div>
                    <div class="doc-kpi-value">{casos_fmt}</div>
                </div>
                <div class="doc-kpi">
                    <div class="doc-kpi-label">Interna&ccedil;&otilde;es/dia</div>
                    <div class="doc-kpi-value">{mpd_fmt}</div>
                </div>
                <div class="doc-kpi">
                    <div class="doc-kpi-label">Munic&iacute;pios</div>
                    <div class="doc-kpi-value">{mun_fmt}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Perguntas norteadoras
    st.markdown("""
        <p class="doc-section-label">O que nosso estudo pretende responder?</p>
        <p class="doc-section-title">Tr&ecirc;s perguntas que guiam a an&aacute;lise</p>
    """, unsafe_allow_html=True)

    perguntas = [
        {
            "num": "01",
            "pergunta": "Quais municípios concentram as maiores taxas de internação cardiovascular por 100 mil habitantes?",
            "resposta": (
                "Ao normalizarmos os dados pelo tamanho da população, descobrimos que as maiores taxas de internação "
                "não estão necessariamente nas grandes capitais — mas sim em municípios de pequeno e médio porte, "
                "frequentemente em regiões com menor acesso à rede de saúde preventiva. "
                "O mapa interativo permite explorar essa distribuição geograficamente, revelando 'zonas vermelhas' "
                "que seriam invisíveis em uma análise por números absolutos."
            ),
        },
        {
            "num": "02",
            "pergunta": "Existe correlação entre baixo atendimento ambulatorial e alta taxa de internações?",
            "resposta": (
                "Sim — e esse é um dos achados mais relevantes do estudo. A Matriz de Risco (scatter plot bivariado) "
                "na aba de Análise revela que municípios com baixo volume de atendimentos ambulatoriais (prevenção) "
                "frequentemente lideram as taxas de internações (urgência). "
                "Isso aponta para uma falha sistêmica na atenção básica: o paciente cardiovascular só acessa o SUS "
                "quando a doença já está em estágio crítico, o que eleva custos e mortalidade."
            ),
        },
        {
            "num": "03",
            "pergunta": "Onde estão as zonas de maior urgência cardiovascular relativa no Brasil?",
            "resposta": (
                "O Índice de Urgência — calculado como a razão entre internações e atendimentos ambulatoriais "
                "por 100 mil habitantes — identifica os municípios onde o sistema opera predominantemente em "
                "modo reativo. Esses municípios constituem alvos prioritários para políticas de expansão da "
                "atenção básica, campanhas de prevenção e mutirões de exames cardiológicos. "
                "O ranking completo está disponível na aba Análise & Ranking."
            ),
        },
    ]

    for item in perguntas:
        with st.expander(f"{item['num']} · {item['pergunta']}", expanded=False):
            st.markdown(
                f'<p class="doc-answer">{item["resposta"]}</p>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Seções informativas
    st.markdown(
        '<p class="doc-section-title" style="margin-top:1.4rem;">Sobre o projeto</p>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="doc-card">
                <div class="doc-card-label">01 &middot; Escopo e Desafio</div>
                O projeto mapeia as interna&ccedil;&otilde;es hospitalares e atendimentos ambulatoriais
                causados por doen&ccedil;as cardiovasculares em 2025. O desafio principal &eacute;
                identificar aglomerados geogr&aacute;ficos com incid&ecirc;ncia anormal e fornecer dados
                claros e proporcionais para a gest&atilde;o de sa&uacute;de p&uacute;blica &mdash;
                superando o vi&eacute;s que favorece cidades grandes em an&aacute;lises brutas.
            </div>
            <div class="doc-card accent-green">
                <div class="doc-card-label green">02 &middot; Rigor T&eacute;cnico &mdash; ETL</div>
                <strong class="hl-white">Diferencial:</strong> a aplica&ccedil;&atilde;o consome a
                <strong class="hl-green">API do IBGE em tempo real</strong> para baixar os dados
                populacionais do Censo 2022. Isso permite calcular a taxa de incid&ecirc;ncia por
                100&nbsp;mil habitantes &mdash; compara&ccedil;&atilde;o cient&iacute;fica e proporcional
                entre munic&iacute;pios de portes radicalmente distintos. Sem esse ajuste, epidemias
                silenciosas em cidades pequenas permanecem invis&iacute;veis.
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="doc-card">
                <div class="doc-card-label">03 &middot; Representa&ccedil;&atilde;o Visual</div>
                O mapa 3D coropl&eacute;tico possui navega&ccedil;&atilde;o interativa com zoom e voo
                animado entre munic&iacute;pios, respondendo ativamente &agrave; sele&ccedil;&atilde;o
                de m&eacute;tricas personaliz&aacute;veis. Na aba de an&aacute;lise, rankings com
                Top&nbsp;10, tabelas cruzadas, &iacute;ndice de urg&ecirc;ncia e uma matriz de risco
                bivariada permitem correlacionar preven&ccedil;&atilde;o e urg&ecirc;ncia em profundidade.
            </div>
            <div class="doc-card">
                <div class="doc-card-label">04 &middot; Principais Conclus&otilde;es</div>
                <ul>
                    <li><strong class="hl-white">Vi&eacute;s populacional:</strong>
                        munic&iacute;pios pequenos escondem epidemias silenciosas que s&oacute;
                        aparecem com a taxa por 100k&nbsp;hab.</li>
                    <li><strong class="hl-white">Alerta preventivo:</strong>
                        baixo ambulat&oacute;rio + alta interna&ccedil;&atilde;o = paciente chegando
                        ao SUS apenas em estado cr&iacute;tico.</li>
                    <li><strong class="hl-white">Aloca&ccedil;&atilde;o inteligente:</strong>
                        gestores podem direcionar recursos para as &ldquo;zonas vermelhas&rdquo;
                        de maior risco proporcional.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)