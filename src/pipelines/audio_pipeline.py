from processing.audio import process_audio
from processing.chunking import chunk_by_time
from processing.summarize import create_summary
from rag.base import upload_records, ensure_index
from rag.build_records import create_summary_record, create_chunk_records
from data_storage.add_document import add_document

def run_audio_pipeline(uploaded_file):
    # 1. Whisper transcription
    transcript = process_audio(uploaded_file)

    # 2. Chunking for RAG use
    chunks = chunk_by_time(transcript.segments)

    # 3. Optional summary
    summary = create_summary(transcript.text)

    index_name = "chatbot"
    namespace = "ns1"
    user_id = "user1"
    source = uploaded_file.name.lower()
    file_type = uploaded_file.type.lower()

    # 1. Ensure index exists
    index = ensure_index(index_name)

    chunk_records = create_chunk_records(
            chunks=chunks,
            user_id=user_id,
            source=source,
            type_= file_type
        )

    # 3. Upload chunks
    upload_records(index, namespace, chunk_records)

    summary_records = create_summary_record(
            summary_text=summary,
            user_id=user_id,
            source=source,
            type_= file_type
        )

    upload_records(index, namespace, summary_records)

    # 4. Store document info in document storage
    add_document(user_id, source, file_type, summary)

    return {
        "type": "audio",
        "summary": summary,
        "source": uploaded_file.name,
        "duration": transcript.duration
    }

