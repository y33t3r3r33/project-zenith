import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import whisper
from groq import Groq
import subprocess
import pyttsx3

#Setting things up

#pyttsx3
engine = pyttsx3.init()

#Vosk model stuff and params
model_path = "trncript/vosk-model-en-us-0.22"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)
SetLogLevel(3) #0 = debug, 1 = info, 2 = warning, 3 = error, 4 = none

#Recording params
RATE = 16000
CHUNK_SIZE = 1024
CHANNELS = 2

# def main():
#     print("Recording started...")
#     with sd.InputStream(channels=CHANNELS, samplerate=RATE, blocksize=CHUNK_SIZE) as stream:
#         while True:
#             data, overflow = stram.read(CHUNK_SIZE)
#             if overflow:
#                 print("Overflow Warning")
#
#             if recognizer.AcceptWaveform(data.tobytes()):
#                 final_text = recognizer.Result()
#                 print(f"Final Transcript: {final_text}")
#             else:
#                 interim_text = recognizer.PartialResult()
#                 print(f"Interim Trancript: {interim_text}")
#
# if __name__ == "__main__":
#     main()
#

print("Recording started...")
with sd.InputStream(channels=2, samplerate=RATE, blocksize=CHUNK_SIZE) as stream:
    while True:
        data, overflow = stream.read(CHUNK_SIZE)
        if overflow:
            print("YOUR BREAKING MY CODE WITH OVERFLOW")

        if recognizer.AcceptWaveform(data.tobytes()):
            final_text = recognizer.Result()
            print(f"Final Transcript: {final_text}")
        else:
            interim_text = recognizer.PartialResult()
            print(f"Interim Transcript: {interim_text}")
