"""One render function per page. Each reads/writes st.session_state directly."""

import os
import pandas as pd
import streamlit as st

from config.settings import FIELDS, N_PER_DIMENSION, TOP_N_RECOMMENDATIONS, COLOR_PRIMARY, COLOR_ACCENT_YELLOW, COLOR_ACCENT_ORANGE
from llm.client import get_mistral_client
from llm.questions import generate_full_test
from llm.links import find_course_link
from engine.scoring import calculate_dimension_scores, calculate_overall_score, get_competency_level
from engine.recommendations import get_course_recommendations
from ui.charts import create_radar_chart, create_gauge_chart
from ui.components import render_course_card, render_dimension_table
from utils.helpers import go_to_page


def _start_new_test(field):
    client = get_mistral_client()
    with st.spinner("Generating your personalized skill test..."):
        questions, used_fallback = generate_full_test(client, field, n_per_dimension=N_PER_DIMENSION)
    st.session_state.questions = questions
    st.session_state.used_fallback = used_fallback
    st.session_state.selected_field = field
    st.session_state.responses = []
    st.session_state.current_q = 0
    st.session_state.test_complete = False
    if 'dim_scores' in st.session_state:
        del st.session_state.dim_scores


def _resolve_link(client, course):
    if pd.notna(course.get('Link')) and str(course.get('Link')).strip():
        return course['Link'], False

    name = course.get('Name', '')
    cache = st.session_state.link_cache
    if name in cache:
        return cache[name], (cache[name] is not None)

    link = find_course_link(client, name, course.get('Provider'))
    cache[name] = link
    return link, (link is not None)


