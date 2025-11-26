from openai import OpenAI
from langchain_openai import ChatOpenAI

client = OpenAI()

def create_summary(text):  
    llm = ChatOpenAI(
        model="gpt-5-nano"
    )
    messages = [
        (
            "system",
            "You are a text summariser. Provide a summary of the  text",
        ),
        ("human", text),
    ]
    response = llm.invoke(messages)
  
    return response

def process_audio(audio_file):
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["segment"]
    )
    return transcription


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

