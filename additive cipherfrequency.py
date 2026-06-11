import collections
import re

ENGLISH_FREQS = {
    'A': 0.0817, 'B': 0.0150, 'C': 0.0278, 'D': 0.0425, 'E': 0.1270, 'F': 0.0223,
    'G': 0.0202, 'H': 0.0609, 'I': 0.0697, 'J': 0.0015, 'K': 0.0077, 'L': 0.0403,
    'M': 0.0241, 'N': 0.0675, 'O': 0.0751, 'P': 0.0193, 'Q': 0.0010, 'R': 0.0599,
    'S': 0.0633, 'T': 0.0906, 'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015,
    'Y': 0.0197, 'Z': 0.0007
}

def decrypt_with_shift(ciphertext, shift):
    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            plaintext.append(decrypted_char)
        else:
            plaintext.append(char)
    return "".join(plaintext)

def calculate_chi_squared(text):
    cleaned = [char.upper() for char in text if char.isalpha()]
    length = len(cleaned)
    if length == 0:
        return float('inf')
        
    counts = collections.Counter(cleaned)
    chi_squared = 0.0
    
    for char, expected_prob in ENGLISH_FREQS.items():
        observed = counts[char]
        expected = length * expected_prob
        chi_squared += ((observed - expected) ** 2) / expected
        
    return chi_squared

def frequency_attack(ciphertext, top_n=10):
    candidates = []
    
    for shift in range(26):
        plaintext = decrypt_with_shift(ciphertext, shift)
        score = calculate_chi_squared(plaintext)
        candidates.append((score, shift, plaintext))
        
    candidates.sort(key=lambda x: x[0])
    return candidates[:top_n]

if __name__ == "__main__":
    encrypted_message = (
        "Ymj tscd bfd yt it lwjfy btwp nx yt qtaj bmfy dtz it. "
        "Xyjan Otgx bfx f anXntsfpd bmt xmruji ymj rtiwse jwfi tk yjxmscgtdp."
    )
    
    print("--- Automated Frequency Attack on Additive Cipher ---")
    print(f"Ciphertext:\n{encrypted_message}\n")
    
    try:
        limit = int(input("Enter the number of top plaintexts to display (1-26): "))
        if not 1 <= limit <= 26:
            raise ValueError
    except ValueError:
        limit = 10
        print("Invalid input. Defaulting to top 10.")

    top_candidates = frequency_attack(encrypted_message, top_n=limit)
    
    print(f"\n--- Top {len(top_candidates)} Most Likely Plaintexts ---")
    for index, (score, shift, plaintext) in enumerate(top_candidates, 1):
        print(f"Rank {index} [Shift Key: {shift:2d} | Chi-Sq Score: {score:7.2f}]:")
        print(f"  {plaintext}\n")