def render_home_page(courses_df):
    st.markdown("<h1 class='centered'>Personalized course recommender</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Pick a field, take a short skill test, and get matched to "
        "real courses based on where you actually stand right now.</p>",
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")
    st.write("")

    steps = [
        {
            "color": COLOR_PRIMARY,
            "title": "1. Select a field",
            "desc": "Pick any field you want to improve in.",
        },
        {
            "color": COLOR_ACCENT_YELLOW,
            "title": "2. Take a test",
            "desc": "This test will identify your skill level as well as gaps in your skills.",
        },
        {
            "color": COLOR_ACCENT_ORANGE,
            "title": "3. Get recommended courses",
            "desc": "These recommendations will help you bridge the gap in your skills so you can advance in your field of interest.",
        },
    ]

    s1, s2, s3 = st.columns([1, 2, 1])
    with s2:
        for step in steps:
            st.markdown(
                f"<div class='step-circle' style='background-color:{step['color']};'>"
                f"{step['title'][0]}</div>"
                f"<div class='step-title'>{step['title']}</div>"
                f"<div class='step-desc'>{step['desc']}</div>",
                unsafe_allow_html=True,
            )
            st.write("")
            st.write("")

    st.write("")
    st.write("")
    st.write("")

    if courses_df is None:
        st.error("No course data loaded. Add coursera_courses.csv to the data folder.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Courses in pool", f"{len(courses_df)}")
    with col2:
        st.metric("Fields available", f"{len(FIELDS)}")

    st.write("")
    st.write("")
    st.write("")

    field = st.selectbox("Field of interest", list(FIELDS.keys()), label_visibility="collapsed")

    st.write("")

    if not st.session_state.api_key and not os.environ.get('MISTRAL_API_KEY'):
        with st.expander("API key needed for fresh questions"):
            key_input = st.text_input("Mistral API key", type="password", value=st.session_state.api_key,
                                       help="Get one free at console.mistral.ai. Without it, a small backup question set is used instead.")
            st.session_state.api_key = key_input

    st.write("")
    b1, b2, b3 = st.columns([1, 2, 1])
    with b2:
        if st.button("Start Assessment!", type="primary", use_container_width=True):
            _start_new_test(field)
            go_to_page('test')

    st.write("")
    st.write("")


def render_test_page():
    st.markdown(
        f"<h1 class='centered'>Skill assessment</h1>"
        f"<p class='subtitle'>{st.session_state.selected_field}</p>",
        unsafe_allow_html=True,
    )
    if st.session_state.used_fallback:
        st.warning("Couldn't reach the question generator for at least one dimension — a backup question was used there instead.")
    st.markdown("---")

    questions = st.session_state.questions
    current_idx = st.session_state.current_q

    if not questions:
        st.error("No questions available.")
        if st.button("Go back"):
            go_to_page('home')
        return

    if current_idx >= len(questions):
        st.session_state.test_complete = True
        go_to_page('results')
        return

    q = questions[current_idx]
    st.progress(current_idx / len(questions))
    st.write(f"**Question {current_idx + 1} of {len(questions)}**  ·  **Dimension:** {q['dimension']}")

    st.markdown("---")
    with st.container(key="mcq_question_container"):
        st.markdown(f"## {q['question']}")

    with st.form(key=f"question_{current_idx}"):
        selected_value = st.radio(
            "Select your answer:",
            options=q['options'],
            key=f"answer_{current_idx}",
            index=None,
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Submit answer", type="primary")

    selected_option = q['options'].index(selected_value) if selected_value is not None else None

    if submitted and selected_option is not None:
        st.session_state.responses.append(selected_option)
        st.session_state.current_q += 1
        if st.session_state.current_q >= len(questions):
            st.session_state.test_complete = True
            go_to_page('results')
        else:
            st.rerun()
    elif submitted and selected_option is None:
        st.warning("Please select an answer before submitting.")


def render_results_page(courses_df):
    st.markdown("<h1 class='centered'>Your results</h1>", unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.responses:
        st.warning("No responses found. Please retake the assessment.")
        if st.button("Start assessment"):
            go_to_page('home')
        return

    dim_scores = calculate_dimension_scores(st.session_state.responses,
                                              st.session_state.questions[:len(st.session_state.responses)])
    overall_score = calculate_overall_score(dim_scores)
    level = get_competency_level(overall_score)

    # 1. Competency level (and related headline numbers) shown first.
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall score", f"{overall_score:.1f}/100")
    with col2:
        st.metric("Competency level", level)
    with col3:
        st.metric("Field", st.session_state.selected_field)

    # 2. Skill assessment profile shown below that, heading centered,
    #    each chart on its own line, colored for the current mode.
    from config.settings import LIGHT_MODE, DARK_MODE
    text_color = DARK_MODE["text"] if st.session_state.dark_mode else LIGHT_MODE["text"]

    st.markdown("<h2 class='centered'>Skill assessment profile</h2>", unsafe_allow_html=True)
    st.plotly_chart(create_radar_chart(dim_scores, text_color), use_container_width=True, theme=None)
    st.plotly_chart(create_gauge_chart(overall_score, text_color), use_container_width=True, theme=None)

    with st.expander("Dimension breakdown"):
        render_dimension_table(dim_scores)

    st.markdown("---")
    st.markdown("<h2 class='centered'>Recommended next courses</h2>", unsafe_allow_html=True)

    recommendations = get_course_recommendations(dim_scores, st.session_state.selected_field,
                                                   courses_df, top_n=TOP_N_RECOMMENDATIONS)
    if recommendations:
        client = get_mistral_client()
        for i, rec in enumerate(recommendations, 1):
            link, is_ai = _resolve_link(client, rec['course'])
            render_course_card(i, rec['course'], rec['match_score'], rec['reasons'],
                                resolved_link=link, link_is_ai_suggested=is_ai)
    else:
        st.info("No course recommendations found.")

    st.markdown("---")
    b1, b2, b3 = st.columns([1, 2, 1])
    with b2:
        if st.button("Retake test", type="primary", use_container_width=True):
            go_to_page('home')

    report_df = pd.DataFrame({
        'Dimension': list(dim_scores.keys()),
        'Score': list(dim_scores.values()),
        'Level': [get_competency_level(s) for s in dim_scores.values()],
    })
    report_df.loc['Overall'] = ['Overall Score', overall_score, level]
    csv = report_df.to_csv(index=False)
    st.download_button("Download report", data=csv, file_name="skill_assessment_report.csv", mime="text/csv")


def render_footer(dark_mode):
    from config.settings import LIGHT_MODE, DARK_MODE
    text_color = DARK_MODE["text"] if dark_mode else LIGHT_MODE["text"]

    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: {text_color}; opacity: 0.7;'>
        <p>Course recommender system — Streamlit + Mistral AI</p>
        <p>Course data: Coursera Courses Dataset & Coursera Free Courses Dataset</p>
    </div>
    """, unsafe_allow_html=True)