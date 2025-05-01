from rabin_karp import rabin_karp
from KMP import kmp_search
from naive import naive_search

def break_into_phrases(text, phrase_length=5):
    words = text.split()
    phrases = []
    for i in range(len(words) - phrase_length + 1):
        phrase = " ".join(words[i:i+phrase_length])
        phrases.append(phrase)
    return phrases

def find_matches(doc1, doc2):
    phrases = break_into_phrases(doc1)
    # Lists to store (phrase, [positions]) tuples for each algorithm
    matches_rabin = [] 
    matches_kmp = []
    matches_naive = []

    for phrase in phrases:
        rabin_positions = rabin_karp(doc2, phrase)
        kmp_positions = kmp_search(doc2, phrase)
        naive_positions = naive_search(doc2, phrase)
        
        # Append (phrase, positions) tuple if positions were found
        if rabin_positions:
            matches_rabin.append((phrase, rabin_positions))
        if kmp_positions:
            matches_kmp.append((phrase, kmp_positions))
        if naive_positions:
            matches_naive.append((phrase, naive_positions))

    # Return a dictionary containing the lists of tuples
    return {
        "Rabin-Karp": matches_rabin,
        "KMP": matches_kmp,
        "Naive": matches_naive
    }

def search_phrase_in_document(document, phrase):
    return len(naive_search(document, phrase)) > 0

