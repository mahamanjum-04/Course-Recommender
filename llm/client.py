"""Mistral API client setup."""

import os
import streamlit as st
from mistralai.client import Mistral


def get_mistral_client():
    """Returns a Mistral client using the key from the sidebar input (session
    state) or the MISTRAL_API_KEY environment variable. Returns None if no
    key is available or the client fails to initialize — callers should
    treat None as "use the offline fallback"."""
    api_key = st.session_state.get('api_key') or os.environ.get('MISTRAL_API_KEY')
    if not api_key:
        return None
    try:
        return Mistral(api_key=api_key)
    except Exception:
        return None