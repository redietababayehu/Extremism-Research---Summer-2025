#use pipeline from transformers to utilize NLP in the simplest way
from transformers import pipeline

# Load sentiment analysis pipeline that has already been pre trained
emotion_pipeline = pipeline("text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=False)

# Test its function with some hardcoded text 
texts = [
    "I love this product!",
    "This is the worst experience ever.",
    "It's okay, nothing special.",
    "Absolutely fantastic!",
    "Meh, it could be better."
]

# Analyze each line of text and print results
for text in texts:
    result = emotion_pipeline(text)[0]
    print(f"'{text}' → {result['label']} (confidence: {result['score']:.2f})")


