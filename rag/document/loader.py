import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


def load_uploaded_file(uploaded_file) -> list[Document]:
    """Load a Streamlit UploadedFile into LangChain Documents."""
    suffix = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    try:
        if suffix == ".pdf":
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path, encoding="utf-8")
        docs = loader.load()
    finally:
        os.unlink(tmp_path)

    # Tag each document with the original filename
    for doc in docs:
        doc.metadata["source_file"] = uploaded_file.name

    return docs
