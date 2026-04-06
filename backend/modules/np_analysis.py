def analyze_nps(doc):
    """
    Framework Step 4: Noun Phrase (NP) Complexity
    """
    noun_phrases = list(doc.noun_chunks)
    avg_np_length = sum([len(np) for np in noun_phrases]) / len(noun_phrases) if noun_phrases else 0
    
    # Simple modification check (optional extra detail)
    total_modifiers = sum([1 for np in noun_phrases for token in np if token.dep_ == 'amod'])
    
    return {
        "total_nps": len(noun_phrases),
        "avg_np_length": round(avg_np_length, 2),
        "total_modifiers": total_modifiers
    }
