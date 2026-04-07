import nltk

def analyze_nps(doc):
    """
    Framework Step 4: Noun Phrase (NP) Complexity using NLTK RegexpParser
    """
    grammar = r"NP: {<DT>?<JJ.*>*<NN.*>+}"
    chunk_parser = nltk.RegexpParser(grammar)
    
    total_nps = 0
    total_np_length = 0
    total_modifiers = 0
    
    for sent in doc["processed_sentences"]:
        try:
            tree = chunk_parser.parse(sent)
            for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
                total_nps += 1
                words = subtree.leaves()
                total_np_length += len(words)
                total_modifiers += sum(1 for w, t in words if t.startswith('JJ'))
        except Exception:
            pass
            
    avg_np_length = total_np_length / total_nps if total_nps > 0 else 0
    
    return {
        "total_nps": total_nps,
        "avg_np_length": round(avg_np_length, 2),
        "total_modifiers": total_modifiers
    }
