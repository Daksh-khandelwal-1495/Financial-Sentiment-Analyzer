from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

# Load FinBERT tokenizer and model
model_name = "yiyanghkust/finbert-tone"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Create a sentiment analysis pipeline
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Test sentence
sentence = "The company reported a record-breaking profit this quarter, beating analyst expectations."

# Predict sentiment
result = nlp(sentence)

# Show result
print(f"Sentence: {sentence}")
print("Sentiment prediction:", result)
