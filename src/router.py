from pipelines.audio_pipeline import run_audio_pipeline
# from pipelines.image_pipeline import run_image_pipeline
from pipelines.pdf_pipeline import run_pdf_pipeline
from pipelines.text_pipeline import run_text_pipeline
from rag.delete import delete_pinecone_records
from data_storage.delete_recods import delete_document, delete_chunks
import logging
import uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def process_file(uploaded_file, progress_text=None, progress_bar=None):
    logger.info(f"Processing file: {uploaded_file.name}")

    ext = uploaded_file.name.lower()

    file_uuid = str(uuid.uuid4())
    logger.info(f"Assigned UUID {file_uuid} to file {uploaded_file.name}")

    if ext.endswith(".mp3") or ext.endswith(".wav") or ext.endswith(".m4a"):
        return run_audio_pipeline(uploaded_file, file_uuid, progress_text, progress_bar)

    elif ext.endswith(".docx"):
        return run_text_pipeline(uploaded_file, file_uuid, progress_text, progress_bar)
    
    elif ext.endswith(".pdf"):
        return run_pdf_pipeline(uploaded_file, file_uuid, progress_text, progress_bar)

    else:
        raise ValueError(f"Unsupported file type: {ext}")



def delete_file(uuid):
    logger.info(f"Deleting file {uuid}...")
    delete_pinecone_records(uuid)
    delete_document(uuid)
    delete_chunks(uuid)
    logger.info(f"File {uuid} deleted successfully.")
