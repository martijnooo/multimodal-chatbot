from openai import OpenAI
from langsmith import traceable
from io import BytesIO
import io
import concurrent.futures
from pydub import AudioSegment

client = OpenAI()

@traceable
def process_audio_old(audio_file):
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
        model="tts-1",  
        voice="echo",  
        input=text,
        response_format="mp3"
    )

    # 2. Read the binary content into a BytesIO object
    audio_fp = BytesIO()
    
    for chunk in tts_response.iter_bytes():
        audio_fp.write(chunk)
    
    audio_fp.seek(0) # Rewind the buffer to the beginning

    return audio_fp



# --- Step 1: Split Audio and Get Chunks with Offsets ---

def split_audio_into_chunks(audio_path, duration_ms):
    """
    Splits a large audio file into smaller chunks of fixed duration.
    
    Returns: A list of tuples: (chunk_bytes_io, start_time_seconds)
    """
    print(f"Loading audio file: {audio_path}...")
    audio = AudioSegment.from_file(audio_path)
    print(f"Audio loaded. Total duration: {len(audio) / 1000} seconds.")

    chunks_with_offsets = []
    current_time_ms = 0

    while current_time_ms < len(audio):
        # Calculate the end time, ensuring it doesn't exceed the audio length
        end_time_ms = min(current_time_ms + duration_ms, len(audio))
        chunk = audio[current_time_ms:end_time_ms]

        # Use io.BytesIO to hold the chunk in memory (faster than writing to disk)
        chunk_io = io.BytesIO()
        chunk.export(chunk_io, format="mp3") # Export to a format Whisper accepts
        chunk_io.seek(0)
        
        # Store the chunk data and its original starting time (offset) in seconds
        start_time_seconds = current_time_ms / 1000.0
        chunks_with_offsets.append((chunk_io, start_time_seconds))

        current_time_ms = end_time_ms

    print(f"Split into {len(chunks_with_offsets)} chunks.")
    return chunks_with_offsets

# --- Step 2: Parallel Transcription and Timestamp Correction ---

def transcribe_and_correct(chunk_io, offset_s):
    """
    Transcribes a single audio chunk and re-bases its timestamps.
    """
    try:
        # The file parameter expects a file-like object with a name attribute.
        chunk_io.name = "chunk.mp3" 

        # Call the Whisper API
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=chunk_io,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

        # Re-base/Offset the timestamps
        corrected_segments = []
        # NOTE: transcription.segments is a list of TranscriptionSegment objects
        for segment_object in transcription.segments:
            
            # .model_dump() is the standard way to convert a Pydantic object to a dict
            segment_data = segment_object.model_dump()
            
            # Add the segment's starting offset to the local start and end times
            segment_data['start'] += offset_s
            segment_data['end'] += offset_s
            
            corrected_segments.append(segment_data)
            
        print(f"Chunk starting at {offset_s:.1f}s transcribed and corrected.")
        return corrected_segments

    except Exception as e:
        print(f"Error transcribing chunk at offset {offset_s:.1f}s: {e}")
        return []

# --- Step 3: Main Execution and Merging ---
@traceable
def process_audio(audio_path, max_workers=10):
    # 1. Split the audio
    chunks_with_offsets = split_audio_into_chunks(audio_path, 60000)

    # 2. Transcribe in parallel using a ThreadPoolExecutor
    all_corrected_segments = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks: (function, chunk_io, offset_s)
        future_to_offset = {
            executor.submit(transcribe_and_correct, chunk_io, offset_s): offset_s
            for chunk_io, offset_s in chunks_with_offsets
        }

        # Process results as they complete (order doesn't matter here)
        for future in concurrent.futures.as_completed(future_to_offset):
            segments = future.result()
            all_corrected_segments.extend(segments)

    # 3. Merge and Sort
    # The segments need to be sorted because parallel execution means they complete out of order.
    final_transcription = sorted(all_corrected_segments, key=lambda x: x['start']) 
    

    return {
        "text": " ".join([seg['text'] for seg in final_transcription]),
        "segments": final_transcription
    }