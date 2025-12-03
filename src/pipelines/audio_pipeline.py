from processing.audio import process_audio
from processing.chunking import chunk_by_time
from processing.summarize import create_summary
from rag.base import upload_records, ensure_index
from rag.build_records import create_chunk_records
from data_storage.add_document import add_document
import concurrent.futures
import logging

# Get the shared logger
logger = logging.getLogger("chatbot")

def run_audio_pipeline(uploaded_file, doc_uuid, progress_text=None, progress_bar=None):
    if progress_text: progress_text.text("Transcribing audio...")
    logger.info(f"Processing audio file: {uploaded_file.name}")

    transcript = process_audio(uploaded_file)
    if progress_bar: progress_bar.progress(30)

    if progress_text: progress_text.text("Processing transcript...")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Launch summary generation
        summary_future = executor.submit(create_summary, transcript["text"])
        # Launch chunking
        chunks_future = executor.submit(chunk_by_time, transcript["segments"])

        # Wait for chunking to finish while summary might still be running
        chunks = chunks_future.result()
        if progress_bar: progress_bar.progress(60)
        if progress_text: progress_text.text("Uploading data...")

        index = ensure_index("chatbot")
        logger.info(f"Uploading {len(chunks)} audio chunks")
        upload_records(
            index,
            "ns1",
            create_chunk_records(chunks, "user1", uploaded_file.name, uploaded_file.type, doc_uuid)
        )

        # Wait for summary if not done yet
        summary = summary_future.result()
        add_document("user1", uploaded_file.name, uploaded_file.type, summary, doc_uuid)
        logger.info(f"Finished processing audio file: {uploaded_file.name}")

    if progress_bar: progress_bar.progress(100)
    if progress_text: progress_text.text("Done!")

    return {
        "type": "audio",
        "summary": summary,
        "source": uploaded_file.name,
        "uuid": doc_uuid
    }
