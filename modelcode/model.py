import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
import requests

nltk.download('punkt')

# For demonstration, let's use a simple dataset
data = {
    "input": ["Hello", "How are you?"],
    "output": ["Hi! How can I assist you?", "I'm good, thanks. How about you?"]
}

df = pd.DataFrame(data)

model_name = "t5-small"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def fetch_data_from_api():
    # Example API call
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def prepare_data(df):
    inputs = []
    outputs = []
    for index, row in df.iterrows():
        input_text = row['input']
        output_text = row['output']

        inputs.append(input_text)
        outputs.append(output_text)

    return inputs, outputs

def train_model(model, tokenizer, device, inputs, outputs):
    for epoch in range(3):  # Example epochs
        input_encodings = tokenizer(inputs, return_tensors='pt', padding=True).to(device)
        output_encodings = tokenizer(outputs, return_tensors='pt', padding=True).to(device)

        labels = output_encodings['input_ids']
        model.zero_grad()

        outputs = model(input_ids=input_encodings['input_ids'], attention_mask=input_encodings['attention_mask'], labels=labels)
        loss = outputs.loss

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        model.optimizer.step()

        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

    return model

inputs, outputs = prepare_data(df)
model = train_model(model, tokenizer, device, inputs, outputs)

# Save the model
model.save_pretrained("my_conversational_model")
tokenizer.save_pretrained("my_conversational_model")