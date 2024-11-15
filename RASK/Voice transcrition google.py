'''
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
import queue

# Set up your Google Cloud credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-key.json"

# Audio stream parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Generate audio chunks for processing."""
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            yield chunk

def transcribe_streaming():
    """Stream audio to Google Speech-to-Text API and print the transcription."""
    client = speech.SpeechClient()
    
    # Configuration for the recognizer
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",  # Change to your preferred language
        enable_speaker_diarization=True,
        diarization_speaker_count=2,  # Adjust the number of speakers
        model="default",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        print_responses(responses)

def print_responses(responses):
    """Process responses from Google Speech-to-Text API."""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the interim or final transcription
        transcript = result.alternatives[0].transcript
        if result.is_final:
            print(f"Final: {transcript}")
        else:
            print(f"Interim: {transcript}", end="\r")

if __name__ == "__main__":
    print("Start speaking...")
    try:
        transcribe_streaming()
    except KeyboardInterrupt:
        print("\nExiting...")
'''
import speech_recognition as sr

def live_transcription():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Adjusting for ambient noise... Please wait.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Speak into the microphone.")

    try:
        while True:
            with mic as source:
                print("Listening...")
                audio = recognizer.listen(source)
                print("Processing...")

            # Recognize speech using Google Web Speech API
            try:
                transcription = recognizer.recognize_google(audio)
                print(f"Transcription: {transcription}")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
    except KeyboardInterrupt:
        print("\nStopping transcription.")

if __name__ == "__main__":
    live_transcription()
