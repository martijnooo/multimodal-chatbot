from langchain.tools import tool
from rag import ensure_index

@tool
def retrival(
    query: str,
    start_constraint: int = None,  
    end_constraint: int = None,
    namespace: str = "ns1",
    index = ensure_index("chatbot"),
    top_k: int = 5
):
    """Search the user documents storage for records matching the query."""

    # Build a dynamic filter for Pinecone
    pinecone_filter = {}
    if start_constraint is not None:
        pinecone_filter["start"] = {"$gte": start_constraint}
    if end_constraint is not None:
        pinecone_filter["end"] = {"$lte": end_constraint}

    response = index.search(
        namespace=namespace,
        query={
            "top_k": top_k,
            "filter": pinecone_filter if pinecone_filter else {},
            "inputs": {'text': query}
        }
    )

    formatted_output_string = f"Found {len(response.result.hits)} matches.\n"

    for i, match in enumerate(response.result.hits):
        fields = match.fields
        meta_info = []

        # Dynamically check for metadata keys
        if "start" in fields and "end" in fields:
            meta_info.append(f"starting at {fields['start']}s, ending at {fields['end']}s")
        if "pages" in fields:
            meta_info.append(f"pages {fields['pages']}")

        match_string = (
            f"Match {i} with score {match._score}, {', '.join(meta_info)}:\n"
            f"{fields.get('text', '[no text available]')}\n"
        )
        formatted_output_string += match_string

    return formatted_output_string
