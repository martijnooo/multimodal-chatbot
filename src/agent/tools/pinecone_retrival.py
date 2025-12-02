from langchain.tools import tool
from rag.retrieval import pinecone_retrieval_raw

@tool
def retrival(
    query: str,
    start_constraint: int = None,
    end_constraint: int = None,
    source: str = None,
    document_uuid: str = None,
    namespace: str = "ns1",
    index=None,
    top_k: int = 5,
):
    """
    Semantic search through the user-uploaded documents. This needs to be a query for semantic meaning and NOT a general one like: "Briefly summarize what this document is about, including the type of document, period covered, etc."

    Use this when the user asks meaning-based questions like:
    - "What did the document say about neural networks?"
    - "What was mentioned about customer satisfaction after minute 10?"
    - "Find references to topic X."

    Do NOT use this for time-based questions such as:
    - "What is said at 8 minutes?" → Use time_based_retrieval instead.

    Args:
        query: Meaning-based search term. Must NOT be empty. 
        start_constraint: Optional metadata filter (seconds).
        end_constraint: Optional metadata filter (seconds).
        source: Optional document name filter.
        document_uuid : Optional document uuid filter.
    """
    hits = pinecone_retrieval_raw(
        query=query,
        start_constraint=start_constraint,
        end_constraint=end_constraint,
        source=source,
        document_uuid=document_uuid ,
        namespace=namespace,
        index=index,
        top_k=top_k,
    )

    if not hits:
        return "No matches found."

    formatted_output = f"Found {len(hits)} matches.\n"
    for i, match in enumerate(hits):
        fields = match.fields
        meta_info = []
        if "start" in fields and "end" in fields:
            meta_info.append(f"starting at {fields['start']}s, ending at {fields['end']}s")
        if "pages" in fields:
            meta_info.append(f"pages {fields['pages']}")

        formatted_output += (
            f"Match {i} with score {round(float(match._score),2)} from {fields["source"]}, {', '.join(meta_info)}:\n"
            f"{fields.get('text', '[no text available]')}\n"
        )

    return formatted_output
