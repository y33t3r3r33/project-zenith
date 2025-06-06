import os
from groq import Groq

def main():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    print("Welcome to Project Zentih! Type 'quit' or 'exit' to exit.")
    chat_history = []

    while True:
        usrinput = input("Usr: ")

        if usrinput.lower() == 'exit':
            print("I see you don't need me anymore, goodbye then.")
            break

        if usrinput.lower() == 'quit':
            print("I see you don't need me anymore, goodbye then.")
            break

        chat_history.append({"role": "user", "content": usrinput})

        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="deepseek-r1-distill-llama-70b"
        )

        response = chat_completion.choices[0].message.content
        print("Project Zenith: ", response)
        print("Type 'quit' or 'exit' to exit")
        chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()