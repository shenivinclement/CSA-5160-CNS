def decrypt_substitution(ciphertext, key_mapping):
    plaintext = []
    
    for char in ciphertext:
        if char.isalpha():
            upper_char = char.upper()
            if upper_char in key_mapping:
                decrypted_char = key_mapping[upper_char]
                if char.islower():
                    plaintext.append(decrypted_char.lower())
                else:
                    plaintext.append(decrypted_char)
            else:
                plaintext.append(char)
        else:
            plaintext.append(char)
            
    return "".join(plaintext)

def main():
    print("--- Simple Substitution Cipher Decryption ---")
    
    ciphertext = input("Enter the ciphertext to decrypt: ")
    
    print("\nEnter your 26-letter substitution key.")
    print("Example: 'XYZABCDEFGHIJKLMNOPQRSTUVW' means A->X, B->Y, C->Z, etc.")
    key_input = input("Key (26 alphabetic characters): ").strip().upper()
    
    if len(key_input) != 26 or not key_input.isalpha() or len(set(key_input)) != 26:
        print("\n[!] Error: Key must contain exactly 26 unique alphabetic characters.")
        return

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    decryption_key_map = {cipher_char: plain_char for plain_char, cipher_char in zip(alphabet, key_input)}
    
    probable_plaintext = decrypt_substitution(ciphertext, decryption_key_map)
    
    print("\n--- Decryption Results ---")
    print(f"Ciphertext:         {ciphertext}")
    print(f"Probable Plaintext: {probable_plaintext}")

if __name__ == "__main__":
    main()