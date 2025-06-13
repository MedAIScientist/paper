import asyncio
from pathlib import Path

import streamlit as st
from paperqa import Docs, Settings, agent_query

st.title("ArcheoRAG")

if "docs" not in st.session_state:
    st.session_state.docs = Docs(name="archeorag")

setting_name = st.selectbox(
    "Settings profile",
    ["default", "fast", "high_quality", "wikicrow", "contracrow"],
)

if setting_name == "default":
    settings = Settings()
else:
    settings = Settings.from_name(setting_name)

upload_dir = Path("archeorag/uploads")
upload_dir.mkdir(parents=True, exist_ok=True)

files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
if files:
    for file in files:
        file_path = upload_dir / file.name
        file_path.write_bytes(file.read())
        asyncio.run(st.session_state.docs.aadd(file_path, docname=file.name))
        st.success(f"Added {file.name}")

question = st.text_input("Ask a question about your papers")
if st.button("Submit") and question:
    response = asyncio.run(
        agent_query(question, settings, docs=st.session_state.docs)
    )
    st.markdown(response.session.formatted_answer)
