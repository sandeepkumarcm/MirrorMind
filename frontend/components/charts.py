import plotly.graph_objects as go

EYE_CONTACT_WEIGHT = 0.35
WPM_WEIGHT = 0.35
FILLER_WEIGHT = 0.15
PAUSE_WEIGHT = 0.15
TECHNICAL_WEIGHT = 0.5
COMMUNICATION_WEIGHT = 0.5
IDEAL_WPM_MID = 130
FILLER_CAP = 10
PAUSE_CAP = 10

DARK_LAYOUT = dict(
    paper_bgcolor="#131826",
    plot_bgcolor="#131826",
    font=dict(color="#E7EAF3", family="Inter"),
    xaxis=dict(gridcolor="#232A3B", zerolinecolor="#232A3B"),
    yaxis=dict(gridcolor="#232A3B", zerolinecolor="#232A3B"),
    legend=dict(bgcolor="rgba(0,0,0,0)")
)


def compute_communication_score(eye_contact_pct, wpm, filler_count, pause_count):
    eye_component = min(eye_contact_pct / 100, 1.0)
    wpm_component = 1 - (abs(wpm - IDEAL_WPM_MID) / IDEAL_WPM_MID)
    wpm_component = max(0.0, min(wpm_component, 1.0))
    filler_component = 1 - min(filler_count / FILLER_CAP, 1.0)
    pause_component = 1 - min(pause_count / PAUSE_CAP, 1.0)
    communication_score = (
        EYE_CONTACT_WEIGHT * eye_component +
        WPM_WEIGHT * wpm_component +
        FILLER_WEIGHT * filler_component +
        PAUSE_WEIGHT * pause_component
    ) * 100
    return round(communication_score, 2)


def compute_overall_score(technical_score, communication_score):
    overall = (TECHNICAL_WEIGHT * technical_score) + (COMMUNICATION_WEIGHT * communication_score)
    return round(overall, 2)


def render_emotion_timeline(emotion_history):
    if not emotion_history:
        fig = go.Figure()
        fig.update_layout(title="No emotion data yet", **DARK_LAYOUT)
        return fig

    fig = go.Figure()
    emotions_present = sorted(set(e["emotion"] for e in emotion_history))
    palette = ["#6C63FF", "#22D3B6", "#F5A623", "#FF6B6B", "#4CD3C2", "#B565F3", "#FFD166"]

    for i, emotion in enumerate(emotions_present):
        points = [e for e in emotion_history if e["emotion"] == emotion]
        fig.add_trace(go.Scatter(
            x=[p["timestamp"] for p in points],
            y=[p["confidence"] for p in points],
            mode="lines+markers",
            name=emotion,
            line=dict(color=palette[i % len(palette)])
        ))

    fig.update_layout(
        title="Emotion Timeline",
        xaxis_title="Time (seconds into session)",
        yaxis_title="Confidence (%)",
        yaxis_range=[0, 100],
        legend_title="Emotion",
        **DARK_LAYOUT
    )
    return fig


def _single_metric_chart(title, value, ideal_low, ideal_high, y_max, unit=""):
    """
    One metric per chart, y-axis scaled to that metric's own realistic range
    — fixes the old bug where WPM (0-150) squashed Fillers/Pauses (0-10)
    into invisible slivers on a shared axis.
    """
    if value <= ideal_high:
        color = "#22D3B6"
    elif value <= ideal_high * 1.5:
        color = "#F5A623"
    else:
        color = "#FF6B6B"

    fig = go.Figure()
    fig.add_trace(go.Bar(x=[title], y=[value], marker_color=color, width=0.5,
                          text=[f"{value}{unit}"], textposition="outside"))

    fig.add_shape(type="line", x0=-0.4, x1=0.4, y0=ideal_low, y1=ideal_low,
                  line=dict(color="#8B93A7", dash="dash"))
    fig.add_shape(type="line", x0=-0.4, x1=0.4, y0=ideal_high, y1=ideal_high,
                  line=dict(color="#8B93A7", dash="dash"))

    fig.update_layout(
        title=title,
        yaxis_range=[0, y_max],
        showlegend=False,
        height=280,
        margin=dict(t=50, b=30, l=40, r=20),
        **DARK_LAYOUT
    )
    return fig


def render_wpm_chart(wpm):
    return _single_metric_chart("WPM (ideal: 110-150)", wpm, ideal_low=110, ideal_high=150, y_max=200)


def render_filler_chart(filler_count):
    return _single_metric_chart("Filler Words (ideal: 0-3)", filler_count, ideal_low=0, ideal_high=3, y_max=12)


def render_pause_chart(pause_count):
    return _single_metric_chart("Pauses (ideal: 0-3)", pause_count, ideal_low=0, ideal_high=3, y_max=12)