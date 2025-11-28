# Multimodal Chatbot with RAG, Memory, and Streamlit

This project is a **multimodal AI chatbot** built with **Streamlit**, **LangChain/LangGraph-style agents**, **Pinecone RAG**, **Whisper transcription**, **SQLite document registry**, and **LangSmith tracing**. It supports:

* Audio file ingestion
* Automatic transcription (Whisper)
* Chunking & summarization for RAG
* Pinecone vector storage & retrieval
* Time-based queries on audio
* Multi-turn memory via thread IDs
* Per-user document registry using SQLite
* A clean Streamlit UX

---

## 🚀 Features

### 🔊 Audio Processing Pipeline

When a user uploads an audio file (`mp3`, `wav`, `m4a`):

1. Transcription using Whisper
2. Chunking of transcript by timestamps
3. Summarization of entire transcript
4. Chunks + summary stored in Pinecone
5. Document metadata stored in SQLite (`user_id`, filename, summary, type)
6. Context returned to the chat agent

### 📚 Retrieval (RAG)

* Vector search using **Pinecone**
* Supports **metadata filters** (start time, end time, source)
* Supports **full-text queries**
* Metadata-only queries use a neutral placeholder vector

### 🧠 Multi-turn Memory

* Implemented via `config={configurable: {thread_id: "..."}}`
* File uploads insert contextual system messages into the conversation

### 💾 SQLite Document Registry

Each uploaded file is recorded in a local SQLite database.

* User ID
* File source
* File type
* Summary
* Timestamp

Custom tools allow the agent to:

* List a user's uploaded documents
* Retrieve RAG data

### 🧪 LangSmith Integration

* Full tracing enabled
* Automatic logging of pipeline execution, chain calls, and tool invocations

---

## 📁 Project Structure

```
app/
│
├── app.py                     # Streamlit UI
├── router.py                  # File routing based on mime type
│
├── pipelines/
│   ├── audio_pipeline.py      # Full audio → RAG processing pipeline
│   ├── image_pipeline.py
│   ├── pdf_pipeline.py
│   └── text_pipeline.py
│
├── processing/
│   ├── audio.py               # Whisper transcription
│   ├── chunking.py            # Time-based chunking
│   └── summarize.py           # Summary LLM calls
│
├── rag/
│   ├── base.py                # Pinecone setup + uploads
│   ├── build_records.py       # Chunk + summary record builders
│   └── retrival.py            # Retrieval functions + tools
│
├── agent/
│   ├── create.py              # Setup of the main agent
│   └── queries.py             # Memory-aware query execution
│
├── data_storage/
│   ├── add_document.py        # Insert row into SQLite
│   └── list_documents.py      # Tool for agent to list user documents
│
└── database/
    ├── documents.db           # SQLite file
    └── init.sql               # Optional schema
```

---

## ⚙️ Setup

### 1️⃣ Clone & install

```bash
git clone <repo-url>
cd multimodal-chatbot
pip install -r requirements.txt
```

### 2️⃣ Add your secrets to Streamlit

`.streamlit/secrets.toml`:

```toml
[openai]
api_key = "YOUR_OPENAI_KEY"

[langsmith]
api_key = "YOUR_LANGSMITH_KEY"
project = "your-project-name"
endpoint = "https://api.smith.langchain.com"
tracing = "true"
```

### 3️⃣ Run the app

```bash
streamlit run app.py
```

---

## 📡 File Processing Flow

```
User uploads → router.py → audio_pipeline → Whisper
              ↓
              chunking → build records → Pinecone
              ↓
              SQLite document registry
              ↓
      Chat agent receives contextual system message
```

---

## 🔍 RAG Query Flow

```
User question → memory-aware query → agent → tools:
    - pinecone retrival tool
    - list_documents tool

Responses are enriched using RAG records & summaries.
```

---

## 🧠 Memory Handling

Uses LangChain’s configurable thread IDs:

```python
agent.invoke({"messages": [...]}, config={"configurable": {"thread_id": "1"}})
```

This persists state across turns.

---

## 🛠 Utilities

### Clearing the local SQLite database

A helper exists to wipe the document registry for debugging.

### Debug Logging

All pipelines include `logger.info()` calls.

LangSmith provides full chain/tool visibility.

---

## 🗺️ Roadmap

* Add login system for per-user persistent documents
* Add PDF & text pipeline
* Improve time-based retrieval UX
* Add agent streaming
* Add summarization-on-query for long documents
* Add real user IDs instead of "user1"

---

## 🤝 Contributing

PRs are welcome! If you want help restructuring the code, adding tests, or extending the pipeline, feel free to open an issue.

---

## 📄 License

MIT License.
