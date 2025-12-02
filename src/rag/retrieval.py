# src/tools/pinecone_retrieval.py
from rag.base import ensure_index
from dotenv import load_dotenv
import os
import numpy as np
load_dotenv()
PINECONE = os.getenv('PINECONE')
from pinecone import Pinecone

pc = Pinecone(api_key=PINECONE)



def embed_text(text: str):
    return pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={"input_type": "passage", "truncate": "END"}
    )

def pinecone_retrieval_raw(
    query: str = None,
    start_constraint=None,
    end_constraint=None,
    page=None,
    source=None,
    document_uuid=None,
    namespace="ns1",
    index=None,
    top_k=5,
):
    """
    If query is None or empty, perform metadata-only retrieval using a tiny random vector.
    """

    index = ensure_index("chatbot")

    # --------------------------
    # Build metadata filter
    # --------------------------
    metadata_filter = {}

    if start_constraint is not None:
        metadata_filter["start"] = {"$gte": start_constraint}

    if end_constraint is not None:
        metadata_filter["end"] = {"$lte": end_constraint}
    
    if page is not None:
        metadata_filter["page"] = page

    if source is not None:
        metadata_filter["source"] = source

    if document_uuid is not None:
        metadata_filter["document_uuid"] = document_uuid

    # --------------------------
    # Choose vector method
    # --------------------------
    if query is None or str(query).strip() == "":
        # Zero-vector query → metadata-only search
        vector = np.random.normal(scale=1e-6, size=1024).tolist()
    else:
        # Normal semantic search
        embedding = embed_text(query)
        vector = embedding.data[0].values

    # --------------------------
    # Query Pinecone
    # --------------------------
    result = index.query(
        namespace=namespace,
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        include_values=False,
        filter=metadata_filter if metadata_filter else None,
    )

    # Convert to your standard hit format
    return result.matches

