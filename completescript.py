import pyaudio
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel
import os
from groq import Groq
import pyttsx3
import threading

#Vosk Log Level
SetLogLevel(0) # 0 = debug, 1 = info, 2 = warning, 3 = error, 4 = none

#Load vosk model
model_path = "vosk-model-en-us-0.22"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

#Params
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 18000
CHUNK_SIZE = 2048

#Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)
def Recording():
    transcript = ""
    while True:
        data = stream.read(CHUNK_SIZE)
        if len(data) == 0:
            break

        #Process audio chunk
        if recognizer.AcceptWaveform(data):
            final_text = recognizer.Result()
            print(f"Final transcript: {final_text}")
        else:
            interim_text = recognizer.PartialResult()
            print(f"Interim transcript: {interim_text}")

        # if interim_text == "stop recording":
        #     print("Ending recording...")
        #     break

def AI():
    client = Groq(
        api_key=os.environ.get("GORQ_API_KEY")
    )

    print("Welcome!")
    chat_history = []

    while True:
        usrinput = input("User:")

        if usrinput.lower() == 'quit':
            print("Goodbye!")
            break

        chat_history.append({"role": "assistant", "content": usrinput})
        
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="qwen/qwen3-32b"
        )

        response = chat_completion.choices[0].message.content
        print("AI: ", response)
        print("Type 'quit' to exit")
        chat_history.append({"role": "assistant", "content": response})

print("Do you want to use text or speech?")
inp = input()

if inp == "text":
    AI()

elif inp == "speech":
    Recording()
    if interim_text == "stop recording":
        print("Ending Recording and Passing to AI...")


#Cleanup
stream.stop_stream()
stream.close()
p.terminate()