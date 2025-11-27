from rag.base import ensure_index
from langchain.tools import tool

@tool
def retrival(
    query: str,
    start_constraint: int = None,  
    end_constraint: int = None,
    source: str = None,
    namespace: str = "ns1",
    index = ensure_index("chatbot"),
    top_k: int = 5
):
    """Search the user documents storage for records matching the query.
    
    Args:
        query: Search terms to look for. You can also use a "zero" vector with 1024 dimensions to filter based on metadata only.
        start_constraint: In case of a video or audio file, when the transcript starts in seconds
        end_constraint: In case of a video or audio file, when the transcript ends in seconds
        source: The name of the file 
    """

    # Build a dynamic filter for Pinecone
    pinecone_filter = {}
    if start_constraint is not None:
        pinecone_filter["start"] = {"$gte": start_constraint}
    if end_constraint is not None:
        pinecone_filter["end"] = {"$lte": end_constraint}
    if source is not None:
        pinecone_filter["source"] = source

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