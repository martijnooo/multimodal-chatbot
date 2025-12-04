# Multimodal Chatbot with RAG, Memory, and Streamlit

This project is a **multimodal AI chatbot** built with **Streamlit**, **LangChain/LangGraph-style agents**, **Pinecone RAG**, **Whisper transcription**, **SQLite document registry**, and **LangSmith tracing**. It supports:

* Audio, text and pdf  multi-file ingestion
* Automatic transcription (Whisper)
* Chunking & summarization for RAG
* Pinecone vector storage & retrieval
* Time-based queries on audio
* Page-based queries for text
* Multi-turn memory via thread IDs
* Per-user document registry using SQLite
* A clean Streamlit UX

---

## 🚀 Key Features

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
* Supports **metadata filters** (start time, end time, page, source)
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

## 🪧 Demo
--> Click image
[![Multimodal Chatbot Demo](interface.jpg)](https://app.guidde.com/share/playbooks/5PZSB4AHr22j7N51dTsMKi?origin=1PiE387AxNZmNhZQ5XHK5q8jKcw2)

---

## 📁 Project Structure

```
├── app/
│   ├── .streamlit/
│   │   ├── config.toml
│   │   └── secrets.toml
│   └── chatbot.py          # Main streamlit app
├── data/                   # SQLLite database for document registry
│   └── user_data/
│       ├── documents.db
│       └── setup.ipynb
└── src/
    ├── __init__.py
    ├── router.py
    ├── agent/              # Agent setup including tools, query and templates
    │   ├── __init__.py
    │   ├── create.py
    │   ├── prompt_templates.py
    │   ├── queries.py
    │   └── tools/
    │       ├── pinecone_retrival.py
    │       └── sql_retrival.py
    ├── data_storage/       # Interaction with SQLLite database
    │   ├── add_document.py
    │   ├── delete_documents.py
    │   ├── delete_recods.py
    │   └── list_documents.py
    ├── pipelines/          # Orchestrator pipelines for uploaded input
    │   ├── __init__.py
    │   ├── audio_pipeline.py
    │   ├── pdf_pipeline.py
    │   └── text_pipeline.py
    ├── processing/         # Processing functions for uploaded input
    │   ├── __init__.py
    │   ├── audio.py
    │   ├── chunking.py
    │   └── summarize.py
    └── rag/                # Pinecone interaction for storing and retrival
        ├── __init__.py
        ├── base.py
        ├── build_records.py
        ├── delete.py
        └── retrieval.py
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

[pinecone]
api_key = "Your_PINECONE_KEY"

```

### 3️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🗺️ Roadmap

* Add login system for per-user persistent documents
* Add chat history


---

## 🤝 Contributing

PRs are welcome! If you want help restructuring the code, adding tests, or extending the pipeline, feel free to open an issue.
