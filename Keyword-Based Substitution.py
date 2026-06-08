def generate_cipher_alphabet(keyword):
    keyword = keyword.upper()
    cipher_alphabet = []
    seen = set()
    
    for char in keyword:
        if char.isalpha() and char not in seen:
            seen.add(char)
            cipher_alphabet.append(char)
            
    for i in range(26):
        char = chr(65 + i)
        if char not in seen:
            seen.add(char)
            cipher_alphabet.append(char)
            
    return "".join(cipher_alphabet)

def substitution_cipher(text, cipher_alphabet, mode='encrypt'):
    standard_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    if mode == 'encrypt':
        mapping = {src: dst for src, dst in zip(standard_alphabet, cipher_alphabet)}
    else:
        mapping = {src: dst for src, dst in zip(cipher_alphabet, standard_alphabet)}
        
    result = []
    for char in text:
        if char.isalpha():
            upper_char = char.upper()
            mapped_char = mapping[upper_char]
            if char.islower():
                result.append(mapped_char.lower())
            else:
                result.append(mapped_char)
        else:
            result.append(char)
            
    return "".join(result)

def main():
    print("--- Keyword-Based Substitution Cipher ---")
    
    keyword = input("Enter the keyword: ")
    plaintext = input("Enter the sample message: ")
    
    if not keyword.isalpha():
        print("Error: The keyword must contain alphabetic characters only.")
        return
        
    cipher_alphabet = generate_cipher_alphabet(keyword)
    
    print("\n--- Alphabet Generation ---")
    print(f"Standard Alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    print(f"Cipher Alphabet:   {cipher_alphabet}")
    print("-" * 28)
    
    ciphertext = substitution_cipher(plaintext, cipher_alphabet, mode='encrypt')
    print(f"\n[+] Encrypted Ciphertext: {ciphertext}")
    
    decrypted_text = substitution_cipher(ciphertext, cipher_alphabet, mode='decrypt')
    print(f"[+] Decrypted Plaintext:  {decrypted_text}")

if __name__ == "__main__":
    main()
