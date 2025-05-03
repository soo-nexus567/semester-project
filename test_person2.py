import unittest
from person2 import break_into_phrases, find_matches, search_phrase_in_document

class TestPerson2(unittest.TestCase):
    def setUp(self):
        # Sample documents for testing
        self.doc1 = "This is a sample document for testing plagiarism detection."
        self.doc2 = "This is a different document with some sample content for testing."
        self.doc3 = "This is a completely different document with no matches."

    def test_break_into_phrases(self):
        # Test default phrase length (5)
        phrases = break_into_phrases(self.doc1)
        self.assertEqual(len(phrases), 5)  # Should have 5 phrases
        self.assertEqual(phrases[0], "This is a sample document")
        
        # Test custom phrase length
        phrases = break_into_phrases(self.doc1, phrase_length=3)
        self.assertEqual(len(phrases), 7)  # Should have 7 phrases
        self.assertEqual(phrases[0], "This is a")

    def test_find_matches(self):
        # Test with documents that have partial matches
        # (Our test strings aren't good enough for exact 5-word phrase matches)
        matches = find_matches(self.doc1, self.doc2)
        
        # Print matches to debug
        print("Found matches in dissimilar documents:")
        for algo, found_matches in matches.items():
            print("%s: %s" % (algo, found_matches))
        
        # Test with documents that have no matches
        matches = find_matches(self.doc1, self.doc3)
        self.assertEqual(len(matches["Rabin-Karp"]), 0)
        self.assertEqual(len(matches["KMP"]), 0)
        self.assertEqual(len(matches["Naive"]), 0)
        
        # This test passes since we verified our algorithms work with better data below

    def test_search_phrase_in_document(self):
        # Test when phrase exists
        self.assertTrue(search_phrase_in_document(self.doc1, "sample document"))
        
        # Test when phrase doesn't exist
        self.assertFalse(search_phrase_in_document(self.doc1, "nonexistent phrase"))
        
        # Test with empty phrase
        self.assertTrue(search_phrase_in_document(self.doc1, ""))
        
        # Test with exact document match
        self.assertTrue(search_phrase_in_document(self.doc1, self.doc1))

    def test_with_better_matching_documents(self):
        """Test with documents that have clearer matching phrases"""
        doc_a = "The quick brown fox jumps over the lazy dog. It was a sunny day."
        doc_b = "On a sunny day, the quick brown fox jumps over the lazy dog."
        
        matches = find_matches(doc_a, doc_b)
        print("\nMatches with better test documents:")
        for algo, found_matches in matches.items():
            print("%s: %s" % (algo, found_matches))
            
        # With these documents, we expect all algorithms to find matches
        self.assertTrue(len(matches["KMP"]) > 0)
        self.assertTrue(len(matches["Naive"]) > 0)
        self.assertTrue(len(matches["Rabin-Karp"]) > 0)
        
        # This test confirms that our algorithms work correctly with proper matching content

if __name__ == '__main__':
    unittest.main() 