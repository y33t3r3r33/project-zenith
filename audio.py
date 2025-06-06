import os
from groq import Groq
import whisper
import subprocess
import pyttsx3

"""
for api key run "export GROQ_API_KEY=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"
"""

# Init pyttsx3
#engine = pyttsx3.init()

# Set up Whisper model
model = whisper.load_model("large-v3-turbo")

def transcribe_audio(file_path):
    """Transcribe audio file using Whisper model"""
    result = model.transcribe(file_path)
    return result["text"]

def record_audio(duration=5):
    """Record audio for a specified duration"""
    # Use a command-line tool like arecord or ffmpeg to record audio
    # For simplicity, let's assume you're on a Linux system
    cmd = f"arecord -f dat -d {duration} temp_audio.wav"
    subprocess.run(cmd, shell=True)
    return "temp_audio.wav"

def main():
    engine = pyttsx3.init()
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    print("Welcome to Project Zentih! Type 'quit' to exit.")
    chat_history = []

    while True:
        usrinput = input("Usr: ")

        if usrinput.lower() == 'quit':
            print("I see you don't need me anymore, goodbye then.")
            break

     # Option to use voice input
        if usrinput.lower() == 'voice':
            print("How long do you need?")
            dur = input()
            audio_file = record_audio(duration=dur) # Record for10 seconds
            usrinput = transcribe_audio(audio_file)
            os.remove(audio_file) # Remove temp audio file (uncomment if needed)

        chat_history.append({"role": "user", "content": usrinput})
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="deepseek-r1-distill-llama-70b"
        )

        response = chat_completion.choices[0].message.content
        print("Project Zenith: ", response)
        print("Type 'quit' to exit")
        chat_history.append({"role": "assistant", "content": response})
        engine.say(response)
        engine.runAndWait()
if __name__ == "__main__":
 main()
