import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def demonstrate_ecb(plaintext, key):
    cipher_enc = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plaintext, AES.block_size)
    ciphertext = bytearray(cipher_enc.encrypt(padded_text))
    
    ciphertext[5] ^= 0xFF
    
    cipher_dec = AES.new(key, AES.MODE_ECB)
    try:
        decrypted_padded = cipher_dec.decrypt(bytes(ciphertext))
        decrypted = unpad(decrypted_padded, AES.block_size)
    except Exception:
        decrypted = cipher_dec.decrypt(bytes(ciphertext))
        
    return decrypted

def demonstrate_cbc(plaintext, key, iv):
    cipher_enc = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plaintext, AES.block_size)
    ciphertext = bytearray(cipher_enc.encrypt(padded_text))
    
    ciphertext[5] ^= 0xFF
    
    cipher_dec = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_padded = cipher_dec.decrypt(bytes(ciphertext))
        decrypted = unpad(decrypted_padded, AES.block_size)
    except Exception:
        decrypted = cipher_dec.decrypt(bytes(ciphertext))
        
    return decrypted

def display_blocks(data_bytes):
    blocks = []
    for i in range(0, len(data_bytes), AES.block_size):
        block = data_bytes[i:i+AES.block_size]
        blocks.append(block.decode('utf-8', errors='replace'))
    return blocks

def main():
    print("--- ECB vs CBC Error Propagation Analysis ---")
    
    key = os.urandom(16)
    iv = os.urandom(16)
    
    block1 = "BLOCK_NUMBER_1__"
    block2 = "BLOCK_NUMBER_2__"
    block3 = "BLOCK_NUMBER_3__"
    sample_input = (block1 + block2 + block3).encode('utf-8')
    
    print(f"\nOriginal Plaintext Blocks (16 bytes each):")
    print(f"Block 1: {block1}")
    print(f"Block 2: {block2}")
    print(f"Block 3: {block3}")
    print("-" * 50)
    
    ecb_result = demonstrate_ecb(sample_input, key)
    ecb_blocks = display_blocks(ecb_result)
    
    print("\n[+] ECB Mode Decryption after Corrupting 1 Byte in Block 1:")
    print(f"Decrypted Block 1: {ecb_blocks[0]} <-- Completely Corrupted")
    print(f"Decrypted Block 2: {ecb_blocks[1]} <-- Unaffected")
    print(f"Decrypted Block 3: {ecb_blocks[2]} <-- Unaffected")
    
    cbc_result = demonstrate_cbc(sample_input, key, iv)
    cbc_blocks = display_blocks(cbc_result)
    
    print("\n[+] CBC Mode Decryption after Corrupting 1 Byte in Block 1:")
    print(f"Decrypted Block 1: {cbc_blocks[0]} <-- Completely Corrupted")
    print(f"Decrypted Block 2: {cbc_blocks[1]} <-- 1 Byte Corrupted (Same index as error)")
    print(f"Decrypted Block 3: {cbc_blocks[2]} <-- Unaffected")

if __name__ == "__main__":
    main()