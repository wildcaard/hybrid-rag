import streamlit as st


def render_chat():
    """Display chat history and handle new user input."""
    pipeline = st.session_state.pipeline
    if pipeline is None:
        return

    if not st.session_state.indexed_files:
        st.info("Upload a document to start chatting.")
        return

    # Display existing messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle new input
    if question := st.chat_input("Ask a question about your documents"):
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Pass all history except the latest user message (it's the input)
                history = st.session_state.chat_history[:-1]
                answer = pipeline.query(question, history)
            st.markdown(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
