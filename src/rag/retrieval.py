# src/tools/pinecone_retrieval.py
from rag.base import ensure_index

def pinecone_retrieval_raw(
    query: str,
    start_constraint: int = None,
    end_constraint: int = None,
    source: str = None,
    namespace: str = "ns1",
    index=None,
    top_k: int = 5,
):
    """
    Retrieve raw Pinecone search results.
    Returns list of matches (objects) without formatting.
    """
    if index is None:
        index = ensure_index("chatbot")

    pinecone_filter = {}
    if start_constraint is not None:
        pinecone_filter["start"] = {"$gte": start_constraint}
    if end_constraint is not None:
        pinecone_filter["end"] = {"$lte": end_constraint}
    if source is not None:
        pinecone_filter["source"] = source

    # Ensure query is non-empty
    query_text = query or " "

    response = index.search(
        namespace=namespace,
        query={
            "top_k": top_k,
            "filter": pinecone_filter,
            "inputs": {"text": query_text},
        },
    )

    return response.result.hits
