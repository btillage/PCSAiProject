'''

import pyaudio
import wave
import whisper
from pyannote.audio import Pipeline

# Load Whisper model
whisper_model = whisper.load_model("base")

# Load Pyannote pipeline for speaker diarization
diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

# Function to capture audio and save it as a file
def record_audio(output_file="output.wav", record_seconds=10):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    
    print("Recording...")
    frames = []
    
    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Finished recording.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    return output_file

# Function to transcribe audio using Whisper
def transcribe_audio(audio_path):
    print("Transcribing audio...")
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# Function to diarize audio using Pyannote
def diarize_audio(audio_path):
    print("Performing speaker diarization...")
    diarization = diarization_pipeline(audio_path)
    speaker_segments = []
    for segment, speaker in diarization.itertracks(yield_label=True):
        speaker_segments.append((segment.start, segment.end, speaker))
    return speaker_segments

# Main function to combine transcription and speaker diarization
def main():
    audio_path = record_audio(record_seconds=15)  # Record 15 seconds of audio
    transcription = transcribe_audio(audio_path)
    speaker_segments = diarize_audio(audio_path)
    
    print("\n--- Final Output ---")
    for segment in speaker_segments:
        start, end, speaker = segment
        print(f"[Speaker {speaker}] ({start:.2f}s - {end:.2f}s): {transcription}")

if __name__ == "__main__":
    main()
'''

import pyaudio
import numpy as np
from pyannote.audio import Pipeline
import whisper
import wave
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Load Whisper model for transcription
whisper_model = whisper.load_model("base")

# Load Pyannote pipeline for speaker diarization
diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token="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"  # Replace with your token
)

# Function to process audio and save to a file for Pyannote
def save_audio_file(frames, rate, output_file="output.wav"):
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit audio
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    return output_file

# Function to transcribe audio
def transcribe_and_diarize(audio_path):
    # Transcription using Whisper
    transcription = whisper_model.transcribe(audio_path)["text"]

    # Speaker Diarization using Pyannote
    diarization = diarization_pipeline(audio_path)
    speaker_segments = []
    for segment, speaker in diarization.itertracks(yield_label=True):
        speaker_segments.append((segment.start, segment.end, speaker))
    
    return transcription, speaker_segments

# Real-time audio processing
def live_transcription():
    # Audio parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5  # Process 5 seconds at a time

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Listening...")

    try:
        while True:
            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            # Save audio to a file for processing
            audio_path = save_audio_file(frames, RATE)

            # Transcribe and diarize the audio
            transcription, speaker_segments = transcribe_and_diarize(audio_path)

            # Display the results
            print("\n--- Transcription ---")
            print(transcription)

            print("\n--- Speaker Segments ---")
            for start, end, speaker in speaker_segments:
                print(f"Speaker {speaker}: {start:.2f}s - {end:.2f}s")
    except KeyboardInterrupt:
        print("\nStopping transcription...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Run the live transcription
if __name__ == "__main__":
    live_transcription()
