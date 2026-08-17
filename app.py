"""Main entry point: wires config, data, and UI together, then routes to
the correct page based on session state."""

import warnings
import streamlit as st
from dotenv import load_dotenv

from data.loader import load_courses
from ui.theme import inject_theme, render_theme_toggle
from ui.pages import render_home_page, render_test_page, render_results_page, render_footer
from utils.helpers import init_session_state

warnings.filterwarnings('ignore')
load_dotenv()

st.set_page_config(page_title="Course Recommender System", layout="centered")

init_session_state()
inject_theme(st.session_state.dark_mode)
render_theme_toggle()

courses_df = load_courses()

if st.session_state.page == 'home':
    render_home_page(courses_df)
elif st.session_state.page == 'test':
    render_test_page()
elif st.session_state.page == 'results':
    render_results_page(courses_df)

render_footer(st.session_state.dark_mode)