from PyPDF2 import PdfReader
from data_storage.add_document import add_document
from data_storage.chunks import add_page_chunk
from processing.summarize import create_summary
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
        # Store page in SQLite
        add_page_chunk(user_id="user1", document_uuid=file_uuid, page=i+1, content=text)
    
    
    full_text = "\n".join([p["text"] for p in page_chunks])
    summary = create_summary(full_text)
    
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
