# Dummy NLP profile analyzer using spaCy
import spacy
nlp = spacy.blank('en')

def analyze_profile(profile):
    # In real use, parse summary, posts, etc.
    doc = nlp(profile.get('summary', ''))
    insights = f"Keywords: {[token.text for token in doc]}"
    profile['insights'] = insights
    return profile
