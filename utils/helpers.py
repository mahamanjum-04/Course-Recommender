"""Small utility functions: session state init, page navigation, styling."""

import streamlit as st
from config.settings import COLOR_PRIMARY, COLOR_ACCENT_YELLOW, COLOR_ACCENT_ORANGE


def init_session_state():
    for key, default in [
        ('page', 'home'), ('responses', []), ('questions', []), ('current_q', 0),
        ('test_complete', False), ('selected_field', None),
        ('api_key', ''), ('used_fallback', False), ('link_cache', {}), ('dark_mode', False),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default


def go_to_page(page):
    st.session_state.page = page
    st.rerun()


def color_score(val):
    if val < 40:
        return f'background-color: {COLOR_ACCENT_ORANGE}55'
    elif val < 70:
        return f'background-color: {COLOR_ACCENT_YELLOW}55'
    return f'background-color: {COLOR_PRIMARY}55'