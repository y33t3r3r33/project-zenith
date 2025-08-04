from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

def load_model(model_name):
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def chat(model, tokenizer):
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        input_encodings = tokenizer(user_input, return_tensors='pt')
        model.zero_grad()

        outputs = model.generate(input_ids=input_encodings['input_ids'], attention_mask=input_encodings['attention_mask'])
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("Model:", response)

if __name__ == "__main__":
    model_name = "my_conversational_model"
    model, tokenizer = load_model(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    chat(model, tokenizer)