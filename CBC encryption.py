import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_cbc(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

def decrypt_cbc(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext_bytes = unpad(decrypted_padded, AES.block_size)
    return plaintext_bytes.decode('utf-8')

def main():
    print("--- AES CBC Mode Encryption & Decryption ---")
    
    plaintext = input("Enter the plaintext message: ")
    
    key = os.urandom(16)
    iv = os.urandom(16)
    
    print("\n--- Encryption Parameters ---")
    print(f"Key (Hex): {key.hex().upper()}")
    print(f"IV (Hex):  {iv.hex().upper()}")
    
    ciphertext = encrypt_cbc(plaintext, key, iv)
    print(f"\n[+] Encrypted Ciphertext (Hex): {ciphertext.hex().upper()}")
    
    recovered_plaintext = decrypt_cbc(ciphertext, key, iv)
    print(f"[+] Recovered Plaintext:        {recovered_plaintext}")
    
    if plaintext == recovered_plaintext:
        print("\n[Verification] Success! Plaintext matches the recovered text.")
    else:
        print("\n[Verification] Failure! Decrypted text does not match.")

if __name__ == "__main__":
    main()