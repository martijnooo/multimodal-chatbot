from langchain.tools import tool
from data_storage.chunks import get_chunks_around_timestamp, get_chunks_around_page


@tool
def time_based_retrieval(document_uuid: str, center: int, window: int = 60, user_id: str = "user1"):
    """
    Retrieve transcript content based ONLY on time ranges.

    Use this tool when the user asks questions like:
    - "What is said around the 10 minute mark?"
    - "What happens between minute 5 and 7?"
    - "What was said just before 02:30?"

    This tool does NOT use semantic search and ignores query text.  
    It simply returns all chunks whose intervals intersect with [start_time, end_time].

    Args:
        document_uuid : The file uuid of the uploaded audio/video.
        center: Requested time (seconds).
        window: time window in seconds around the center to search for. Can be adjusted to larger values to have higher chance of a hit.
    """
    chunks = get_chunks_around_timestamp(user_id, document_uuid, center, window)

    if not chunks:
        return f"No content found around {center} seconds in '{document_uuid}'."

    result = f"Content around {center} seconds:\n\n"
    for start, end, text in chunks:
        result += f"[{start:.1f}s → {end:.1f}s]\n{text}\n\n"

    return result

@tool
def page_based_retrieval(document_uuid: str, page_number: int, user_id: str = "user1"):
    """
    Retrieve document content based ONLY on page number.

    Use this tool when the user asks questions like:
    - "What is on page 5?"
    - "Show me content around page 10"

    This tool does NOT use semantic search and ignores query text.  

    Args:
        document_uuid : The file uuid of the uploaded document.
        page_number: Requested page number (1-indexed).
    """

    chunks = get_chunks_around_page(user_id, document_uuid, page_number)

    if not chunks:
        return f"No content found around page {page_number} in document '{document_uuid}'."

    result = f"Content around page {page_number}:\n\n"
    for page, text in chunks:
        result += f"[Page {page}]\n{text}\n\n"

    return result
