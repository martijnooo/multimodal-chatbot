from docx import Document
from rag.base import upload_records, ensure_index
from rag.build_records import create_chunk_records
from data_storage.add_document import add_document
from processing.chunking import chunk_by_length
from processing.summarize import create_summary
import logging
from langsmith import traceable

# Shared logger
logger = logging.getLogger("chatbot")


@traceable(name="text_pipeline")
def run_text_pipeline(uploaded_file, doc_uuid, progress_text=None, progress_bar=None):
    if progress_text:
        progress_text.text("Reading Word document...")
    logger.info(f"Processing Word document: {uploaded_file.name}")

    doc = Document(uploaded_file)
    full_text = "\n".join([para.text for para in doc.paragraphs])

    if progress_bar: progress_bar.progress(20)

    if progress_text: progress_text.text("Chunking text...")
    chunks = chunk_by_length(full_text, max_length=500)
    if progress_bar: progress_bar.progress(50)

    if progress_text: progress_text.text("Creating summary...")
    summary = create_summary(full_text)
    if progress_bar: progress_bar.progress(80)

    if progress_text: progress_text.text("Uploading data...")
    index = ensure_index("chatbot")
    upload_records(
        index,
        "ns1",
        create_chunk_records(chunks, "user1", uploaded_file.name, uploaded_file.type, doc_uuid)
    )

    add_document("user1", uploaded_file.name, uploaded_file.type, summary, doc_uuid)
    logger.info(f"Finished processing Word document: {uploaded_file.name}")

    if progress_bar: progress_bar.progress(100)
    if progress_text: progress_text.text("Done!")

    return {
        "type": "text",
        "summary": summary,
        "source": uploaded_file.name,
        "chunks": chunks
    }
