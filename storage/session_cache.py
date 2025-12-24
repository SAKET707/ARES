
import streamlit as st

#session_cache
def _ensure_cache():
    if "repo_cache" not in st.session_state:
        st.session_state.repo_cache = {}


def get_cached(key: str):
    _ensure_cache()
    return st.session_state.repo_cache.get(key)


def set_cached(key: str, value):
    _ensure_cache()
    st.session_state.repo_cache[key] = value


def clear_cache():
    if "repo_cache" in st.session_state:
        del st.session_state.repo_cache
