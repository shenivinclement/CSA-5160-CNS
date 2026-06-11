import collections
import re

ENGLISH_FREQ = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

TRIGRAM_DATA = {
    'THE': 0.0356, 'AND': 0.0159, 'ING': 0.0114, 'ENT': 0.0110, 'ION': 0.0100,
    'HER': 0.0082, 'FOR': 0.0076, 'THA': 0.0072, 'NTH': 0.0067, 'WAS': 0.0063,
    'ETH': 0.0061, 'TIO': 0.0058, 'FOR': 0.0055, 'VTIS': 0.0053, 'HAT': 0.0051,
    'ERS': 0.0050, 'HIS': 0.0049, 'RES': 0.0048, 'ILL': 0.0047, 'ARE': 0.0046
}

def clean_text(text):
    return re.sub(r'[^A-Z]', '', text.upper())

def get_frequency_map(ciphertext):
    cleaned = clean_text(ciphertext)
    counts = collections.Counter(cleaned)
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if char not in counts:
            counts[char] = 0
    return [item[0] for item in counts.most_common()]

def score_text(text):
    cleaned = clean_text(text)
    score = 0.0
    for i in range(len(cleaned) - 2):
        trigram = cleaned[i:i+3]
        if trigram in TRIGRAM_DATA:
            score += TRIGRAM_DATA[trigram]
    return score

def generate_key_variations(base_mapping):
    variations = [base_mapping.copy()]
    swaps = [
        ('E', 'T'), ('A', 'O'), ('I', 'N'), ('S', 'H'), 
        ('R', 'D'), ('L', 'C'), ('U', 'M'), ('W', 'F')
    ]
    for target1, target2 in swaps:
        new_mapping = base_mapping.copy()
        c1 = [k for k, v in base_mapping.items() if v == target1]
        c2 = [k for k, v in base_mapping.items() if v == target2]
        if c1 and c2:
            new_mapping[c1[0]] = target2
            new_mapping[c2[0]] = target1
            variations.append(new_mapping)
    return variations

def decrypt_with_key(ciphertext, key_map):
    decrypted = []
    for char in ciphertext:
        if char.isupper():
            decrypted.append(key_map.get(char, char))
        elif char.islower():
            decrypted.append(key_map.get(char.upper(), char.upper()).lower())
        else:
            decrypted.append(char)
    return "".join(decrypted)

def frequency_attack(ciphertext, top_n=10):
    cipher_freqs = get_frequency_map(ciphertext)
    
    base_mapping = {}
    for i, cipher_char in enumerate(cipher_freqs):
        if i < len(ENGLISH_FREQ):
            base_mapping[cipher_char] = ENGLISH_FREQ[i]

    candidate_keys = generate_key_variations(base_mapping)
    results = []

    for key_map in candidate_keys:
        plaintext = decrypt_with_key(ciphertext, key_map)
        score = score_text(plaintext)
        results.append((score, plaintext))

    results.sort(key=lambda x: x[0], reverse=True)
    
    unique_results = []
    seen = set()
    for score, pt in results:
        if pt not in seen:
            seen.add(pt)
            unique_results.append((score, pt))
            if len(unique_results) == top_n:
                break
                
    return unique_results

if __name__ == "__main__":
    encrypted_message = (
        "GPE TPEVJECE TVPTECZEDZVE ZY TPEVJECE KPRK PECECHVEGZCECP "
        "YCHVBEVGFCP GCBEZVEGZCECP GCBEVGFCP KP GPE KPEVJECE GPEVEGCVE "
        "KPE VY KPE ACCH KPRK TPEVJECE PECECHVEGZCECP PECCMKP VAKV "
        "GPE KPEVJECE KPRK VY KPVEKPEVE. GPE KPEVJECE VY GPE KPEVJECE "
        "ZPEVKEK KPE KPEVJECE VY GPE KPEVJECE."
    )
    
    print("--- Automated Frequency Analysis Attack ---")
    print(f"Ciphertext:\n{encrypted_message}\n")
    
    try:
        limit = int(input("Enter the number of top plaintexts to display (e.g., 10): "))
    except ValueError:
        limit = 10
        print("Invalid input. Defaulting to top 10.")

    top_candidates = frequency_attack(encrypted_message, top_n=limit)
    
    print(f"\n--- Top {len(top_candidates)} Most Likely Plaintexts ---")
    for index, (score, plaintext) in enumerate(top_candidates, 1):
        print(f"Rank {index} [Trigram Score: {score:.4f}]:")
        print(f"{plaintext}\n")