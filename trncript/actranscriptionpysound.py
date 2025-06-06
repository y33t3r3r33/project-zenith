import pyaudio
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel
import os

# Set up Vosk
SetLogLevel(0)  # 0 = debug, 1 = info, 2 = warning, 3 = error, 4 = none

# Load the Vosk model
model_path = "vosk-model-en-us-0.22"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

print("Recording started...")

while True:
    data = stream.read(CHUNK_SIZE)
    if len(data) == 0:
        break

    # Process the audio chunk
    if recognizer.AcceptWaveform(data):
        final_text = recognizer.Result()
        print(f"Final transcript: {final_text}")
    else:
        interim_text = recognizer.PartialResult()
        print(f"Interim transcript: {interim_text}")

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
