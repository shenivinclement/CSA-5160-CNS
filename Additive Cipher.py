def frequency_attack(ciphertext):
    ciphertext = ciphertext.upper()
    
    english_frequencies = {
        'A': 0.0817, 'B': 0.0150, 'C': 0.0278, 'D': 0.0425, 'E': 0.1270, 
        'F': 0.0223, 'G': 0.0202, 'H': 0.0609, 'I': 0.0697, 'J': 0.0015, 
        'K': 0.0077, 'L': 0.0403, 'M': 0.0241, 'N': 0.0675, 'O': 0.0751, 
        'P': 0.0193, 'Q': 0.0010, 'R': 0.0599, 'S': 0.0633, 'T': 0.0906, 
        'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015, 'Y': 0.0197, 
        'Z': 0.0007
    }
    
    alpha_text = [char for char in ciphertext if char.isalpha()]
    total_chars = len(alpha_text)
    
    if total_chars == 0:
        return 0, ""
        
    best_key = 0
    lowest_score = float('inf')
    
    for shift in range(26):
        score = 0.0
        observed_counts = {chr(65 + i): 0 for i in range(26)}
        
        for char in alpha_text:
            decrypted_char = chr((ord(char) - 65 - shift) % 26 + 65)
            observed_counts[decrypted_char] += 1
            
        for char in english_frequencies:
            observed_freq = observed_counts[char] / total_chars
            score += abs(observed_freq - english_frequencies[char])
            
        if score < lowest_score:
            lowest_score = score
            best_key = shift
            
    recovered_plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            recovered_plaintext += chr((ord(char) - 65 - best_key) % 26 + 65)
        else:
            recovered_plaintext += char
            
    return best_key, recovered_plaintext

def main():
    print("--- Frequency Attack on Additive Cipher ---")
    ciphertext = input("Enter the ciphertext: ")
    
    key, plaintext = frequency_attack(ciphertext)
    
    print("\n--- Attack Results ---")
    print(f"Most Likely Key (Shift): {key}")
    print(f"Recovered Plaintext:     {plaintext}")

if __name__ == "__main__":
    main()
