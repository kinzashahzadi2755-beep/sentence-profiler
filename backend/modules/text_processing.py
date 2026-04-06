import spacy
import re

# Load the small English NLP model for grammatical observation
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None
    print("Warning: SpaCy model 'en_core_web_sm' is not loaded.")

def clean_input(raw_text: str) -> str:
    """
    Cleans the text by normalizing whitespace.
    """
    return re.sub(r'\s+', ' ', raw_text).strip()

def process_text(raw_text: str):
    """
    Text Processing Pipeline core function.
    Connects to Conceptual Framework -> Step 1: Sentence Observation.
    
    Cleans the input and applies the NLP model to structure the text into
    sentences, count words, and prepare components for phrase extraction.
    """
    cleaned_text = clean_input(raw_text)
    
    if not nlp:
        # Fallback Mock NLP if the spacy model could not be downloaded
        class MockToken:
            def __init__(self, text, pos, dep):
                self.text = text
                self.pos_ = pos
                self.dep_ = dep
                self.lemma_ = text.lower()
                self.is_punct = not text.isalnum()
                self.is_space = text.isspace()
            def __len__(self): return len(self.text)
        
        class MockSpan:
            def __init__(self, tokens): self.tokens = tokens
            def __iter__(self): return iter(self.tokens)
            def __len__(self): return len(self.tokens)
        
        class MockDoc:
            def __init__(self, text):
                raw_tokens = text.split()
                self.tokens = [MockToken(t, 'NOUN' if len(t)>3 else 'VERB', 'nsubj' if len(t)<5 else 'amod') for t in raw_tokens]
                self.sents = [MockSpan(self.tokens)]
                self.noun_chunks = [MockSpan(self.tokens[:2])] if len(self.tokens) > 1 else []
            def __iter__(self): return iter(self.tokens)
            def __len__(self): return len(self.tokens)
            
        doc = MockDoc(cleaned_text)
    else:
        doc = nlp(cleaned_text)
        
    sentences = list(doc.sents)
    words = [token for token in doc if not token.is_punct and not token.is_space]
    
    return {
        "text_doc": doc,
        "sentences": sentences,
        "total_words": len(words),
        "total_sentences": len(sentences)
    }
