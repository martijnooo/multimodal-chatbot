from langchain.tools import tool
from data_storage.chunks import get_chunks_around_timestamp


@tool
def time_based_retrieval(source: str, start_time: int, end_time: int, user_id: str = "user1"):
    """
    Retrieve transcript content based ONLY on time ranges.

    Use this tool when the user asks questions like:
    - "What is said around the 10 minute mark?"
    - "What happens between minute 5 and 7?"
    - "What was said just before 02:30?"

    This tool does NOT use semantic search and ignores query text.  
    It simply returns all chunks whose intervals intersect with [start_time, end_time].

    Args:
        source: The file name of the uploaded audio/video.
        start_time: Start of requested interval (seconds).
        end_time: End of requested interval (seconds).
    """
    chunks = get_chunks_around_timestamp(user_id, source, start_time, end_time)

    if not chunks:
        return f"No content found around {start_time} seconds in '{source}'."

    result = f"Content around {start_time} seconds:\n\n"
    for start, end, text in chunks:
        result += f"[{start:.1f}s → {end:.1f}s]\n{text}\n\n"

    return result
