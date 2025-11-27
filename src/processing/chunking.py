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