from langchain.tools import tool
from rag.retrieval import pinecone_retrieval_raw

@tool
def retrival(
    query: str,
    start_constraint: int = None,
    end_constraint: int = None,
    source: str = None,
    namespace: str = "ns1",
    index=None,
    top_k: int = 5,
):
    """Search the user documents storage for records matching the query.
    
    Args:
        query: Search terms to look for. Must be a non-empty string.
        start_constraint: In case of a video or audio file, when the transcript starts in seconds
        end_constraint: In case of a video or audio file, when the transcript ends in seconds
        source: The name of the file 
    """
    hits = pinecone_retrieval_raw(
        query=query,
        start_constraint=start_constraint,
        end_constraint=end_constraint,
        source=source,
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
            f"Match {i} with score {match._score}, {', '.join(meta_info)}:\n"
            f"{fields.get('text', '[no text available]')}\n"
        )

    return formatted_output
