import secrets

def generate_otp_key(length):
    return "".join(chr(secrets.randbelow(26) + 65) for _ in range(length))

def otp_cipher(text, key, mode='encrypt'):
    result = []
    text = text.upper()
    key = key.upper()
    
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            p_num = ord(char) - 65
            k_num = ord(key[i]) - 65
            
            if mode == 'encrypt':
                c_num = (p_num + k_num) % 26
            else:
                c_num = (p_num - k_num + 26) % 26
                
            result.append(chr(c_num + 65))
        else:
            result.append(char)
            
    return "".join(result)

def main():
    print("--- One-Time Pad (Vigenere Variant) ---")
    
    plaintext = input("Enter the plaintext message: ")
    
    clean_text = "".join([c for c in plaintext if c.isalpha()])
    key = generate_otp_key(len(clean_text))
    
    full_key_stream = []
    key_idx = 0
    for char in plaintext:
        if char.isalpha():
            full_key_stream.append(key[key_idx])
            key_idx += 1
        else:
            full_key_stream.append(char)
    final_key = "".join(full_key_stream)
    
    print(f"\n[+] Generated Random Key:  {final_key}")
    
    ciphertext = otp_cipher(plaintext, final_key, mode='encrypt')
    print(f"[+] Encrypted Ciphertext: {ciphertext}")
    
    decrypted_text = otp_cipher(ciphertext, final_key, mode='decrypt')
    print(f"[+] Recovered Plaintext:  {decrypted_text}")

if __name__ == "__main__":
    main()