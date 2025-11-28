import streamlit as st
import os
import logging

# ----------------- Environment -----------------
os.environ["LANGSMITH_TRACING"] = st.secrets["langsmith"]["tracing"]
os.environ["LANGSMITH_ENDPOINT"] = st.secrets["langsmith"]["endpoint"]
os.environ["LANGSMITH_API_KEY"] = st.secrets["langsmith"]["api_key"]
os.environ["LANGSMITH_PROJECT"] = st.secrets["langsmith"]["project"]
os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]

from router import process_file
from agent.create import setup_agent
from agent.queries import run_query_with_memory

# ----------------- Logging -----------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ----------------- Initialize agent -----------------
if "agent" not in st.session_state:
    st.session_state.agent = setup_agent()

# ----------------- Chat UI -----------------
st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Accept user input
if prompt := st.chat_input("Ask something...", accept_file="multiple"):
    st.session_state.messages.append({"role": "user", "text": prompt.text})
    with st.chat_message("user"):
        st.markdown(prompt.text)

    file_context = None
    if prompt.files:
        st.info("Processing uploaded file...")
        # Placeholders for progress
        progress_text = st.empty()
        progress_bar = st.progress(0)

        # Pass placeholders to pipeline for step-by-step updates
        file_context = process_file(prompt.files[0], progress_text=progress_text, progress_bar=progress_bar)

        # Optionally show file summary / details
        with st.expander("File Details / Summary"):
            st.write(f"Type: {file_context['type']}")
            st.write(f"Source: {file_context['source']}")
            st.write(f"Summary: {file_context['summary']}")
            st.write(f"Duration: {file_context.get('duration', 'N/A')}s")

    # Run query using agent and optional file context
    agent = st.session_state.agent
    st.info("Querying your data...")
    answer = run_query_with_memory(
        agent=agent,
        prompt=prompt.text,
        memory_id="1",
        file_context=file_context
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "text": answer})
