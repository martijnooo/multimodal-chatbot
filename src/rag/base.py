from typing import List, Dict
from dotenv import load_dotenv
import os
load_dotenv()
PINECONE = os.getenv('PINECONE')
from pinecone import Pinecone

def ensure_index(
    index_name: str = "chatbot",
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

def upload_records(
    index,
    namespace: str,
    records: List[Dict]
):
    """Upload a batch of records to Pinecone."""
    index.upsert_records(namespace, records)