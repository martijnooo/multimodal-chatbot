from typing import List, Dict


def create_chunk_records(
    chunks: List[Dict],
    user_id: str,
    source: str,
    type_: str,
    doc_uuid,
    chunk_prefix: str = "chunk"    
) -> List[Dict]:
    """
    Generic chunk -> Pinecone record builder.
    Automatically supports different metadata types (start/end, page, etc.)
    """
    records = []

    for i, chunk in enumerate(chunks):
        base = {
            "_id": f"{doc_uuid}-{chunk_prefix}-{i}",
            "user": user_id,
            "text": chunk.get("text"),
            "source": source,
            "type": type_,
            "document_uuid": doc_uuid
        }

        # include any metadata that exists
        # Only add these keys if present in chunk
        for key in ["start", "end", "page", "chapter", "section", "timestamp"]:
            if key in chunk:
                base[key] = chunk[key]

        # also include arbitrary metadata
        for k, v in chunk.items():
            if k not in base and k not in ("text",):
                base[k] = v
        
        records.append(base)

    return records


def create_summary_record(
    summary_text: str,
    user_id: str,
    source: str,
    type_: str,
    doc_uuid: str
) -> List[Dict]:
    """Create a summary document for Pinecone."""
    return [
        {
            "_id": f"{user_id}-summary",
            "user": user_id,
            "text": summary_text,
            "source": source,
            "type": type_,
            "document_uuid": doc_uuid
        }
    ]