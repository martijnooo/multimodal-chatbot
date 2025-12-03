from langchain.tools import tool
from rag.retrieval import pinecone_retrieval_raw


@tool
def retrival(
    query: str = None,
    start_constraint: int = None,
    end_constraint: int = None,
    page: int = None,
    source: str = None,
    document_uuid: str = None,
    namespace: str = "ns1",
    index=None,
    top_k: int = 5,
):
    """
    Meaning-based or metadata-based search.

    - If query is non-empty → semantic search.
    - If query is empty but metadata constraints exist → metadata-only retrieval.
    - If everything is empty → return warning.

    Args:
        query: Meaning-based search term. In case of metadata only search, leave empty. When used, the query must contain meaning for semantic search and can't be used for general queries on the document such as "summarise the content".
        start_constraint: Optional metadata filter (seconds).
        end_constraint: Optional metadata filter (seconds).
        source: Optional document name filter.
        document_uuid : Optional document uuid filter.
    """

    # If query is empty AND no metadata filters provided
    if (query is None or query.strip() == "") and not any(
        [start_constraint, end_constraint, page, source, document_uuid]
    ):
        return "Please provide either a semantic query or at least one metadata filter."

    hits = pinecone_retrieval_raw(
        query=query,
        start_constraint=start_constraint,
        end_constraint=end_constraint,
        page=page,
        source=source,
        document_uuid=document_uuid,
        namespace=namespace,
        index=index,
        top_k=top_k,
    )

    if not hits:
        return "No matches found."

    formatted_output = f"Found {len(hits)} matches.\n"
    
    for i, match in enumerate(hits):
        fields = match.metadata
        meta_info = []

        if "start" in fields and "end" in fields:
            meta_info.append(f"time {fields['start']}–{fields['end']}s")

        if "page" in fields:
            meta_info.append(f"page {fields['page']}")

        formatted_output += (
            f"Match {i} (score {round(float(match.score),2)}), "
            f"from {fields.get('source','unknown')}, "
            + ", ".join(meta_info) + ":\n"
            f"{fields.get('text', '[no text available]')}\n\n"
        )

    return formatted_output
