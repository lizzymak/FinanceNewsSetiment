from fastapi import FastAPI
from pydantic import BaseModel
import torch
import pickle
import requests

from .model import TextClassifier 

from fastapi.middleware.cors import CORSMiddleware

import torch.nn.functional as F

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load vocab and model
with open("vocab.pkl", "rb") as f:
    vocab = pickle.load(f)
vocab_size = len(vocab)
num_classes = 3
embed_dim = 50


model = TextClassifier(vocab_size=vocab_size, embed_dim=embed_dim, num_classes=num_classes)
model.load_state_dict(torch.load("sentiment_model.pth"))
model.eval()

important_words = ["profit", "loss", "earnings", "revenue", "merger", "acquisition", "downgrade", "lawsuit", "bankruptcy", "ipo", "interest", "rate"]

class Headline(BaseModel):
    text: str

class BrandRequest(BaseModel):
    brand: str

def prediction(text, model, vocab, max_len = 50):
    model.eval()
    with torch.no_grad():
        # tokenize
        tokens = text.lower().split()
        token_ids = [vocab.get(word, vocab["<unk>"]) for word in tokens]

        # pad
        if len(tokens) < max_len:
            token_ids += [vocab["<pad>"]] * (max_len - len(token_ids))
        else:
            token_ids = token_ids[:max_len]
        
        label_map = {0: "negative", 1: "neutral", 2: "positive"}

        input_tensor = torch.tensor([token_ids])
        output = model(input_tensor)

        probs = F.softmax(output, dim=1) # rescales input and has it sum to 1, probability distribution
        predicted_class = torch.argmax(probs, dim=1).item() # picks class with highest probability
        return {
            "text": text, "prediction": label_map[predicted_class]
        }

@app.post("/predict")
def predict_sentiment(data: BrandRequest):
    API_KEY = "f726ca01832b44599b281c99e7a3d0b8"
    query = data.brand
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"

    response = requests.get(url).json()
    headlines = [article['title'] for article in response['articles']]

    # Filter headlines using important words
    filtered_headlines = [h for h in headlines if any(word in h.lower() for word in important_words)]
    top_headlines = filtered_headlines[:5]  # keep top 5

    results = []
    for h in top_headlines:
        results.append(prediction(h, model, vocab))
    return{"brand": data.brand, "headlines": results}
    
        
