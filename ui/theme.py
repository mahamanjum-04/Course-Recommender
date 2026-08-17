"""Global CSS theme: light/dark mode, color palette, typography hierarchy,
rounded buttons/inputs, hidden sidebar, theme toggle button."""

import streamlit as st
from config.settings import (
    COLOR_PRIMARY, COLOR_ACCENT_YELLOW, COLOR_ACCENT_ORANGE, COLOR_BUTTON_TEXT,
    LIGHT_MODE, DARK_MODE,
)


def inject_theme(dark_mode):
    palette = DARK_MODE if dark_mode else LIGHT_MODE
    bg, text = palette["background"], palette["text"]

    st.markdown(f"""
    <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {bg} !important;
        }}

        body, .stMarkdown, .stText, p, span, label, div {{ color: {text}; }}

        h1 {{ color: {text}; font-size: 2.1rem; font-weight: 700; margin: 0 0 0.5rem 0; }}
        h2 {{ color: {text}; font-size: 1.4rem; font-weight: 600; margin: 1.5rem 0 0.75rem 0; }}
        h3 {{ color: {text}; font-size: 1.1rem; font-weight: 600; margin: 1rem 0 0.5rem 0; }}
        p, .stMarkdown, li {{ font-size: 1rem; font-weight: 400; line-height: 1.6; }}

        [data-testid="stSidebar"] {{ display: none; }}
        [data-testid="collapsedControl"] {{ display: none; }}

        [data-testid="stExpander"], [data-testid="stDataFrame"],
        [data-baseweb="popover"], [data-baseweb="menu"],
        div[data-baseweb="select"] > div, input, textarea {{
            background-color: {bg} !important;
            color: {text} !important;
        }}

        /* Expander header: newer Streamlit versions render this as native
           <details>/<summary> tags instead of a data-testid div, so both
           forms are targeted here with descendant wildcards to survive
           version differences. */
        details, summary, details *, summary *,
        [data-testid="stExpander"] *,
        [data-testid="stExpanderHeader"], [data-testid="stExpanderHeader"] *,
        [data-testid="stExpanderDetails"], [data-testid="stExpanderDetails"] * {{
            background-color: {bg} !important;
            color: {text} !important;
        }}

        /* Plotly chart wrapper: paper_bgcolor/plot_bgcolor in charts.py
           only makes the plot's own SVG transparent -- the surrounding
           Streamlit container div still carries the light theme's white
           background behind it, so it must be forced transparent here too. */
        [data-testid="stPlotlyChart"], [data-testid="stPlotlyChart"] > div,
        .js-plotly-plot, .plot-container, .svg-container {{
            background-color: transparent !important;
        }}

        /* Course links: always green */
        a {{ color: {COLOR_PRIMARY} !important; }}

        /* Inline code AND fenced code blocks -- skills tags and anything
           in the MCQ question -- always orange. The "code *" and "pre *"
           wildcards are required because fenced code blocks go through
           syntax highlighting, which paints individual tokens with their
           own <span> colors -- those override a plain "code" rule since
           they're a more specific, deeper match. Forcing every descendant
           to orange overrides the highlighter's per-token palette. */
        code, code *, pre, pre *, pre code, pre code * {{
            color: {COLOR_ACCENT_ORANGE} !important;
            background-color: rgba(253, 167, 105, 0.12) !important;
        }}

        div.stButton > button,
        div.stButton > button * {{
            color: {COLOR_BUTTON_TEXT} !important;
        }}
        div.stButton > button {{
            background-color: {COLOR_PRIMARY};
            border: none;
            border-radius: 999px;
            padding: 0.6rem 2rem;
            font-weight: 600;
            min-width: 220px;
            white-space: nowrap;
        }}
        div.stButton > button:hover {{
            background-color: {COLOR_ACCENT_YELLOW};
            border: none;
        }}
        div.stButton > button:focus:not(:active) {{
            background-color: {COLOR_PRIMARY};
        }}

        /* Submit answer button: yellow, orange on hover. Same descendant fix. */
        [data-testid="stFormSubmitButton"] button,
        [data-testid="stFormSubmitButton"] button * {{
            color: {COLOR_BUTTON_TEXT} !important;
        }}
        [data-testid="stFormSubmitButton"] button {{
            background-color: {COLOR_ACCENT_YELLOW} !important;
            border: none !important;
            border-radius: 999px !important;
            padding: 0.6rem 2rem !important;
            font-weight: 600 !important;
            min-width: 220px !important;
            white-space: nowrap !important;
        }}
        [data-testid="stFormSubmitButton"] button:hover {{
            background-color: {COLOR_ACCENT_ORANGE} !important;
        }}

        /* Download button: same descendant fix. */
        div.stDownloadButton > button,
        div.stDownloadButton > button * {{
            color: {COLOR_BUTTON_TEXT} !important;
        }}
        div.stDownloadButton > button {{
            background-color: {COLOR_ACCENT_ORANGE};
            border: none;
            border-radius: 999px;
            padding: 0.6rem 2rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        div.stDownloadButton > button:hover {{
            background-color: {COLOR_ACCENT_YELLOW};
        }}

        div[data-baseweb="select"] {{ width: 100% !important; min-width: 100%; }}
        div[data-baseweb="select"] > div {{
            border-radius: 999px;
            border-color: {COLOR_PRIMARY} !important;
        }}
        div[data-baseweb="select"] * {{
            overflow: visible !important;
            text-overflow: unset !important;
            white-space: nowrap !important;
        }}

        /* Dropdown option list: this is a separate floating popover, not
           the select box itself. Previous attempt assumed <li> tags, but
           BaseWeb actually renders options as <div role="option">, so
           that selector never matched anything. Tag-agnostic wildcards
           here, keyed only on the stable data-baseweb/role attributes,
           so this works regardless of which element BaseWeb uses. */
        [data-baseweb="popover"],
        [data-baseweb="popover"] *,
        [data-baseweb="menu"],
        [data-baseweb="menu"] *,
        [role="listbox"],
        [role="listbox"] *,
        [role="option"] {{
            background-color: {bg} !important;
            color: {text} !important;
        }}
        [role="option"]:hover,
        [role="option"][aria-selected="true"] {{
            background-color: {text}22 !important;
        }}

        /* Code block copy-icon button: it's an SVG, which uses "fill" for
           its color, not "color" -- our earlier code/pre rules only set
           color, so the icon itself was untouched and stayed its default
           dark fill, invisible against a dark background. */
        [data-testid="stCodeCopyButton"], [data-testid="stCodeCopyButton"] svg,
        [data-testid="stCodeCopyButton"] path, [data-testid="stCodeCopyButton"] *,
        button[title="Copy to clipboard"], button[title="Copy to clipboard"] svg,
        button[title="Copy to clipboard"] path {{
            color: {text} !important;
            fill: {text} !important;
        }}

        /* Progress bar: green */
        div[data-testid="stProgress"] > div > div > div {{
            background-color: {COLOR_PRIMARY};
        }}

        .st-key-theme_toggle_btn button,
        .st-key-theme_toggle_btn button * {{
            color: {text} !important;
        }}
        .st-key-theme_toggle_btn button {{
            min-width: unset !important;
            width: 44px !important;
            height: 44px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            font-size: 1.3rem !important;
            background-color: transparent !important;
            border: 1px solid {text} !important;
        }}
        .st-key-theme_toggle_btn button:hover {{
            background-color: {text}22 !important;
        }}

        /* st.metric truncates its value with ellipsis by default and has
           no built-in option to disable it -- overriding the truncation
           CSS directly lets long values (like a field name) wrap onto a
           second line instead of cutting off. Smaller font-size keeps it
           proportionate to the other metric boxes next to it. */
        [data-testid="stMetricValue"] {{
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: unset !important;
            font-size: 1.7rem !important;
            line-height: 1.2 !important;
        }}

        .centered {{ text-align: center; }}
        .subtitle {{ text-align: center; color: {text}; opacity: 0.85; font-size: 1.05rem; margin: 0 0 1rem 0; }}

        /* Bring the expander header (a native widget) into the same
           hierarchy scale as h3, so "Dimension breakdown" reads at the
           same level as course card titles elsewhere on the page. */
        [data-testid="stExpander"] summary,
        [data-testid="stExpanderHeader"] {{
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }}

        .step-circle {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem auto;
            font-size: 1.6rem;
            font-weight: 700;
            color: {COLOR_BUTTON_TEXT};
        }}
        .step-title {{
            text-align: center;
            font-size: 1.1rem;
            font-weight: 600;
            color: {text};
            margin-bottom: 0.4rem;
        }}
        .step-desc {{
            text-align: center;
            font-size: 0.92rem;
            color: {text};
            opacity: 0.75;
            line-height: 1.5;
            margin-bottom: 2rem;
        }}

        [data-testid="stMetric"] {{
            text-align: center;
        }}
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
            display: flex;
            justify-content: center;
        }}

        div[role="radiogroup"] > label {{
            margin-bottom: 1rem;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_theme_toggle():
    col1, col2 = st.columns([10, 1])
    with col2:
        icon = "\u2600\ufe0f" if st.session_state.dark_mode else "\U0001F319"
        if st.button(icon, key="theme_toggle_btn"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()