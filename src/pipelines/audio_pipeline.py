from processing.audio import process_audio
from processing.chunking import chunk_by_time
from processing.summarize import create_summary
from rag.base import upload_records, ensure_index
from rag.build_records import create_summary_record, create_chunk_records
from data_storage.add_document import add_document



def run_audio_pipeline(uploaded_file, doc_uuid, progress_text=None, progress_bar=None):

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
    upload_records(index, "ns1", create_chunk_records(chunks, "user1", uploaded_file.name, uploaded_file.type, doc_uuid))
    add_document("user1", uploaded_file.name, uploaded_file.type, summary, doc_uuid)

    if progress_bar: progress_bar.progress(100)
    if progress_text: progress_text.text("Done!")

    return {
        "type": "audio",
        "summary": summary,
        "source": uploaded_file.name,
        "duration": transcript.duration,
        "uuid": doc_uuid

    }


