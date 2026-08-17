"""Loads and merges the paid + free Coursera datasets into one unified table.
Column names are matched against several common naming variants, since raw
Kaggle downloads don't always use the exact headers you'd expect."""

import pandas as pd
import numpy as np
import streamlit as st

UNIFIED_COLS = ['Name', 'Provider', 'Difficulty', 'Rating', 'Link', 'Description', 'Skills', 'Price', 'Source']

COLUMN_CANDIDATES = {
    'Name': ['Name', 'Course Name', 'title', 'Title', 'course_name'],
    'Provider': ['University', 'Provider', 'course_by', 'Organization'],
    'Difficulty': ['Difficulty Level', 'Difficulty', 'level', 'Level', 'level, type and duration'],
    'Rating': ['Rating', 'Course Rating', 'ratings', 'rating'],
    'Link': ['Link', 'Course URL', 'url', 'URL'],
    'Description': ['Description', 'Course Description', 'description'],
    'Skills': ['Skills', 'skills'],
}


def _pick_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def _normalize_columns(df, source_label, price_value):
    """Map whatever columns exist in df onto the unified schema using
    COLUMN_CANDIDATES, so minor header naming differences (e.g. 'Course
    Name' vs 'Name') don't silently drop the whole dataset."""
    out = pd.DataFrame(index=df.index)
    for unified_col, candidates in COLUMN_CANDIDATES.items():
        found = _pick_column(df, candidates)
        out[unified_col] = df[found] if found else np.nan
    out['Price'] = price_value
    out['Source'] = source_label
    return out[UNIFIED_COLS]


@st.cache_data
def load_courses():
    frames = []

    try:
        main = pd.read_csv('data/coursera_courses.csv')
        main_normalized = _normalize_columns(main, source_label='Coursera (General Catalog)', price_value='Unknown')
        if main_normalized['Name'].notna().sum() == 0:
            st.warning(
                f"data/coursera_courses.csv loaded but no recognizable 'Name' column was found. "
                f"Actual columns in the file: {list(main.columns)}. "
                f"Update COLUMN_CANDIDATES in data/loader.py to include the real header name."
            )
        frames.append(main_normalized)
    except FileNotFoundError:
        st.error("data/coursera_courses.csv not found — this dataset is required.")

    try:
        free = pd.read_csv('data/coursera_free_courses.csv')
        free_normalized = _normalize_columns(free, source_label='Coursera (Free)', price_value='Free')
        if free_normalized['Name'].notna().sum() == 0:
            st.warning(
                f"data/coursera_free_courses.csv loaded but no recognizable 'Name' column was found. "
                f"Actual columns in the file: {list(free.columns)}."
            )
        frames.append(free_normalized)
    except FileNotFoundError:
        pass  # optional dataset — app works fine without it

    if not frames:
        return None

    merged = pd.concat(frames, ignore_index=True)
    merged = merged.dropna(subset=['Name'])  # rows we couldn't map a name for are useless for recommendations
    merged = merged.drop_duplicates(subset=['Name'], keep='first').reset_index(drop=True)
    return merged