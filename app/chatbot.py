import streamlit as st
import os

# Option 1: Set environment variables from secrets
os.environ["LANGSMITH_TRACING"] = st.secrets["langsmith"]["tracing"]
os.environ["LANGSMITH_ENDPOINT"] = st.secrets["langsmith"]["endpoint"]
os.environ["LANGSMITH_API_KEY"] = st.secrets["langsmith"]["api_key"]
os.environ["LANGSMITH_PROJECT"] = st.secrets["langsmith"]["project"]
os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]

from router import process_file
from agent.create import setup_agent
from agent.queries import run_query_with_memory

# Initialize agent once per session
if "agent" not in st.session_state:
    st.session_state.agent = setup_agent()

st.title("Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Accept user input
if prompt := st.chat_input("What is up?", accept_file="multiple"):
    # Store message to show chat history
    st.session_state.messages.append({
        "role": "user",
        "text": prompt.text
    })

    # Write text for chat
    with st.chat_message("user"):
        st.markdown(prompt.text)

    # Process any attachments
    file_context  = None
    if prompt.files:
        file_context  = process_file(prompt.files[0])

    # Run prompt query
    agent = st.session_state.agent
    answer = run_query_with_memory(agent=agent, prompt=prompt.text, memory_id= "1", file_context=file_context)

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "text": answer
    })
