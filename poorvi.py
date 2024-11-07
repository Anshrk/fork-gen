from textblob import TextBlob
import spacy

# Load Spacy's English model for NLP
nlp = spacy.load("en_core_web_sm")

def analyze_text(title, description):
    # Combine title and description
    text = title + " " + description
    
    # Sentiment analysis using TextBlob
    sentiment = TextBlob(text).sentiment
    
    # Keyword extraction using Spacy
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    
    return sentiment, keywords

title = "Vectors | Chapter 1, Essence of linear algebra"
description = "In this video, we dive into the fundamentals of vectors, the building blocks of linear algebra. Learn about their key properties, operations, and how they form the foundation for understanding more advanced concepts in linear algebra. From vector addition and scalar multiplication to their application in solving real-world problems, this chapter will guide you through the essence of vectors and how they relate to systems of equations, geometry, and more. Perfect for students and anyone looking to deepen their understanding of linear algebra!"

sentiment, keywords = analyze_text(title, description)

print(f"Sentiment: {sentiment}")
print(f"Keywords: {keywords}")