import streamlit as st

KEYS = {
    "mode": "Local",
    "pipeline": None,
    "chat_history": [],
    "indexed_files": [],
    "openai_api_key": "",
    "mongodb_uri": "",
}


def initialize():
    """Set default session state values if not already present."""
    for key, default in KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def set_mode(mode: str):
    """Switch mode, clearing pipeline and chat state."""
    if st.session_state.mode != mode:
        st.session_state.mode = mode
        st.session_state.pipeline = None
        st.session_state.chat_history = []
        st.session_state.indexed_files = []
