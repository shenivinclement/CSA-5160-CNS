import os
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

def encrypt_3des_cbc(plaintext, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded_text = pad(plaintext.encode('utf-8'), DES3.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext

def decrypt_3des_cbc(ciphertext, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_padded, DES3.block_size)
    return plaintext.decode('utf-8')

def main():
    print("--- Triple DES (3DES) CBC Mode Program ---")
    
    message = input("Enter the secret message to transmit: ")
    
    key = DES3.adjust_key_parity(os.urandom(24))
    iv = os.urandom(8)
    
    print("\n--- Secure Channel Simulation ---")
    print(f"[Sender] Original Message:  {message}")
    print(f"[Sender] Generated Key (Hex): {key.hex().upper()}")
    print(f"[Sender] Generated IV (Hex):  {iv.hex().upper()}")
    
    ciphertext = encrypt_3des_cbc(message, key, iv)
    print(f"\n--- Transmission over insecure network ---")
    print(f"[Wire] Ciphertext (Hex):    {ciphertext.hex().upper()}")
    
    try:
        recovered_message = decrypt_3des_cbc(ciphertext, key, iv)
        print(f"\n--- Receiver Endpoint ---")
        print(f"[Receiver] Decrypted Text: {recovered_message}")
        
        if recovered_message == message:
            print("\n[Success] Message securely transmitted and verified!")
    except Exception as e:
        print(f"\n[Error] Decryption failed: {e}")

if __name__ == "__main__":
    main()