import collections
import random
import re
import math

ENGLISH_FREQ = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

# Top English trigrams and their relative log-probabilities for scoring
TRIGRAM_LOG_PROBS = {
    'THE': -2.3, 'AND': -2.8, 'ING': -3.1, 'ENT': -3.2, 'ION': -3.3,
    'HER': -3.4, 'FOR': -3.5, 'THA': -3.5, 'NTH': -3.6, 'WAS': -3.7,
    'ETH': -3.7, 'TIO': -3.8, 'HAT': -3.9, 'ERS': -3.9, 'HIS': -4.0,
    'RES': -4.0, 'ILL': -4.1, 'ARE': -4.1, 'ATT': -4.2, 'NOT': -4.2
}

def clean_text(text):
    return re.sub(r'[^A-Z]', '', text.upper())

def get_cipher_frequency(ciphertext):
    cleaned = clean_text(ciphertext)
    counts = collections.Counter(cleaned)
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if char not in counts:
            counts[char] = 0
    return [item[0] for item in counts.most_common()]

def score_text(text):
    cleaned = clean_text(text)
    score = 0.0
    # Floor value for trigrams not present in our dictionary to penalize gibberish
    floor = -15.0 
    
    for i in range(len(cleaned) - 2):
        trigram = cleaned[i:i+3]
        if trigram in TRIGRAM_LOG_PROBS:
            score += TRIGRAM_LOG_PROBS[trigram]
        else:
            score += floor
    return score

def decrypt_with_cipher_key(ciphertext, cipher_key):
    # cipher_key maps: Ciphertext Letter -> Plaintext Letter
    decrypted = []
    for char in ciphertext:
        if char.isupper():
            decrypted.append(cipher_key.get(char, char))
        elif char.islower():
            decrypted.append(cipher_key.get(char.upper(), char.upper()).lower())
        else:
            decrypted.append(char)
    return "".join(decrypted)

def generate_initial_key(ciphertext):
    cipher_freqs = get_cipher_frequency(ciphertext)
    initial_key = {}
    for i, cipher_char in enumerate(cipher_freqs):
        initial_key[cipher_char] = ENGLISH_FREQ[i]
    return initial_key

def simulated_annealing_search(ciphertext, iterations=2000):
    # Starts with a baseline frequency mapping and optimizes it via hill-climbing
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    current_key = generate_initial_key(ciphertext)
    current_text = decrypt_with_cipher_key(ciphertext, current_key)
    current_score = score_text(current_text)
    
    best_key = current_key.copy()
    best_score = current_score
    
    T = 10.0
    cooling_rate = 0.995
    
    for _ in range(iterations):
        T *= cooling_rate
        
        # Pick two random characters to swap in the mapping decryption output
        c1, c2 = random.sample(alphabet, 2)
        
        neighbor_key = current_key.copy()
        neighbor_key[c1], neighbor_key[c2] = neighbor_key[c2], neighbor_key[c1]
        
        neighbor_text = decrypt_with_cipher_key(ciphertext, neighbor_key)
        neighbor_score = score_text(neighbor_text)
        
        # Acceptance probability
        if neighbor_score > current_score:
            current_key = neighbor_key
            current_score = neighbor_score
        else:
            delta = neighbor_score - current_score
            if T > 0 and random.random() < math.exp(delta / T):
                current_key = neighbor_key
                current_score = neighbor_score
                
        if current_score > best_score:
            best_score = current_score
            best_key = current_key.copy()
            
    return best_score, best_key

def attack_monoalphabetic(ciphertext, top_n=10):
    candidates = []
    seen_texts = set()
    
    # Run multiple structural optimization tracks to bypass local maximums
    runs = top_n * 3 
    for _ in range(runs):
        score, key_map = simulated_annealing_search(ciphertext)
        decrypted_text = decrypt_with_cipher_key(ciphertext, key_map)
        
        if decrypted_text not in seen_texts:
            seen_texts.add(decrypted_text)
            candidates.append((score, decrypted_text))
            
    # Sort candidates by log-probability likelihood (closest to 0 is best)
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[:top_n]

if __name__ == "__main__":
    # Sample ciphertext generated via a random monoalphabetic substitution cipher
    sample_ciphertext = (
        "GPE TPEVJECE TVPTECZEDZVE ZY TPEVJECE KPRK PECECHVEGZCECP "
        "YCHVBEVGFCP GCBEZVEGZCECP GCBEVGFCP KP GPE KPEVJECE GPEVEGCVE "
        "KPE VY KPE ACCH KPRK TPEVJECE PECECHVEGZCECP PECCMKP VAKV "
        "GPE KPEVJECE KPRK VY KPVEKPEVE. GPE KPEVJECE VY GPE KPEVJECE "
        "ZPEVKEK KPE KPEVJECE VY GPE KPEVJECE."
    )
    
    print("--- Fully Automated Monoalphabetic Frequency Attack ---")
    print(f"Ciphertext Target:\n{sample_ciphertext}\n")
    
    try:
        user_input = input("Enter the number of top plaintexts to return (Default 10): ")
        requested_limit = int(user_input) if user_input.strip() else 10
    except ValueError:
        requested_limit = 10
        print("Invalid entry. Defaulting to top 10 positions.")

    print("\nAnalyzing cryptographic structures... please wait...")
    top_results = attack_monoalphabetic(sample_ciphertext, top_n=requested_limit)
    
    print(f"\n--- Top {len(top_results)} Most Likely Decryptions ---")
    for rank, (score, plaintext) in enumerate(top_results, 1):
        print(f"Rank {rank} [Statistical Probability Score: {score:.2f}]:")
        print(f"{plaintext}\n")