"""Plotly chart builders: radar profile + gauge score."""

import plotly.graph_objects as go
from config.settings import DIMENSIONS, COLOR_PRIMARY, COLOR_ACCENT_YELLOW, COLOR_ACCENT_ORANGE


def _hex_to_rgba(hex_color, alpha):
    """Plotly rejects 8-digit hex (#RRGGBBAA) -- it wants rgba(r,g,b,a)."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def create_radar_chart(scores, text_color):
    categories = [d for d in DIMENSIONS if d in scores]
    values = [scores[d] for d in categories]

    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    grid_color = _hex_to_rgba(text_color, 0.2)
    line_color = _hex_to_rgba(text_color, 0.35)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values_closed, theta=categories_closed, fill='toself', name='Your skill profile',
                                   line_color=COLOR_PRIMARY, fillcolor='rgba(171, 194, 112, 0.35)'))
    fig.add_trace(go.Scatterpolar(r=[70] * len(categories_closed), theta=categories_closed, fill=None, name='Target level',
                                   line=dict(color=COLOR_ACCENT_ORANGE, dash='dash')))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",  # the actual fix -- the disc itself, separate from paper/plot bgcolor
            radialaxis=dict(
                visible=True, range=[0, 100], tickvals=[20, 40, 60, 80, 100],
                tickfont=dict(color=text_color),
                gridcolor=grid_color,
                linecolor=line_color,
            ),
            angularaxis=dict(
                tickfont=dict(color=text_color),
                gridcolor=grid_color,
                linecolor=line_color,
            ),
        ),
        title="", showlegend=True, height=400,
        font=dict(color=text_color),
        legend=dict(font=dict(color=text_color)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_gauge_chart(score, text_color):
    color = COLOR_ACCENT_ORANGE if score < 40 else COLOR_ACCENT_YELLOW if score < 70 else COLOR_PRIMARY
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score, title={'text': "Overall competency level", 'font': {'color': text_color}},
        number={'font': {'color': text_color}},
        gauge={
            'bgcolor': "rgba(0,0,0,0)",  # same fix applied preemptively -- gauge has this too
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': text_color,
                      'tickfont': {'color': text_color}},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': 'rgba(253, 167, 105, 0.25)'},
                {'range': [40, 70], 'color': 'rgba(254, 200, 104, 0.25)'},
                {'range': [70, 100], 'color': 'rgba(171, 194, 112, 0.25)'},
            ],
            'threshold': {'line': {'color': text_color, 'width': 4}, 'thickness': 0.75, 'value': score},
        }
    ))
    fig.update_layout(height=350, font=dict(color=text_color),
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig