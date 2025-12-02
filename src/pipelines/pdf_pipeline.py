from PyPDF2 import PdfReader
from data_storage.add_document import add_document
from processing.summarize import create_summary
from rag.base import upload_records, ensure_index
from rag.build_records import create_chunk_records
import logging
from io import BytesIO
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

def run_pdf_pipeline(uploaded_file, file_uuid, progress_text=None, progress_bar=None):
    if progress_text: progress_text.text("Reading PDF in-memory...")

    pdf_bytes = uploaded_file.getbuffer()
    pdf_stream = BytesIO(pdf_bytes)  # wrap memoryview in BytesIO

    reader = PdfReader(pdf_stream)
    
    if progress_text: progress_text.text("Processing pages...")
    
    page_chunks = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text.strip():  # skip empty pages
            continue
        page_chunks.append({
            "page": i + 1,
            "text": text
        })
    
    full_text = "\n".join([p["text"] for p in page_chunks])
    summary = create_summary(full_text)
    
    index = ensure_index("chatbot")
    upload_records(index, "ns1", create_chunk_records(page_chunks, "user1", uploaded_file.name, uploaded_file.type, file_uuid))

    # Add document info
    add_document(user_id="user1", name=uploaded_file.name, type_=uploaded_file.type, summary=summary, document_uuid=file_uuid)
    
    if progress_bar: progress_bar.progress(100)
    if progress_text: progress_text.text("Done!")
    
    return {
        "type": "pdf",
        "summary": summary,
        "source": uploaded_file.name,
        "pages": len(page_chunks)
    }
