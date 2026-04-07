def analyze_features(doc):
    """
    Framework Step 5: Linguistic Feature Analysis
    """
    words = [w.lower() for w, t in doc["all_words"]]
    unique_words = set(words)
    lexical_diversity = len(unique_words) / len(words) if words else 0
    
    return {
        "lexical_diversity": round(lexical_diversity, 2),
        "unique_words": len(unique_words)
    }
