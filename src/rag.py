from typing import List, Dict
from dotenv import load_dotenv
import os
load_dotenv()
PINECONE = os.getenv('PINECONE')
from pinecone import Pinecone


def ensure_index(
    index_name: str,
    model_name: str = "llama-text-embed-v2",
    cloud: str = "aws",
    region: str = "us-east-1",
    field_map: Dict = {"text": "chunk_text"}
):
    """Create the Pinecone index if it does not exist."""
    pc = Pinecone(api_key=PINECONE)
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud=cloud,
            region=region,
            embed={
                "model": model_name,
                "field_map": field_map
            }
        )
    return pc.Index(index_name)

def build_records(
    chunks: List[Dict],
    user_id: str,
    source: str,
    type_: str,
    chunk_prefix: str = "chunk"
) -> List[Dict]:
    """
    Generic chunk -> Pinecone record builder.
    Automatically supports different metadata types (start/end, page, etc.)
    """
    records = []

    for i, chunk in enumerate(chunks):
        base = {
            "_id": f"{user_id}-{chunk_prefix}-{i}",
            "user": user_id,
            "text": chunk.get("text"),
            "source": source,
            "type": type_
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

def build_summary_record(
    summary_text: str,
    user_id: str,
    source: str,
    type_: str
) -> List[Dict]:
    """Create a summary document for Pinecone."""
    return [
        {
            "_id": f"{user_id}-summary",
            "user": user_id,
            "text": summary_text,
            "source": source,
            "type": type_
        }
    ]


def upload_records(
    index,
    namespace: str,
    records: List[Dict]
):
    """Upload a batch of records to Pinecone."""
    index.upsert_records(namespace, records)

def retrival(
        query: str,
        index,
        namespace: str,
        top_k: int = 5
        ):

    results = index.search(
        namespace= namespace,
        query={
            "top_k": top_k,
            "inputs": {
                'text': query
            }
        }
    )

    return results

if __name__ == "__main__":
    # Set dynamic values
    index_name = "chatbot"
    namespace = "ns1"
    user_id = "user1"
    source = "audio.mvp"

    # 1. Ensure index exists
    index = ensure_index(index_name)

    # 2. Prepare chunk uploads
    chunk_records = build_records(
        chunks=chunks,
        user_id=user_id,
        source=source,
        type_="audio"
    )

    # 3. Upload chunks
    upload_records(index, namespace, chunk_records)

    # 4. Prepare and upload summary
    summary_records = build_summary_record(
        summary_text=summary,
        user_id=user_id,
        source=source,
        type_="audio"
    )

    upload_records(index, namespace, summary_records)
