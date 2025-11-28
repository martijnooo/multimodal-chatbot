from processing.audio import process_audio
from processing.chunking import chunk_by_time
from processing.summarize import create_summary
from rag.base import upload_records, ensure_index
from rag.build_records import create_summary_record, create_chunk_records
from data_storage.add_document import add_document
from data_storage.chunks import add_time_chunk
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run_audio_pipeline(uploaded_file, progress_text=None, progress_bar=None):
    if progress_text: progress_text.text("Transcribing audio...")
    transcript = process_audio(uploaded_file)
    if progress_bar: progress_bar.progress(30)

    if progress_text: progress_text.text("Chunking audio...")
    chunks = chunk_by_time(transcript.segments)
    if progress_bar: progress_bar.progress(60)

    if progress_text: progress_text.text("Creating summary...")
    summary = create_summary(transcript.text)
    if progress_bar: progress_bar.progress(80)

    if progress_text: progress_text.text("Uploading data...")
    # Upload chunks & summary
    index = ensure_index("chatbot")
    upload_records(index, "ns1", create_chunk_records(chunks, "user1", uploaded_file.name, uploaded_file.type))
    upload_records(index, "ns1", create_summary_record(summary, "user1", uploaded_file.name, uploaded_file.type))
    add_document("user1", uploaded_file.name, uploaded_file.type, summary)
    for ch in chunks:
        add_time_chunk(
            user_id="user1",
            source=uploaded_file.name,
            start=ch["start"],
            end=ch["end"],
            text=ch["text"]
        )
    if progress_bar: progress_bar.progress(100)
    if progress_text: progress_text.text("Done!")

    return {
        "type": "audio",
        "summary": summary,
        "source": uploaded_file.name,
        "duration": transcript.duration
    }


