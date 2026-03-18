import streamlit as st

from state.session import set_mode


def render_sidebar():
    """Render sidebar with mode toggle and credential inputs."""
    with st.sidebar:
        st.header("Configuration")

        mode = st.radio("Mode", ["Local", "Cloud"],
                        index=0 if st.session_state.mode == "Local" else 1)
        set_mode(mode)

        if mode == "Local":
            st.info("Using **Ollama** (embeddings + LLM) and **ChromaDB**.\n\n"
                    "Make sure Ollama is running with `llama3.2` and `nomic-embed-text` pulled.")
        else:
            st.session_state.openai_api_key = st.text_input(
                "OpenAI API Key", type="password",
                value=st.session_state.openai_api_key,
            )
            st.session_state.mongodb_uri = st.text_input(
                "MongoDB Atlas URI", type="password",
                value=st.session_state.mongodb_uri,
            )
            if not st.session_state.openai_api_key or not st.session_state.mongodb_uri:
                st.warning("Enter both OpenAI API Key and MongoDB URI to use Cloud mode.")

        if st.session_state.indexed_files:
            st.divider()
            st.subheader("Indexed Files")
            for name in st.session_state.indexed_files:
                st.write(f"- {name}")
