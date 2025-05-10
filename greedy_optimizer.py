import os
from person2 import preprocess_text

def prioritize_document_pairs(directory, file_extension='.txt'):
    """
    Greedy approach to prioritize document pairs for plagiarism detection.
    
    Args:
        directory (str): Directory containing documents
        file_extension (str): File extension to filter documents
        
    Returns:
        list: Prioritized list of document pairs with scores
    """
    # Get all text files in directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f)) and f.endswith(file_extension)]
    
    if len(files) < 2:
        return []
    
    # Helper function to get document features
    def get_features(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            processed = preprocess_text(content)
            words = processed.split()
            word_count = len(words)
            
            if word_count == 0:
                return {"word_count": 0, "unique_ratio": 0, "avg_length": 0}
                
            unique_ratio = len(set(words)) / word_count
            avg_length = sum(len(word) for word in words) / word_count
            
            return {
                "word_count": word_count,
                "unique_ratio": unique_ratio,
                "avg_length": avg_length
            }
        except Exception:
            return None
    
    # Choose starting document (highest word count)
    start_doc = None
    max_words = -1
    for file in files:
        features = get_features(file)
        if features and features["word_count"] > max_words:
            max_words = features["word_count"]
            start_doc = file
    
    # Calculate similarity score between documents
    def calc_similarity(doc1, doc2):
        f1 = get_features(doc1)
        f2 = get_features(doc2)
        
        if not f1 or not f2:
            return 0
            
        # Simple similarity metrics
        count_ratio = min(f1["word_count"], f2["word_count"]) / max(f1["word_count"], f2["word_count"]) if max(f1["word_count"], f2["word_count"]) > 0 else 0
        vocab_sim = 1 - abs(f1["unique_ratio"] - f2["unique_ratio"])
        length_sim = 1 - abs(f1["avg_length"] - f2["avg_length"]) / max(f1["avg_length"], f2["avg_length"]) if max(f1["avg_length"], f2["avg_length"]) > 0 else 0
        
        # Combined score
        return 0.3 * count_ratio + 0.5 * vocab_sim + 0.2 * length_sim
    
    # Greedy selection algorithm
    pairs = []
    current = start_doc
    remaining = [f for f in files if f != current]
    
    while remaining:
        # Find next best document to compare
        best_doc = None
        best_score = -1
        
        for doc in remaining:
            score = calc_similarity(current, doc)
            if score > best_score:
                best_score = score
                best_doc = doc
        
        pairs.append((current, best_doc, best_score))
        remaining.remove(best_doc)
        current = best_doc
    
    # Return pairs sorted by relevance
    return sorted(pairs, key=lambda x: x[2], reverse=True)

if __name__ == "__main__":
    # Example usage
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prioritized_pairs = prioritize_document_pairs(current_dir)
    
    print("Prioritized document pairs for plagiarism detection:")
    for i, (doc1, doc2, score) in enumerate(prioritized_pairs[:10], 1):
        print(f"{i}. {os.path.basename(doc1)} <-> {os.path.basename(doc2)}: {score:.4f}")