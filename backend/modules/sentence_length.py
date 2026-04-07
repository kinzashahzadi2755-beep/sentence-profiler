def analyze_length(doc, sentences):
    """
    Framework Step 2: Sentence Length Analysis
    """
    total_words = len(doc["all_words"])
    num_sentences = len(sentences)
    avg_length = total_words / num_sentences if num_sentences > 0 else 0
    return {
        "total_words": total_words,
        "total_sentences": num_sentences,
        "avg_length": round(avg_length, 2)
    }
