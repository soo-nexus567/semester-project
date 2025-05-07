from rabin_karp import rabin_karp
from KMP import kmp_search
from naive import naive_search
import re
from collections import Counter

def preprocess_text(text):
    """
    Preprocess text for better matching:
    - Convert to lowercase
    - Remove special characters
    - Normalize whitespace
    
    Args:
        text (str): Text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep spaces and punctuation that affects meaning
    text = re.sub(r'[^\w\s.,;:?!-]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def break_into_phrases(text, phrase_length=5):
    """
    Break text into n-word phrases.
    
    Args:
        text (str): Text to break into phrases
        phrase_length (int): Number of words in each phrase
        
    Returns:
        list: List of phrases
    """
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Split into words
    words = processed_text.split()
    
    # Generate phrases
    phrases = []
    for i in range(len(words) - phrase_length + 1):
        phrase = " ".join(words[i:i+phrase_length])
        phrases.append(phrase)
    
    return phrases

def find_matches(doc1, doc2, phrase_length=5):
    """
    Find matching phrases between two documents using multiple algorithms.
    
    Args:
        doc1 (str): First document
        doc2 (str): Second document
        phrase_length (int): Number of words in each phrase
        
    Returns:
        dict: Dictionary containing match results and similarity score
    """
    # Handle empty documents
    if not doc1 or not doc2:
        return {
            "Rabin-Karp": [],
            "KMP": [],
            "Naive": [],
            "similarity_score": 0,
            "similarity_percentage": 0,
            "total_phrases": 0,
            "unique_matches": []
        }
    
    # Break documents into phrases
    doc1_phrases = break_into_phrases(doc1, phrase_length)
    doc2_phrases = break_into_phrases(doc2, phrase_length)
    
    # Get unique phrases from both documents for more efficient comparison
    unique_doc1_phrases = list(set(doc1_phrases))
    
    # Lists to store (phrase, [positions]) tuples for each algorithm
    matches_rabin = [] 
    matches_kmp = []
    matches_naive = []
    
    # Keep track of all unique phrases that were matched
    all_matched_phrases = set()
    
    # Process unique phrases to avoid redundant searches
    for phrase in unique_doc1_phrases:
        # Only process phrases of sufficient length (avoid matching common single words)
        if len(phrase) > 10:  # Minimum character length threshold
            # Find positions using all algorithms
            doc2_preprocessed = preprocess_text(doc2)
            
            rabin_positions = rabin_karp(doc2_preprocessed, phrase)
            kmp_positions = kmp_search(doc2_preprocessed, phrase)
            naive_positions = naive_search(doc2_preprocessed, phrase)
            
            # Append (phrase, positions) tuple if positions were found
            if rabin_positions:
                matches_rabin.append((phrase, rabin_positions))
                all_matched_phrases.add(phrase)
                
            if kmp_positions:
                matches_kmp.append((phrase, kmp_positions))
                all_matched_phrases.add(phrase)
                
            if naive_positions:
                matches_naive.append((phrase, naive_positions))
                all_matched_phrases.add(phrase)
    
    # Calculate similarity score
    similarity_score = calculate_similarity_score(doc1_phrases, doc2_phrases, all_matched_phrases)
    
    # Return a dictionary containing the lists of tuples and the similarity score
    return {
        "Rabin-Karp": matches_rabin,
        "KMP": matches_kmp,
        "Naive": matches_naive,
        "similarity_score": similarity_score,
        "similarity_percentage": similarity_score * 100,
        "total_phrases": len(doc1_phrases),
        "unique_matches": list(all_matched_phrases)
    }

def calculate_similarity_score(doc1_phrases, doc2_phrases, matched_phrases):
    """
    Calculate a similarity score between two documents based on phrase matches.
    
    Args:
        doc1_phrases (list): Phrases from document 1
        doc2_phrases (list): Phrases from document 2
        matched_phrases (set): Set of matched phrases
        
    Returns:
        float: Similarity score between 0 and 1
    """
    # Count occurrences of each phrase in doc1
    doc1_phrase_counts = Counter(doc1_phrases)
    
    # Total number of phrases in doc1
    total_phrases = len(doc1_phrases)
    
    if total_phrases == 0:
        return 0
    
    # Number of matched phrases (counting duplicates)
    matched_count = sum(doc1_phrase_counts[phrase] for phrase in matched_phrases)
    
    # Calculate similarity as the proportion of matched phrases
    similarity = matched_count / total_phrases
    
    return similarity

# Testing code
if __name__ == "__main__":
    # Test documents
    doc1 = """
    This is a test document for plagiarism detection. 
    It contains some phrases that will be matched in the second document.
    The algorithms should identify these matching segments efficiently.
    """
    
    doc2 = """
    This is another document with some duplicated content.
    It contains some phrases that will be matched from the first document.
    We want to see how well our algorithms identify these matching segments efficiently.
    """
    
    # Find matches
    matches = find_matches(doc1, doc2)
    
    # Print results
    print(f"Similarity score: {matches['similarity_score']:.2f} ({matches['similarity_percentage']:.2f}%)")
    print(f"Total phrases analyzed: {matches['total_phrases']}")
    print(f"Unique matching phrases: {len(matches['unique_matches'])}")
    
    # Print some matched phrases
    print("\nSample matched phrases:")
    for phrase in matches['unique_matches'][:5]:
        print(f"- {phrase}")

