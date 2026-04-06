def analyze_grammar(sentences):
    """
    Framework Step 3: Grammatical Structure Analysis
    """
    total_clauses = 0
    subordinate_clauses = 0
    for sent in sentences:
        clauses = [token for token in sent if token.dep_ in ('csubj', 'csubjpass', 'ccomp', 'xcomp', 'advcl', 'relcl') or token.pos_ == 'VERB']
        total_clauses += len(clauses)
        subordinate_clauses += len([token for token in sent if token.dep_ in ('advcl', 'relcl', 'ccomp')])
    return {
        "total_clauses": total_clauses,
        "subordinate_clauses": subordinate_clauses
    }
