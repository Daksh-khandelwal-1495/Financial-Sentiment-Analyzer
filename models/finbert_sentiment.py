# models/finbert_sentiment.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import streamlit as st

# Load model and tokenizer only once (cached)
@st.cache_resource(show_spinner="📦 Loading FinBERT model...")
def load_model():
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    return tokenizer, model

tokenizer, model = load_model()

@st.cache_data(ttl=3600)
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        labels = ["Negative", "Neutral", "Positive"]
        return {"label": labels[predicted_class]}
