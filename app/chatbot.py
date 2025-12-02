import streamlit as st
import os

# --- Imports (Assuming these are correct and available) ---
from router import process_file
from agent.create import setup_agent
from agent.queries import run_query_with_memory
from data_storage.list_documents import list_documents
from router import delete_file
from processing.audio import generate_audio 
# --------------------------------------------------------

# ----------------- Environment Setup -----------------
try:
    os.environ["LANGSMITH_TRACING"] = st.secrets["langsmith"]["tracing"]
    os.environ["LANGSMITH_ENDPOINT"] = st.secrets["langsmith"]["endpoint"]
    os.environ["LANGSMITH_API_KEY"] = st.secrets["langsmith"]["api_key"]
    os.environ["LANGSMITH_PROJECT"] = st.secrets["langsmith"]["project"]
    os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]
except KeyError as e:
    st.error(f"Missing required secret: {e}. Please check your `secrets.toml`.")
    st.stop()


# ----------------- Initialize Agent and Session State -----------------
@st.cache_resource
def get_agent():
    """Initializes the agent and caches it."""
    return setup_agent()

if "agent" not in st.session_state:
    st.session_state.agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Initialize the audio state if it doesn't exist
if "audio_enabled" not in st.session_state:
    st.session_state.audio_enabled = True # Default to ON

st.title("💡 Multimodal Chatbot")

# --- Sidebar for File Management and Configuration (REVISED) ---
with st.sidebar:
    st.header("⚙️ Configuration")

    # 1. AUDIO TOGGLE (New Feature)
    # Checkbox state is automatically managed by Streamlit's session state
    st.session_state.audio_enabled = st.checkbox(
        "🔊 Enable Audio Responses", 
        value=st.session_state.audio_enabled, 
        help="Turn on to receive Text-to-Speech audio alongside text replies."
    )
    
    st.markdown("---")
    
    # 2. FILE MANAGEMENT (Existing)
    st.header("🗃️ File Management")

    docs = list_documents("user1")
    
    if docs:
        st.subheader("Uploaded Documents")
        doc_data = [
            {"ID": doc[0], "File Name": doc[1], "Uploaded On": doc[4]}
            for doc in docs
        ]

        st.dataframe(
            doc_data, 
            column_order=("File Name", "Uploaded On", "ID"),
            hide_index=True,
            use_container_width=True,
            column_config={
                "ID": st.column_config.TextColumn("ID", disabled=True),
                "File Name": st.column_config.TextColumn("File Name", width="medium"),
                "Uploaded On": st.column_config.DatetimeColumn("Uploaded On", format="YYYY-MM-DD HH:mm:ss"),
            }
        )

        doc_to_delete = st.text_input("Enter Document ID to Remove", key="delete_id_input")
        if st.button("🗑️ Remove Document by ID"):
            if doc_to_delete:
                try:
                    delete_file(doc_to_delete)
                    st.success(f"Document ID '{doc_to_delete}' deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting file: {e}")
            else:
                st.warning("Please enter a Document ID.")
    else:
        st.info("No documents uploaded yet.")
    
    st.markdown("---")
    st.caption("Agent Status: Ready")
    
# --- Main Chat UI ---

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Accept user input (prompt and file upload integrated)
if prompt := st.chat_input("Ask something or upload files to chat...", accept_file="multiple"):
    # 1. User message
    user_prompt_text = prompt.text
    st.session_state.messages.append({"role": "user", "text": user_prompt_text})
    with st.chat_message("user"):
        st.markdown(user_prompt_text)

    # Placeholder for the assistant's response during processing
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 2. File processing and context gathering
        file_context = []
        if prompt.files:
            message_placeholder.markdown("🔍 **Processing uploaded files...**")
            
            # ... (File processing logic remains the same)
            for f in prompt.files:
                with st.container():
                    st.caption(f"Handling: **{f.name}**")
                    progress_text = st.empty()
                    progress_bar = st.progress(0)
                    
                    result = process_file(f, progress_text, progress_bar)
                    file_context.append(result)
                    
                    progress_bar.empty()
                    progress_text.empty()
            
            message_placeholder.markdown("🧠 **Generating response...**")

        # 3. Run query using agent
        agent = st.session_state.agent
        
        with st.spinner("Thinking..."):
            answer = run_query_with_memory(
                agent=agent,
                prompt=user_prompt_text,
                memory_id="1",
                file_context=file_context
            )
        
        # 4. Display assistant response
        message_placeholder.markdown(answer)

        # 5. Conditional Text-to-Speech Implementation (REVISED LOGIC)
        if st.session_state.audio_enabled:
            st.caption("🔊 Generating audio...")
            try:
                # Only call generate_audio if the toggle is ON
                audio_bytes = generate_audio(answer)
                st.audio(audio_bytes, format='audio/mp3')
            except Exception as e:
                st.error("Could not generate audio response.")
                st.exception(e)

        # 6. Append assistant message to session state
        st.session_state.messages.append({"role": "assistant", "text": answer})