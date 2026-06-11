import secrets

def encrypt_vigenere_otp(plaintext, key_stream):
    ciphertext = []
    for i, char in enumerate(plaintext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = key_stream[i]
            cipher_char = chr((ord(char) - base + shift) % 26 + base)
            ciphertext.append(cipher_char)
        else:
            ciphertext.append(char)
    return "".join(ciphertext)

def decrypt_vigenere_otp(ciphertext, key_stream):
    plaintext = []
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = key_stream[i]
            plain_char = chr((ord(char) - base - shift) % 26 + base)
            plaintext.append(plain_char)
        else:
            plaintext.append(char)
    return "".join(plaintext)

if __name__ == "__main__":
    message = "ATTACKATDAWN"
    
    # Generate a cryptographically secure random key stream of matching length
    # Values range from 0 to 25 inclusive
    otp_key_stream = [secrets.randbelow(26) for _ in range(len(message))]
    
    cipher = encrypt_vigenere_otp(message, otp_key_stream)
    decrypted = decrypt_vigenere_otp(cipher, otp_key_stream)
    
    print(f"Plaintext:  {message}")
    print(f"Key Stream: {otp_key_stream}")
    print(f"Ciphertext: {cipher}")
    print(f"Decrypted:  {decrypted}")