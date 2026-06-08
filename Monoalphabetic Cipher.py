def monoalphabetic_frequency_attack(ciphertext):
    english_frequency_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    
    clean_ciphertext = ciphertext.upper()
    letter_counts = {}
    
    for char in clean_ciphertext:
        if char.isalpha():
            letter_counts[char] = letter_counts.get(char, 0) + 1
            
    sorted_cipher_letters = sorted(letter_counts, key=letter_counts.get, reverse=True)
    
    unused_alphabet = [chr(i) for i in range(65, 91) if chr(i) not in sorted_cipher_letters]
    full_cipher_order = sorted_cipher_letters + unused_alphabet
    
    decryption_mapping = {}
    for i in range(26):
        decryption_mapping[full_cipher_order[i]] = english_frequency_order[i]
        
    probable_plaintext = []
    for char in ciphertext:
        if char.isalpha():
            upper_char = char.upper()
            mapped_char = decryption_mapping[upper_char]
            if char.islower():
                probable_plaintext.append(mapped_char.lower())
            else:
                probable_plaintext.append(mapped_char)
        else:
            probable_plaintext.append(char)
            
    return "".join(probable_plaintext), decryption_mapping

def main():
    print("--- Monoalphabetic Cipher Frequency Attack ---")
    ciphertext = input("Enter the ciphertext: ")
    
    plaintext, mapping = monoalphabetic_frequency_attack(ciphertext)
    
    print("\n--- Generated Substitution Mapping ---")
    for cipher_char, plain_char in sorted(mapping.items()):
        print(f"{cipher_char} -> {plain_char}", end="  ")
        if (ord(cipher_char) - 64) % 6 == 0:
            print()
            
    print("\n\n--- Most Probable Plaintext (Initial Guess) ---")
    print(plaintext)
    print("\nNote: Long text yields higher statistical accuracy.")

if __name__ == "__main__":
    main()
