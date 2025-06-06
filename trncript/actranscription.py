import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel

#vosk setup/params
SetLogLevel(0) #0 = debug, 1 = info, 2 = warning, 3 = error, 4 = none

#load Model
model_path = "vosk-model-en-us-0.22"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

#record params
RATE = 16000
CHUNK_SIZE = 1024

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

