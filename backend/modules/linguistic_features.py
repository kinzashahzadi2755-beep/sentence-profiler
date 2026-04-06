def analyze_features(doc):
    """
    Framework Step 5: Linguistic Feature Analysis
    """
    words = [token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space]
    unique_words = set(words)
    lexical_diversity = len(unique_words) / len(words) if words else 0
    
    return {
        "lexical_diversity": round(lexical_diversity, 2),
        "unique_words": len(unique_words)
    }
