import streamlit as st


def render_aba_doc(gdf=None):

    # ── Calcular métricas do dataset ─────────────────────────────────────────
    total_casos    = 0
    total_mun      = 0
    internacoes_dia = 0

    if gdf is not None:
        total_casos     = int(
            gdf["nu_ocorrencias_internacoes"].sum()
        )
        total_mun       = int(gdf["no_municipio"].nunique())
        # 8 meses de coleta = 243 dias (jan–ago 2025)
        internacoes_dia = round(gdf["nu_ocorrencias_internacoes"].sum() / 243)

    casos_fmt = f"{total_casos:,}".replace(",", ".")
    mpd_fmt   = f"{internacoes_dia:,.1f}".replace(",", ".")
    mun_fmt   = str(total_mun)

    # ── Hero ─────────────────────────────────────────────────────────────────
    # Monta o HTML usando concatenação para evitar conflito de aspas no f-string
    hero_html = (
        '<div style="background:linear-gradient(135deg,#1a1a1c 0%,#1e1212 60%,#2a1010 100%);'
        'border:1px solid #3a2020;border-radius:16px;padding:2.8rem 2.4rem 2.4rem;'
        'margin-bottom:2rem;position:relative;overflow:hidden;">'

        # glow decorativo
        '<div style="position:absolute;top:-60px;right:-60px;width:220px;height:220px;'
        'border-radius:50%;background:radial-gradient(circle,rgba(248,113,113,0.10) 0%,transparent 70%);'
        'pointer-events:none;"></div>'

        # badge
        '<div style="display:inline-block;background:rgba(248,113,113,0.12);color:#F87171;'
        'font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;'
        'padding:0.28rem 0.85rem;border-radius:99px;border:1px solid rgba(248,113,113,0.25);'
        'margin-bottom:1.2rem;">&#x1FAC0; Alerta de Sa\u00fade P\u00fablica</div>'

        # título
        '<h2 style="font-family:\'DM Serif Display\',serif;font-size:2rem;font-weight:400;'
        'color:#EEECEA;line-height:1.25;margin:0 0 0.6rem 0;letter-spacing:-0.01em;">'
        'A doen\u00e7a que mais mata no Brasil<br>ao longo dos anos</h2>'

        # parágrafo
        '<p style="font-size:1.1rem;color:#a09890;line-height:1.6;margin:0 0 2rem 0;max-width:620px;">'
        'Apenas nos primeiros 8 meses de 2025, em '
        '<strong style="color:#EEECEA">' + mun_fmt + ' munic\u00edpios</strong> do pa\u00eds, '
        'foram registrados <strong style="color:#F87171">' + casos_fmt + ' casos</strong> '
        'de doen\u00e7as cardiovasculares \u2014 '
        'provando uma realidade alarmante: quase '
        '<strong style="color:#F87171">' + mpd_fmt + ' interna\u00e7\u00f5es por dia</strong>.'
        '</p>'

        # KPIs
        '<div style="display:flex;gap:1.2rem;flex-wrap:wrap;">'

        '<div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.2);'
        'border-radius:12px;padding:1rem 1.4rem;min-width:150px;">'
        '<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;'
        'color:#F87171;margin-bottom:0.3rem;">Total de casos</div>'
        '<div style="font-size:1.8rem;font-weight:700;color:#EEECEA;letter-spacing:-0.03em;">' + casos_fmt + '</div>'
        '</div>'

        '<div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.2);'
        'border-radius:12px;padding:1rem 1.4rem;min-width:150px;">'
        '<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;'
        'color:#F87171;margin-bottom:0.3rem;">Interna\u00e7\u00f5es/dia</div>'
        '<div style="font-size:1.8rem;font-weight:700;color:#EEECEA;letter-spacing:-0.03em;">' + mpd_fmt + '</div>'
        '</div>'

        '<div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.2);'
        'border-radius:12px;padding:1rem 1.4rem;min-width:150px;">'
        '<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;'
        'color:#F87171;margin-bottom:0.3rem;">Munic\u00edpios</div>'
        '<div style="font-size:1.8rem;font-weight:700;color:#EEECEA;letter-spacing:-0.03em;">' + mun_fmt + '</div>'
        '</div>'

        '</div>'  # fecha KPIs
        '</div>'  # fecha hero
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # ── Perguntas norteadoras ─────────────────────────────────────────────────
    st.markdown(
        '<p style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;'
        'text-transform:uppercase;color:#7A7875;margin-bottom:0.2rem;">'
        'O que nosso estudo pretende responder?</p>'
        '<p style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;font-weight:400;'
        'color:#EEECEA;margin:0 0 1.2rem 0;">Tr\u00eas perguntas que guiam a an\u00e1lise</p>',
        unsafe_allow_html=True,
    )

    # CSS para estilizar o st.expander no tema do projeto
    st.markdown("""
    <style>
    /* Expander — accordion de perguntas */
    [data-testid="stExpander"] {
        background: #1A1A1C !important;
        border: 1px solid #2E2E33 !important;
        border-radius: 12px !important;
        margin-bottom: 0.7rem !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"]:has(details[open]) {
        border-color: rgba(248,113,113,0.35) !important;
        background: rgba(248,113,113,0.04) !important;
    }
    [data-testid="stExpander"] summary {
        padding: 1rem 1.4rem !important;
        cursor: pointer !important;
        font-size: 1.0rem !important;
        font-weight: 500 !important;
        color: #EEECEA !important;
        list-style: none !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: #F87171 !important;
    }
    [data-testid="stExpander"] summary svg {
        color: #7A7875 !important;
    }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        padding: 0 1.4rem 1.2rem !important;
        border-top: 1px solid rgba(248,113,113,0.15) !important;
    }
    </style>
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
        label = f"{item['num']} · {item['pergunta']}"
        with st.expander(label, expanded=False):
            st.markdown(
                '<p style="font-size:0.97rem;color:#a09890;line-height:1.75;margin:0.6rem 0 0 0;">'
                + item["resposta"]
                + "</p>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Demais seções ─────────────────────────────────────────────────────────
    st.markdown(
        '<p style="font-family:\'DM Serif Display\',serif;font-size:1.3rem;font-weight:400;'
        'color:#EEECEA;margin:1.4rem 0 1rem 0;">Sobre o projeto</p>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    card_css = (
        "border-radius:12px;padding:1.4rem 1.6rem;margin-bottom:1rem;"
        "font-size:0.97rem;color:#a09890;line-height:1.7;"
    )

    with col1:
        st.markdown(
            '<div style="background:#1A1A1C;border:1px solid #2E2E33;' + card_css + '">'
            '<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;'
            'color:#7A7875;margin-bottom:0.6rem;">01 · Escopo e Desafio</div>'
            'O projeto mapeia as interna\u00e7\u00f5es hospitalares e atendimentos ambulatoriais causados por '
            'doen\u00e7as cardiovasculares em 2025. O desafio principal \u00e9 identificar aglomerados '
            'geogr\u00e1ficos com incid\u00eancia anormal e fornecer dados claros e proporcionais para a '
            'gest\u00e3o de sa\u00fade p\u00fablica \u2014 superando o vi\u00e9s que favorece cidades '
            'grandes em an\u00e1lises brutas.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="background:#1A1A1C;border:1px solid rgba(74,222,128,0.2);' + card_css + '">'
            '<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;'
            'color:#4ADE80;margin-bottom:0.6rem;">02 · Rigor T\u00e9cnico \u2014 ETL</div>'
            '<strong style="color:#EEECEA;">Diferencial:</strong> a aplica\u00e7\u00e3o consome a '
            '<strong style="color:#4ADE80;">API do IBGE em tempo real</strong> para baixar os dados '
            'populacionais do Censo 2022. Isso permite calcular a taxa de incid\u00eancia por 100 mil '
            'habitantes \u2014 compara\u00e7\u00e3o cient\u00edfica e proporcional entre munic\u00edpios '
            'de portes radicalmente distintos. Sem esse ajuste, epidemias silenciosas em cidades '
            'pequenas permanecem invis\u00edveis.'
            '</div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div style="background:#1A1A1C;border:1px solid #2E2E33;' + card_css + '">'
            '<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;'
            'color:#7A7875;margin-bottom:0.6rem;">03 · Representa\u00e7\u00e3o Visual</div>'
            'O mapa 3D coropl\u00e9tico possui navega\u00e7\u00e3o interativa com zoom e voo animado '
            'entre munic\u00edpios, respondendo ativamente \u00e0 sele\u00e7\u00e3o de m\u00e9tricas '
            'personaliz\u00e1veis. Na aba de an\u00e1lise, rankings com Top\u00a010, tabelas cruzadas, '
            '\u00edndice de urg\u00eancia e uma matriz de risco bivariada permitem correlacionar '
            'preven\u00e7\u00e3o e urg\u00eancia em profundidade.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="background:#1A1A1C;border:1px solid #2E2E33;' + card_css + '">'
            '<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;'
            'color:#7A7875;margin-bottom:0.6rem;">04 · Principais Conclus\u00f5es</div>'
            '<ul style="padding-left:1.1rem;margin:0;">'
            '<li style="margin-bottom:0.55rem;"><strong style="color:#EEECEA;">Vi\u00e9s populacional:</strong> '
            'munic\u00edpios pequenos escondem epidemias silenciosas que s\u00f3 aparecem com a taxa por 100k\u00a0hab.</li>'
            '<li style="margin-bottom:0.55rem;"><strong style="color:#EEECEA;">Alerta preventivo:</strong> '
            'baixo ambulat\u00f3rio + alta interna\u00e7\u00e3o = paciente chegando ao SUS apenas em estado cr\u00edtico.</li>'
            '<li><strong style="color:#EEECEA;">Aloca\u00e7\u00e3o inteligente:</strong> '
            'gestores podem direcionar recursos para as \u201czonas vermelhas\u201d de maior risco proporcional.</li>'
            '</ul>'
            '</div>',
            unsafe_allow_html=True,
        )