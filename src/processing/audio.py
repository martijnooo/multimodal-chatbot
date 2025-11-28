from openai import OpenAI
from langsmith import traceable

client = OpenAI()

@traceable
def process_audio(audio_file):
    transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["segment"]
    )
    return transcription

