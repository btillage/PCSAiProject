'''
import whisper

model = whisper.load_model("base")
result = model.transcribe("meeting_audio.mp3", task="transcribe")
print(result['text'])
'''


'''
from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
)
streaming_config = speech.StreamingRecognitionConfig(config=config)
'''


import pyaudio
import whisper
from transformers import LlamaForCausalLM, LlamaTokenizer

# Load ASR and Llama
whisper_model = whisper.load_model("base")
llama_tokenizer = LlamaTokenizer.from_pretrained("meta/llama-3.1")
llama_model = LlamaForCausalLM.from_pretrained("meta/llama-3.1")

# Stream audio
def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    while True:
        data = stream.read(1024)
        # Process audio (e.g., save or transcribe in real-time)
        result = whisper_model.transcribe(data, task="transcribe")
        print("Transcribed Text:", result['text'])

        # Generate response with Llama
        input_prompt = f"Conversation so far: {result['text']}\nWhat should be said next?"
        inputs = llama_tokenizer(input_prompt, return_tensors="pt")
        outputs = llama_model.generate(**inputs, max_new_tokens=50)
        response = llama_tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("AI Response:", response)

record_audio()
