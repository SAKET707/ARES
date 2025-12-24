
import streamlit as st

#file cache
def _ensure_file_cache():
    if "file_cache" not in st.session_state:
        st.session_state.file_cache = {}


def get_file_cached(path: str):
    _ensure_file_cache()
    return st.session_state.file_cache.get(path)


def set_file_cached(path: str, content: str):
    _ensure_file_cache()
    st.session_state.file_cache[path] = content


def clear_file_cache():
    if "file_cache" in st.session_state:
        del st.session_state.file_cache
