import re
import os
import nltk

# Configure NLTK to use the bundled nltk_data directory inside the backend folder
nltk_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../nltk_data'))
if nltk_data_dir not in nltk.data.path:
    nltk.data.path.append(nltk_data_dir)

def clean_input(raw_text: str) -> str:
    """
    Cleans the text by normalizing whitespace.
    """
    return re.sub(r'\s+', ' ', raw_text).strip()

def process_text(raw_text: str):
    """
    Text Processing Pipeline core function using NLTK.
    """
    cleaned_text = clean_input(raw_text)
    
    try:
        sentences = nltk.sent_tokenize(cleaned_text)
    except:
        # Fallback if download failed
        sentences = [s.strip() for s in re.split(r'[.!?]+', cleaned_text) if s.strip()]
        if not sentences:
            sentences = [cleaned_text]
            
    processed_sentences = []
    all_words = []
    
    for sent in sentences:
        try:
            words = nltk.word_tokenize(sent)
            tagged = nltk.pos_tag(words)
        except:
            # Fallback
            words = sent.split()
            tagged = [(w, 'NN') for w in words]
            
        processed_sentences.append(tagged)
        for w, t in tagged:
            if w.isalnum():
                all_words.append((w, t))
                
    doc = {
        "text": cleaned_text,
        "processed_sentences": processed_sentences,
        "all_words": all_words
    }
    
    return {
        "text_doc": doc,
        "sentences": processed_sentences,
        "total_words": len(all_words),
        "total_sentences": len(sentences)
    }
