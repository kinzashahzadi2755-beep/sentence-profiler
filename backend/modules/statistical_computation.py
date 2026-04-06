from .sentence_length import analyze_length
from .grammatical_complexity import analyze_grammar
from .np_analysis import analyze_nps
from .linguistic_features import analyze_features

def compute_statistics(text_data):
    """
    Framework Steps 6 & 7: Statistical Processing & Decision Framework
    """
    doc = text_data["text_doc"]
    sentences = text_data["sentences"]
    
    length_stats = analyze_length(doc, sentences)
    grammar_stats = analyze_grammar(sentences)
    np_stats = analyze_nps(doc)
    feature_stats = analyze_features(doc)
    
    # Framework Step 7: Decision Rules
    avg_len = length_stats["avg_length"]
    clauses = grammar_stats["total_clauses"]
    sub_clauses = grammar_stats["subordinate_clauses"]
    
    is_short = avg_len <= 12
    is_long = avg_len >= 20
    is_simple = sub_clauses == 0 and clauses <= len(sentences)
    is_complex_struct = sub_clauses >= len(sentences) * 0.5 or clauses > len(sentences) * 1.5
    
    # Rules translation
    if is_short and is_simple:
        complexity = "Low Complexity"
    elif is_long and is_complex_struct:
        complexity = "High Complexity"
    else:
        complexity = "Moderate Complexity"
        
    return {
        "length_stats": length_stats,
        "grammar_stats": grammar_stats,
        "np_stats": np_stats,
        "feature_stats": feature_stats,
        "overall_complexity": complexity
    }
