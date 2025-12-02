from docx import Document
from rag.base import upload_records, ensure_index
from rag.build_records import create_chunk_records
from data_storage.add_document import add_document
from processing.chunking import chunk_by_length
from processing.summarize import create_summary
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run_text_pipeline(uploaded_file, doc_uuid, progress_text=None, progress_bar=None):

    if progress_text:
        progress_text.text("Reading Word document...")
    
    # --- Read Word file ---
    doc = Document(uploaded_file)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    
    if progress_bar:
        progress_bar.progress(20)

    if progress_text:
        progress_text.text("Chunking text...")
    
    # --- Chunk text ---
    chunks = chunk_by_length(full_text, max_length=500)
    
    if progress_bar:
        progress_bar.progress(50)

    if progress_text:
        progress_text.text("Creating summary...")
    
    # --- Create summary ---
    summary = create_summary(full_text)
    
    if progress_bar:
        progress_bar.progress(80)

    if progress_text:
        progress_text.text("Uploading data...")
    
    # --- Upload to Pinecone ---
    index = ensure_index("chatbot")
    upload_records(index, "ns1", create_chunk_records(chunks, "user1", uploaded_file.name, uploaded_file.type, doc_uuid))
 
    # --- Store document in SQLite ---
    add_document("user1", uploaded_file.name, uploaded_file.type, summary, doc_uuid)
    
    if progress_bar:
        progress_bar.progress(100)
    if progress_text:
        progress_text.text("Done!")

    return {
        "type": "text",
        "summary": summary,
        "source": uploaded_file.name,
        "chunks": chunks
    }
