from openai import OpenAI
from langsmith import traceable
from io import BytesIO

client = OpenAI()

@traceable
def process_audio(audio_file):
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["segment"]
    )
    return transcription

def generate_audio(text):
    # 1. Call the OpenAI API to generate the speech
    tts_response = client.audio.speech.create(
        model="tts-1",  # Use tts-1 or tts-1-hd for higher quality
        voice="alloy",  # Choose a voice: 'alloy', 'echo', 'fable', 'onyx', 'nova', or 'shimmer'
        input=text,
        response_format="mp3"
    )

    # 2. Read the binary content into a BytesIO object
    audio_fp = BytesIO()
    
    for chunk in tts_response.iter_bytes():
        audio_fp.write(chunk)
    
    audio_fp.seek(0) # Rewind the buffer to the beginning

    return audio_fp
