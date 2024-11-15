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
