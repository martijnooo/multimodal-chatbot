def chunk_by_time(segments, chunk_size=45, overlap=10):
    chunks = []
    stride = chunk_size - overlap

    end_of_audio = segments[-1].end
    t = 0

    while t < end_of_audio:
        chunk_start = t
        chunk_end = t + chunk_size

        # collect all text covered by this window
        texts = []
        for seg in segments:
            if seg.end >= chunk_start and seg.start <= chunk_end:
                texts.append(seg.text.strip())

        if texts:
            chunks.append({
                "start": chunk_start,
                "end": chunk_end,
                "text": " ".join(texts)
            })

        t += stride

    return chunks

def chunk_by_length(text, max_length=1000):
    """
    Split a text into chunks of approximately max_length characters.
    Preserves paragraph boundaries if possible.

    Returns a list of dicts: {"text": ..., "start_paragraph": ..., "end_paragraph": ...}
    """
    chunks = []
    # 1. Split and filter out paragraphs that are empty or only whitespace
    paragraphs = [para.strip() for para in text.split("\n\n")]
    paragraphs = [para for para in paragraphs if para]  # Ensure it's not an empty string

    current_chunk = ""
    start_idx = 0  # paragraph index start (of the *filtered* list)

    for i, para in enumerate(paragraphs):
        # Calculate length with the separator if it were added
        len_with_para = len(current_chunk) + len(para) + 2

        if len_with_para <= max_length:
            # Add the paragraph and the separator (if this isn't the first item in the chunk)
            current_chunk += (para + "\n\n")
        else:
            # The current paragraph exceeds the limit, so save the current chunk first.
            
            # **2. Check if current_chunk has content before appending**
            # This handles the case where the very first paragraph is already > max_length
            if current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "start_paragraph": start_idx,
                    "end_paragraph": i - 1
                })
            
            # Start a new chunk with the current paragraph
            current_chunk = para + "\n\n"
            start_idx = i

    # Add last chunk
    # **2. Check if current_chunk has content before appending**
    if current_chunk:
        chunks.append({
            "text": current_chunk.strip(),
            "start_paragraph": start_idx,
            # The end index is the index of the last paragraph in the filtered list
            "end_paragraph": len(paragraphs) - 1
        })

    return chunks
