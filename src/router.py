from pipelines.audio_pipeline import run_audio_pipeline
# from pipelines.image_pipeline import run_image_pipeline
# from pipelines.pdf_pipeline import run_pdf_pipeline
# from pipelines.text_pipeline import run_text_pipeline
from rag.delete import delete_pinecone_records
from data_storage.delete_recods import delete_document, delete_chunks
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def process_file(uploaded_file, progress_text=None, progress_bar=None):
    mime_type = uploaded_file.type.lower()

    if mime_type.startswith("audio/"):
        return run_audio_pipeline(uploaded_file, progress_text=progress_text, progress_bar=progress_bar)

    if mime_type.startswith("image/"):
        return run_image_pipeline(uploaded_file)

    if mime_type == "application/pdf":
        return run_pdf_pipeline(uploaded_file)

    if mime_type.startswith("text/"):
        return run_text_pipeline(uploaded_file)

    # fallback by extension
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext in {"mp3","wav","m4a"}:
        return run_audio_pipeline(uploaded_file)
    if ext in {"jpg","jpeg","png"}:
        return run_image_pipeline(uploaded_file)
    if ext == "pdf":
        return run_pdf_pipeline(uploaded_file)
    if ext in {"txt","md"}:
        return run_text_pipeline(uploaded_file)

    raise ValueError("Unsupported file type")



def delete_file(uuid):
    logger.info(f"Deleting file {uuid}...")
    delete_pinecone_records(uuid)
    delete_document(uuid)
    delete_chunks(uuid)
    logger.info(f"File {uuid} deleted successfully.")
