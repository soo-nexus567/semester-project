#Rabin-Karp String Matching Algorithm

def rabin_karp(text, pattern, q=101):
    d = 256 # Number of characters in the input alphabet(252)
    m = len(pattern)
    n = len(text)
    h = pow(d, m-1) % q #This helps in removing the leading denominator
    p_hash = 0
    t_hash = 0
    positions = [] # storing the indices of the pattern found

    #Step 1: Calculate initial hash of Pattern & First window of has
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
        
    #Step 2: Slide the pattern over the text one character at a time
    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                positions.append(i)
        
        if i < n - m:
            # Remove leading digit, add trailing digit
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            
            if t_hash < 0:
                t_hash += q
    return positions
        
        
#Example input:  
text = "Hello World! This is Computer Science"
pattern = "Computer"

#Output
print("Rabin-Karp String match found at:", rabin_karp(text, pattern))