#KMP algo

#Step 1: Pre-processing to compute LPS Array
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m #Initializing LPS array with Zeros
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

#Step 2: KMP Pattern Searching
def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    positions = []

    i = j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
            if j == m:
                positions.append(i - j)
                j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    return positions

#Example Input:
text = "Hello World! this is Computer Science!"
pattern = "Computer"

#Output
print("KMP match found at:", kmp_search(text, pattern))