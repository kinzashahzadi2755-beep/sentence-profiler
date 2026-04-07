def analyze_grammar(sentences):
    """
    Framework Step 3: Grammatical Structure Analysis
    """
    total_clauses = 0
    subordinate_clauses = 0
    sub_conjs = {'because', 'although', 'though', 'if', 'since', 'unless', 'while', 'whereas', 'whether', 'that'}
    
    for sent in sentences:
        # Each sent is a list of (word, tag)
        verbs = [1 for w, t in sent if t.startswith('VB')]
        total_clauses += len(verbs)
        
        subs = [1 for w, t in sent if t in ('WDT', 'WP', 'WP$', 'WRB') or (t == 'IN' and w.lower() in sub_conjs)]
        subordinate_clauses += len(subs)
        
    # Ensure at least 1 clause per sentence for realistic baselines if we missed verbs
    if total_clauses < len(sentences):
        total_clauses = len(sentences)
        
    return {
        "total_clauses": total_clauses,
        "subordinate_clauses": subordinate_clauses
    }
