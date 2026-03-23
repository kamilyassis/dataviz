import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ─────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Serif+Display:ital@0;1&display=swap');

    /* ── Tokens dark ──────────────────────────────────────────────────────── */
    :root {
        --bg:           #0E0E0F;
        --surface:      #1A1A1C;
        --surface-2:    #222225;
        --surface-3:    #2A2A2E;
        --border:       #2E2E33;
        --border-light: #3A3A40;
        --text:         #EEECEA;
        --text-muted:   #EEECEA;
        --text-dim:     #4A4845;
        --accent:       #4ADE80;       /* verde-esmeralda vibrante */
        --accent-dim:   #166534;       /* verde escuro p/ fundos */
        --accent-glow:  rgba(74,222,128,0.12);
        --red:          #F87171;
        --radius:       12px;
        --radius-sm:    8px;
        --radius-xs:    6px;
        --shadow:       0 2px 12px rgba(0,0,0,0.4);
        --shadow-md:    0 4px 28px rgba(0,0,0,0.55);
        --font:         'DM Sans', sans-serif;
        --font-display: 'DM Serif Display', serif;
        --transition:   0.18s ease;
    }

    /* ── Reset global ─────────────────────────────────────────────────────── */
    html, body,
    [class*="css"],
    .stApp,
    .stApp > header,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stMain"] {
        font-family: var(--font) !important;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    /* ── Scrollbar ────────────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 99px; }

    /* ── Toolbar / header Streamlit ───────────────────────────────────────── */
    [data-testid="stHeader"] { background: var(--bg) !important; }
    [data-testid="stToolbar"] { display: none !important; }

    /* ── App container ────────────────────────────────────────────────────── */
    .main .block-container {
        padding: 2rem 3rem 4rem !important;
        max-width: 1300px !important;
    }

    /* ── Título principal ─────────────────────────────────────────────────── */
    h1 {
        font-family: var(--font-display) !important;
        font-size: 2rem !important;
        font-weight: 400 !important;
        letter-spacing: -0.02em !important;
        color: var(--text) !important;
        line-height: 1.2 !important;
        margin-bottom: 0.2rem !important;
    }

    /* ── Subtítulos ───────────────────────────────────────────────────────── */
    h2, h3, h4 {
        font-family: var(--font) !important;
        color: var(--text) !important;
    }
    h2 { font-size: 1.15rem !important; font-weight: 600 !important; }
    h3 { font-size: 0.95rem !important; font-weight: 600 !important; }
    h4 {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: var(--text-muted) !important;
    }

    /* ── Parágrafos ───────────────────────────────────────────────────────── */
    p, li {
        font-size: 0.9rem !important;
        line-height: 1.65 !important;
        color: var(--text) !important;
    }

    /* ── hr ───────────────────────────────────────────────────────────────── */
    hr {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 0.9rem 0 !important;
    }

    /* ── Badge de título ──────────────────────────────────────────────────── */
    .title-badge {
        display: inline-block;
        background: var(--accent-dim);
        color: var(--accent);
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        padding: 0.22rem 0.7rem;
        border-radius: 99px;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(74,222,128,0.2);
    }

    /* ── Tabs ─────────────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        background: var(--surface) !important;
        border-radius: var(--radius) !important;
        padding: 4px !important;
        border: 1px solid var(--border) !important;
        width: fit-content !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: var(--font) !important;
        font-size: 0.83rem !important;
        font-weight: 500 !important;
        color: var(--text-muted) !important;
        background: transparent !important;
        border-radius: var(--radius-xs) !important;
        padding: 0.4rem 1.05rem !important;
        border: none !important;
        transition: color var(--transition) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--surface-3) !important;
        color: var(--text) !important;
        box-shadow: var(--shadow) !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* ── Métricas ─────────────────────────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 0.9rem 1.1rem !important;
        box-shadow: var(--shadow) !important;
        transition: border-color var(--transition), box-shadow var(--transition) !important;
    }
    [data-testid="stMetric"]:hover {
        border-color: var(--border-light) !important;
        box-shadow: 0 0 0 1px var(--border-light), var(--shadow-md) !important;
    }
    [data-testid="stMetricLabel"] > div {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        color: var(--text-muted) !important;
    }
    [data-testid="stMetricValue"] > div {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: var(--text) !important;
        letter-spacing: -0.02em !important;
    }
    [data-testid="stMetricDelta"] { display: none !important; }

    /* ── Selectbox ────────────────────────────────────────────────────────── */
    [data-baseweb="select"] > div {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        font-size: 0.875rem !important;
        transition: border-color var(--transition) !important;
        box-shadow: none !important;
    }
    [data-baseweb="select"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
    }
    [data-baseweb="select"] span { color: var(--text) !important; }
    [data-baseweb="popover"] [role="listbox"] {
        background: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow-md) !important;
    }
    [role="option"] {
        background: transparent !important;
        color: var(--text-muted) !important;
        font-size: 0.875rem !important;
    }
    [role="option"]:hover,
    [aria-selected="true"][role="option"] {
        background: var(--surface-3) !important;
        color: var(--text) !important;
    }

    /* ── Radio — pill style ───────────────────────────────────────────────── */
    [data-testid="stRadio"] > label {
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        color: var(--text-muted) !important;
        margin-bottom: 0.35rem !important;
    }
    [data-testid="stRadio"] > div {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.35rem !important;
    }
    [data-testid="stRadio"] > div > label {
        background: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 99px !important;
        padding: 0.28rem 0.8rem !important;
        cursor: pointer !important;
        transition: all var(--transition) !important;
        font-size: 0.82rem !important;
        font-weight: 400 !important;
        color: var(--text-muted) !important;
        text-transform: none !important;
        letter-spacing: normal !important;
    }
    [data-testid="stRadio"] > div > label:has(input:checked) {
        background: var(--accent-dim) !important;
        border-color: rgba(74,222,128,0.3) !important;
        color: var(--accent) !important;
        font-weight: 500 !important;
    }
    [data-testid="stRadio"] > div > label:hover:not(:has(input:checked)) {
        border-color: var(--border-light) !important;
        color: var(--text) !important;
    }
    [data-testid="stRadio"] input[type="radio"] { display: none !important; }
    [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        font-size: 0.82rem !important;
        font-weight: 400 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        color: inherit !important;
    }

    /* ── Botões ───────────────────────────────────────────────────────────── */
    .stButton > button {
        font-family: var(--font) !important;
        font-size: 0.83rem !important;
        font-weight: 500 !important;
        background: var(--surface-2) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.42rem 0.9rem !important;
        transition: all var(--transition) !important;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        background: var(--surface-3) !important;
        border-color: var(--border-light) !important;
        color: var(--text) !important;
        transform: translateY(-1px) !important;
    }
    /* botão ✕ fechar — discreto */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        border-color: transparent !important;
        color: var(--text-muted) !important;
        padding: 0.3rem 0.5rem !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: var(--surface-3) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
        transform: none !important;
    }

    /* ── Download button ──────────────────────────────────────────────────── */
    [data-testid="stDownloadButton"] > button {
        font-family: var(--font) !important;
        font-size: 0.83rem !important;
        font-weight: 500 !important;
        background: var(--accent-dim) !important;
        color: var(--accent) !important;
        border: 1px solid rgba(74,222,128,0.25) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.45rem 1rem !important;
        transition: all var(--transition) !important;
        width: 100% !important;
        box-shadow: none !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: rgba(74,222,128,0.18) !important;
        border-color: rgba(74,222,128,0.45) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 0 16px var(--accent-glow) !important;
    }

    /* ── Popover ──────────────────────────────────────────────────────────── */
    [data-testid="stPopover"] > div > button {
        font-family: var(--font) !important;
        font-size: 0.83rem !important;
        font-weight: 500 !important;
        background: var(--surface-2) !important;
        color: var(--text-muted) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.42rem 0.9rem !important;
        width: 100% !important;
        transition: all var(--transition) !important;
    }
    [data-testid="stPopover"] > div > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }
    [data-testid="stPopoverBody"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow-md) !important;
        padding: 1.1rem !important;
    }

    /* ── Info / Warning ───────────────────────────────────────────────────── */
    [data-testid="stAlert"] {
        background: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        font-size: 0.85rem !important;
        color: var(--text-muted) !important;
    }

    /* ── Caption ──────────────────────────────────────────────────────────── */
    [data-testid="stCaptionContainer"] p {
        font-size: 0.77rem !important;
        color: var(--text-muted) !important;
    }

    /* ── Sidebar (desativada mas override p/ segurança) ───────────────────── */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }

    /* ── Plotly — fundo transparente ──────────────────────────────────────── */
    .js-plotly-plot .plotly,
    .js-plotly-plot .plotly .svg-container {
        background: transparent !important;
    }

    /* ── Animação de entrada ──────────────────────────────────────────────── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0);   }
    }
    [data-testid="stMetric"] {
        animation: fadeUp 0.3s ease both;
    }
    [data-testid="stMetric"]:nth-child(1) { animation-delay: 0.04s; }
    [data-testid="stMetric"]:nth-child(2) { animation-delay: 0.08s; }
    [data-testid="stMetric"]:nth-child(3) { animation-delay: 0.12s; }
    [data-testid="stMetric"]:nth-child(4) { animation-delay: 0.16s; }

    /* ── Cols de detalhe — card sutil ─────────────────────────────────────── */
    [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"] {
        background: transparent !important;
    }

    /* ── Aumento global de fonte (+150%) ──────────────────────────────────── */
    p, li {
        font-size: 1.35rem !important;
        line-height: 1.7 !important;
    }
    [data-testid="stCaptionContainer"] p {
        font-size: 1.05rem !important;
    }
    [data-testid="stMetricLabel"] > div {
        font-size: 1.0rem !important;
    }
    [data-testid="stMetricValue"] > div {
        font-size: 2.0rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem !important;
    }
    [data-baseweb="select"] > div {
        font-size: 1.1rem !important;
    }
    [role="option"] {
        font-size: 1.1rem !important;
    }
    .stButton > button {
        font-size: 1.1rem !important;
    }
    [data-testid="stDownloadButton"] > button {
        font-size: 1.1rem !important;
    }

    /* ── Aba Doc — Hero ───────────────────────────────────────────────────── */
    .doc-hero {
        background: linear-gradient(135deg, #1a1a1c 0%, #1e1212 60%, #2a1010 100%);
        border: 1px solid #3a2020;
        border-radius: 16px;
        padding: 2.8rem 2.4rem 2.4rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .doc-hero-glow {
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(248,113,113,0.10) 0%, transparent 70%);
        pointer-events: none;
    }
    .doc-hero-badge {
        display: inline-block;
        background: rgba(248,113,113,0.12);
        color: #F87171;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.28rem 0.85rem;
        border-radius: 99px;
        border: 1px solid rgba(248,113,113,0.25);
        margin-bottom: 1.2rem;
    }
    .doc-hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        font-weight: 400;
        color: #EEECEA;
        line-height: 1.25;
        margin: 0 0 0.6rem 0;
        letter-spacing: -0.01em;
    }
    .doc-hero-lead {
        font-size: 1.1rem;
        color: #a09890;
        line-height: 1.6;
        margin: 0 0 2rem 0;
        max-width: 620px;
    }
    .doc-hero-lead strong.hl-white { color: #EEECEA; }
    .doc-hero-lead strong.hl-red   { color: #F87171; }
    .doc-kpis {
        display: flex;
        gap: 1.2rem;
        flex-wrap: wrap;
    }
    .doc-kpi {
        background: rgba(248,113,113,0.08);
        border: 1px solid rgba(248,113,113,0.2);
        border-radius: 12px;
        padding: 1rem 1.4rem;
        min-width: 150px;
    }
    .doc-kpi-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: #F87171;
        margin-bottom: 0.3rem;
    }
    .doc-kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #EEECEA;
        letter-spacing: -0.03em;
    }

    /* ── Aba Doc — Perguntas (expander accordion) ─────────────────────────── */
    .doc-section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #7A7875;
        margin-bottom: 0.2rem;
    }
    .doc-section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.45rem;
        font-weight: 400;
        color: #EEECEA;
        margin: 0 0 1.2rem 0;
    }
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
    .doc-answer {
        font-size: 0.97rem;
        color: #a09890;
        line-height: 1.75;
        margin: 0.6rem 0 0 0;
    }

    /* ── Aba Doc — Cards de seção ─────────────────────────────────────────── */
    .doc-card {
        background: #1A1A1C;
        border: 1px solid #2E2E33;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        font-size: 0.97rem;
        color: #a09890;
        line-height: 1.7;
    }
    .doc-card.accent-green {
        border-color: rgba(74,222,128,0.2);
    }
    .doc-card-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: #7A7875;
        margin-bottom: 0.6rem;
    }
    .doc-card-label.green { color: #4ADE80; }
    .doc-card ul {
        padding-left: 1.1rem;
        margin: 0;
    }
    .doc-card li {
        font-size: 0.97rem !important;
        color: #a09890 !important;
        line-height: 1.7 !important;
        margin-bottom: 0.55rem;
    }
    .hl-white { color: #EEECEA; }
    .hl-green { color: #4ADE80; }
    </style>
    """, unsafe_allow_html=True)