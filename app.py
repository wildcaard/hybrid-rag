import streamlit as st

from state.session import initialize
from ui.sidebar import render_sidebar
from ui.uploader import render_uploader
from ui.chat import render_chat


def build_pipeline(mode: str, **kwargs):
    """Factory: build a RAGPipeline for the given mode with delayed imports."""
    from rag.pipeline import RAGPipeline

    if mode == "Local":
        from rag.embeddings.local_embeddings import LocalEmbeddingProvider
        from rag.vectorstores.local_store import LocalVectorStoreProvider
        from rag.llm.local_llm import LocalLLMProvider

        emb = LocalEmbeddingProvider()
        vec = LocalVectorStoreProvider(emb.get_embeddings())
        llm = LocalLLMProvider()
    else:
        from rag.embeddings.cloud_embeddings import CloudEmbeddingProvider
        from rag.vectorstores.cloud_store import CloudVectorStoreProvider
        from rag.llm.cloud_llm import CloudLLMProvider

        api_key = kwargs["openai_api_key"]
        mongodb_uri = kwargs["mongodb_uri"]

        emb = CloudEmbeddingProvider(api_key=api_key)
        vec = CloudVectorStoreProvider(emb.get_embeddings(), mongodb_uri=mongodb_uri)
        llm = CloudLLMProvider(api_key=api_key)

    return RAGPipeline(emb, vec, llm)


def main():
    st.set_page_config(page_title="Hybrid RAG", page_icon="📄", layout="wide")
    st.title("Hybrid RAG Chat")

    initialize()
    render_sidebar()

    # Build pipeline if not yet created
    mode = st.session_state.mode
    if st.session_state.pipeline is None:
        if mode == "Local":
            st.session_state.pipeline = build_pipeline("Local")
        elif (st.session_state.openai_api_key and st.session_state.mongodb_uri):
            st.session_state.pipeline = build_pipeline(
                "Cloud",
                openai_api_key=st.session_state.openai_api_key,
                mongodb_uri=st.session_state.mongodb_uri,
            )

    render_uploader()
    render_chat()


if __name__ == "__main__":
    main()
