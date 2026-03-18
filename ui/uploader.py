import streamlit as st


def render_uploader():
    """File uploader that indexes documents into the current pipeline."""
    pipeline = st.session_state.pipeline
    if pipeline is None:
        return

    uploaded = st.file_uploader(
        "Upload a document (PDF or TXT)",
        type=["pdf", "txt"],
        key=f"uploader_{st.session_state.mode}",
    )

    if uploaded and uploaded.name not in st.session_state.indexed_files:
        with st.spinner(f"Indexing **{uploaded.name}**..."):
            chunk_count = pipeline.index_file(uploaded)
        st.session_state.indexed_files.append(uploaded.name)
        st.success(f"Indexed **{uploaded.name}** ({chunk_count} chunks)")
        st.rerun()
