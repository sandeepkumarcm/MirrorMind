import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #0B0F19; color: #E7EAF3; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stStatusWidget"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent; }

    /* Kill Streamlit Cloud's "Deploy" toolbar chrome — looks unfinished in a demo */
    .stAppDeployButton,
    [data-testid="stToolbarActions"],
    [data-testid="stDeployButton"],
    button[kind="header"] { display: none !important; }

    .block-container { padding-top: 1.2rem !important; }

    .mm-card {
        background: #131826;
        border-radius: 16px;
        padding: 28px 32px;
        position: relative;
        border: 1px solid #232A3B;
        margin-bottom: 20px;
        overflow: hidden;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .mm-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #6C63FF, #22D3B6);
    }

    [data-baseweb="tab-panel"] {
        background: transparent !important;
        border: none !important;
        padding: 14px 0 0 0 !important;
    }

    .mm-hero { text-align: center; padding: 36px 32px 28px 32px; margin-bottom: 20px; }
    .mm-hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(90deg, #6C63FF, #22D3B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .mm-hero p.tagline { color: #8B93A7; font-size: 15px; margin-bottom: 24px; }

    /* ---- Live Pipeline Strip ---- */
    .mm-pipeline {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 32px;
    }
    .mm-pipeline-pill {
        background: #1A2033;
        border: 1px solid #232A3B;
        color: #C7CCDB;
        font-size: 13px;
        font-family: 'JetBrains Mono', monospace;
        padding: 8px 16px;
        border-radius: 999px;
        animation: mm-pulse 4.5s ease-in-out infinite;
    }
    .mm-pipeline-pill:nth-child(1) { animation-delay: 0s; }
    .mm-pipeline-pill:nth-child(3) { animation-delay: 0.6s; }
    .mm-pipeline-pill:nth-child(5) { animation-delay: 1.2s; }
    .mm-pipeline-pill:nth-child(7) { animation-delay: 1.8s; }
    .mm-pipeline-arrow { color: #6C63FF; font-size: 16px; opacity: 0.6; }

    @keyframes mm-pulse {
        0%, 70%, 100% { box-shadow: 0 0 0 0 rgba(108, 99, 255, 0); border-color: #232A3B; }
        15% { box-shadow: 0 0 14px 2px rgba(108, 99, 255, 0.55); border-color: #6C63FF; }
    }

    /* ---- Spec Sheet Stack ---- */
    .mm-spec-sheet {
        max-width: 620px;
        margin: 0 auto;
        text-align: left;
        border-top: 1px solid #232A3B;
        padding-top: 18px;
    }
    .mm-spec-row {
        display: flex;
        justify-content: space-between;
        padding: 7px 4px;
        border-bottom: 1px solid #1A2033;
        font-size: 13px;
    }
    .mm-spec-row:last-child { border-bottom: none; }
    .mm-spec-label {
        color: #6C63FF;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        letter-spacing: 0.04em;
        width: 110px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .mm-spec-value {
        color: #8B93A7;
        font-family: 'JetBrains Mono', monospace;
        text-align: right;
        flex-grow: 1;
    }
    .mm-live-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #22D3B6;
        display: inline-block;
        animation: mm-dot-pulse 1.6s ease-in-out infinite;
    }
    @keyframes mm-dot-pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(34, 211, 182, 0.5); }
        50% { opacity: 0.6; box-shadow: 0 0 0 5px rgba(34, 211, 182, 0); }
    }

    /* ---- Stat Strip (with designed empty state) ---- */
    .mm-stat-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 20px;
    }
    .mm-stat {
        background: #131826;
        border: 1px solid #232A3B;
        border-radius: 12px;
        padding: 16px 20px;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .mm-stat:hover { border-color: #3A3F55; transform: translateY(-2px); }
    .mm-stat-label {
        color: #8B93A7;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .mm-stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 700;
        color: #E7EAF3;
    }
    .mm-stat-value.mm-stat-empty {
        font-size: 14px;
        font-weight: 600;
        color: #4B5468;
        letter-spacing: 0.03em;
    }
    .mm-stat-icon { font-size: 13px; opacity: 0.8; }

    /* ---- Section header (used above content blocks like "Interview Question") ---- */
    .mm-section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }
    .mm-section-header .mm-section-icon {
        width: 30px; height: 30px;
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(108,99,255,0.18), rgba(34,211,182,0.18));
        border: 1px solid #2A3150;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px;
        flex-shrink: 0;
    }
    .mm-section-header h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 19px;
        font-weight: 700;
        color: #E7EAF3;
        margin: 0;
    }
    .mm-section-header p {
        color: #6B7285;
        font-size: 12.5px;
        margin: 2px 0 0 40px;
    }

    /* ---- Soft section wrapper (light grouping, not a heavy card) ---- */
    .mm-section-wrap {
        border: 1px solid #1D2333;
        background: linear-gradient(180deg, rgba(19,24,38,0.6), rgba(19,24,38,0.15));
        border-radius: 18px;
        padding: 24px 26px 20px 26px;
        margin-bottom: 22px;
    }

    /* ---- Recording / live status badge ---- */
    .mm-live-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.35);
        color: #FF8A8A;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.04em;
        padding: 5px 12px;
        border-radius: 999px;
        margin-bottom: 14px;
    }
    .mm-live-badge .mm-rec-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #FF6B6B;
        animation: mm-rec-pulse 1.1s ease-in-out infinite;
    }
    @keyframes mm-rec-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.35; }
    }

    button[data-baseweb="tab"] {
        background: #131826 !important;
        border-radius: 999px !important;
        border: 1px solid #232A3B !important;
        color: #8B93A7 !important;
        margin-right: 8px;
        padding: 8px 20px !important;
        font-family: 'Space Grotesk', sans-serif;
        transition: all 0.15s ease !important;
    }
    button[data-baseweb="tab"]:hover {
        border-color: #6C63FF !important;
        color: #C7CCDB !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #6C63FF, #22D3B6) !important;
        color: #0B0F19 !important;
        border: none !important;
        font-weight: 700;
    }
    [data-baseweb="tab-highlight"] { display: none; }
    [data-baseweb="tab-border"] { display: none; }

    div[data-testid="stMetric"] {
        background: #131826;
        border: 1px solid #232A3B;
        border-radius: 12px;
        padding: 14px 18px;
        transition: border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover { border-color: #3A3F55; }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; color: #22D3B6; }
    div[data-testid="stMetricLabel"] { color: #8B93A7; }

    .stButton > button {
        background: linear-gradient(90deg, #6C63FF, #22D3B6);
        color: #0B0F19;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-family: 'Space Grotesk', sans-serif;
        transition: transform 0.12s ease, box-shadow 0.12s ease, opacity 0.12s ease;
    }
    .stButton > button:hover {
        opacity: 0.95;
        color: #0B0F19;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px -6px rgba(108, 99, 255, 0.55);
    }
    .stButton > button:active { transform: translateY(0px); }

    div[data-testid="stAlert"] {
        background: #131826;
        border: 1px solid #232A3B;
        border-radius: 12px;
    }

    /* ---- Native bordered container (st.container(border=True)) ----
       Used to visually group Setup-tab content into one card WITHOUT
       the raw-HTML-div-spanning-multiple-calls bug. This is a real
       Streamlit container, so native widgets nest inside it correctly. */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #1D2333 !important;
        background: linear-gradient(180deg, rgba(19,24,38,0.55), rgba(19,24,38,0.15)) !important;
        border-radius: 18px !important;
    }

    /* ---- Tech stack expander (dark-themed to match) ---- */
    div[data-testid="stExpander"] {
        background: #131826;
        border: 1px solid #232A3B;
        border-radius: 14px;
        margin-bottom: 20px;
        overflow: hidden;
    }
    div[data-testid="stExpander"] summary {
        color: #C7CCDB !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 14px;
    }
    div[data-testid="stExpander"] summary:hover { color: #22D3B6 !important; }
    div[data-testid="stExpander"] svg { fill: #8B93A7 !important; }

    .mm-gauge-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    .mm-gauge {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .mm-gauge-inner {
        width: 160px;
        height: 160px;
        background: #131826;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .mm-gauge-score { font-family: 'JetBrains Mono', monospace; font-size: 36px; font-weight: 700; color: #E7EAF3; }
    .mm-gauge-caption { color: #8B93A7; font-size: 12px; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)


def glass_card_open():
    st.markdown('<div class="mm-card">', unsafe_allow_html=True)

def glass_card_close():
    st.markdown('</div>', unsafe_allow_html=True)


def section_wrap_open():
    """Soft, low-weight grouping wrapper — use around a Setup-tab-style block
    of content so it reads as one section without the old heavy glass-card look."""
    st.markdown('<div class="mm-section-wrap">', unsafe_allow_html=True)

def section_wrap_close():
    st.markdown('</div>', unsafe_allow_html=True)


def render_section_header(title, subtitle=None, icon="🎯"):
    """Renders a small icon-badge + title + optional subtitle, for giving
    plain st.subheader() text real visual weight (e.g. 'Interview Question')."""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="mm-section-header">
        <div class="mm-section-icon">{icon}</div>
        <h3>{title}</h3>
    </div>
    {subtitle_html}
    """, unsafe_allow_html=True)


def render_live_badge(text="RECORDING"):
    """Small pulsing red badge — use during active answer recording for
    a strong visual 'this is really live' moment in a demo."""
    st.markdown(f"""
    <div class="mm-live-badge">
        <span class="mm-rec-dot"></span>{text}
    </div>
    """, unsafe_allow_html=True)


def render_hero():
    """Pure pitch: title, tagline, pipeline. Tech stack now lives in
    render_tech_stack_expander() so first impression stays uncluttered."""
    hero_html = """
<div class="mm-card mm-hero">
<h1>🎯 MirrorMind</h1>
<p class="tagline">AI Interview Coach — Real-Time Video, Audio &amp; NLP Analysis</p>

<div class="mm-pipeline">
<span class="mm-pipeline-pill">🎥 Video</span>
<span class="mm-pipeline-arrow">→</span>
<span class="mm-pipeline-pill">🎙 Audio</span>
<span class="mm-pipeline-arrow">→</span>
<span class="mm-pipeline-pill">🧠 RAG + LLM</span>
<span class="mm-pipeline-arrow">→</span>
<span class="mm-pipeline-pill">📊 Scored Feedback</span>
</div>
</div>
"""
    st.markdown(hero_html, unsafe_allow_html=True)


def render_tech_stack_expander():
    """Collapsible 'proof' section shown right below the hero. Closed by
    default so the pitch lands first; one click reveals the full stack for
    anyone (recruiter, hiring manager) who wants the technical detail."""
    with st.expander("🛠️  Built end-to-end with — view tech stack", expanded=False):
        st.markdown("""
<div class="mm-spec-sheet" style="border-top:none;padding-top:0;">
<div class="mm-spec-row"><span class="mm-spec-label">BACKEND</span><span class="mm-spec-value">FastAPI · Uvicorn</span></div>
<div class="mm-spec-row"><span class="mm-spec-label">VISION</span><span class="mm-spec-value">OpenCV · MediaPipe · DeepFace</span></div>
<div class="mm-spec-row"><span class="mm-spec-label">SPEECH</span><span class="mm-spec-value">Whisper</span></div>
<div class="mm-spec-row"><span class="mm-spec-label"><span class="mm-live-dot"></span>RAG</span><span class="mm-spec-value">Sentence-BERT · FAISS</span></div>
<div class="mm-spec-row"><span class="mm-spec-label">LLM</span><span class="mm-spec-value">Groq · Llama 3.3</span></div>
<div class="mm-spec-row"><span class="mm-spec-label">UI</span><span class="mm-spec-value">Streamlit · Plotly</span></div>
<div class="mm-spec-row"><span class="mm-spec-label">INFRA</span><span class="mm-spec-value">Docker</span></div>
</div>
""", unsafe_allow_html=True)


def render_stat_strip(questions_answered, categories_covered, avg_score, session_time_str):
    """Designed empty state: instead of stark '0' / '0%' / '—', shows a
    muted 'Ready' label until the session actually produces data."""

    q_val = str(questions_answered) if questions_answered > 0 else '<span class="mm-stat-value mm-stat-empty">Ready to start</span>'
    q_val = f'<div class="mm-stat-value">{questions_answered}</div>' if questions_answered > 0 else '<div class="mm-stat-value mm-stat-empty">— Ready —</div>'

    c_val = f'<div class="mm-stat-value">{categories_covered}</div>' if categories_covered > 0 else '<div class="mm-stat-value mm-stat-empty">No data yet</div>'

    s_val = f'<div class="mm-stat-value">{avg_score}%</div>' if avg_score > 0 else '<div class="mm-stat-value mm-stat-empty">Awaiting answers</div>'

    t_val = f'<div class="mm-stat-value">{session_time_str}</div>' if session_time_str != "—" else '<div class="mm-stat-value mm-stat-empty">Not started</div>'

    st.markdown(f"""
    <div class="mm-stat-strip">
        <div class="mm-stat"><div class="mm-stat-label"><span class="mm-stat-icon">📝</span>Questions Answered</div>{q_val}</div>
        <div class="mm-stat"><div class="mm-stat-label"><span class="mm-stat-icon">🗂</span>Categories Covered</div>{c_val}</div>
        <div class="mm-stat"><div class="mm-stat-label"><span class="mm-stat-icon">📈</span>Avg Overall Score</div>{s_val}</div>
        <div class="mm-stat"><div class="mm-stat-label"><span class="mm-stat-icon">⏱</span>Session Time</div>{t_val}</div>
    </div>
    """, unsafe_allow_html=True)


def render_radial_gauge(score, label="Overall Score"):
    if score >= 75:
        color = "#22D3B6"
    elif score >= 50:
        color = "#F5A623"
    else:
        color = "#FF6B6B"
    angle = min(max(score, 0), 100) * 3.6
    st.markdown(f"""
    <div class="mm-gauge-wrap">
        <div class="mm-gauge" style="background: conic-gradient({color} {angle}deg, #232A3B {angle}deg);">
            <div class="mm-gauge-inner">
                <div class="mm-gauge-score">{score}%</div>
                <div class="mm-gauge-caption">{label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)