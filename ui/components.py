"""Reusable UI pieces: course cards, dimension table."""

import pandas as pd
import streamlit as st

from config.settings import LIGHT_MODE, DARK_MODE, COLOR_PRIMARY, COLOR_ACCENT_YELLOW, COLOR_ACCENT_ORANGE


def render_course_card(rank, course, match_score, reasons, resolved_link=None, link_is_ai_suggested=False):
    col1, col2 = st.columns([4, 1])
    with col1:
        name = course.get('Name', 'Unnamed course')
        if resolved_link:
            st.markdown(f"### {rank}. [{name}]({resolved_link})")
        else:
            st.markdown(f"### {rank}. {name}")

        if link_is_ai_suggested:
            st.caption("Link found by AI — may not be accurate, please verify before using it.")
        elif resolved_link is None:
            st.caption("No link available for this course.")

        details = []
        if pd.notna(course.get('Provider')):
            details.append(f"{course['Provider']}")
        if pd.notna(course.get('Difficulty')):
            details.append(f"{course['Difficulty']}")
        if pd.notna(course.get('Rating')):
            try:
                details.append(f"{float(course['Rating']):.1f}/5")
            except (ValueError, TypeError):
                pass
        if details:
            st.write(" · ".join(details))

        if pd.notna(course.get('Description')) and course.get('Description'):
            with st.expander("Course description"):
                desc = str(course['Description'])
                st.write(desc[:500] + "..." if len(desc) > 500 else desc)

        if pd.notna(course.get('Skills')) and course.get('Skills'):
            skills = str(course['Skills']).split(',')[:5]
            st.write("**Skills:** " + " ".join(f"`{s.strip()}`" for s in skills))

        if reasons:
            st.write("**Why this course?** " + " · ".join(reasons))

    with col2:
        st.metric("Match", f"{match_score*100:.0f}%")
    st.markdown("---")


def render_dimension_table(dim_scores):
    """Hand-rendered HTML table instead of st.dataframe -- Streamlit's
    native dataframe grid is a compiled widget locked to the theme set
    once at startup, so it can't follow a runtime dark-mode toggle. This
    version reads the current mode directly and always matches."""
    from engine.scoring import get_competency_level

    dark = st.session_state.dark_mode
    palette = DARK_MODE if dark else LIGHT_MODE
    text_color = palette["text"]
    border_color = f"{text_color}33"

    def row_bg(score):
        if score < 40:
            return f"{COLOR_ACCENT_ORANGE}33"
        elif score < 70:
            return f"{COLOR_ACCENT_YELLOW}33"
        return f"{COLOR_PRIMARY}33"

    rows_sorted = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)

    body_rows = ""
    for dim, score in rows_sorted:
        level = get_competency_level(score)
        bg = row_bg(score)
        body_rows += (
            f"<tr style='background-color:{bg};'>"
            f"<td style='padding:8px 12px;color:{text_color};border-bottom:1px solid {border_color};'>{dim}</td>"
            f"<td style='padding:8px 12px;color:{text_color};border-bottom:1px solid {border_color};'>{score:.1f}</td>"
            f"<td style='padding:8px 12px;color:{text_color};border-bottom:1px solid {border_color};'>{level}</td>"
            f"</tr>"
        )

    html = f"""
    <table style='width:100%; border-collapse:collapse;'>
        <thead>
            <tr>
                <th style='text-align:left;padding:8px 12px;color:{text_color};border-bottom:2px solid {border_color};'>Dimension</th>
                <th style='text-align:left;padding:8px 12px;color:{text_color};border-bottom:2px solid {border_color};'>Score</th>
                <th style='text-align:left;padding:8px 12px;color:{text_color};border-bottom:2px solid {border_color};'>Level</th>
            </tr>
        </thead>
        <tbody>{body_rows}</tbody>
    </table>
    """
    st.markdown(html, unsafe_allow_html=True)