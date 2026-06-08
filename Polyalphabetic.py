def generate_key(text, key):
    key = list(key.upper())
    if len(text) == len(key):
        return "".join(key)
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt_vigenere(plaintext, key):
    ciphertext = []
    plaintext = plaintext.upper()
    key = generate_key(plaintext, key)
    
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            shift = (ord(char) + ord(key[key_index])) % 26
            ciphertext.append(chr(shift + 65))
            key_index += 1
        else:
            ciphertext.append(char)
            
    return "".join(ciphertext)

def decrypt_vigenere(ciphertext, key):
    decrypted_text = []
    ciphertext = ciphertext.upper()
    key = generate_key(ciphertext, key)
    
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = (ord(char) - ord(key[key_index]) + 26) % 26
            decrypted_text.append(chr(shift + 65))
            key_index += 1
        else:
            decrypted_text.append(char)
            
    return "".join(decrypted_text)

def demonstrate_variation():
    repeated_plaintext = "AAAAA AAAAA"
    sample_key = "KEY"
    
    cipher_output = encrypt_vigenere(repeated_plaintext, sample_key)
    generated_key_stream = generate_key(repeated_plaintext.replace(" ", ""), sample_key)
    
    print("--- Variation Demonstration ---")
    print(f"Plaintext (Repeated 'A's):  {repeated_plaintext}")
    print(f"Repeating Key Stream:      {' '.join([generated_key_stream[i:i+5] for i in range(0, len(generated_key_stream), 5)])}")
    print(f"Resulting Ciphertext:      {cipher_output[:5]} {cipher_output[6:]}")
    print("-" * 32)

def main():
    print("--- Polyalphabetic Cipher Program ---")
    
    plaintext = input("Enter the plaintext: ")
    key = input("Enter the repeating key: ")
    
    if not key.isalpha():
        print("Error: The key must only contain alphabetic characters.")
        return

    ciphertext = encrypt_vigenere(plaintext, key)
    recovered_text = decrypt_vigenere(ciphertext, key)
    
    print(f"\n[+] Original Plaintext:   {plaintext}")
    print(f"[+] Encrypted Ciphertext: {ciphertext}")
    print(f"[+] Recovered Plaintext:  {recovered_text}\n")
    
    demonstrate_variation()

if __name__ == "__main__":
    main()