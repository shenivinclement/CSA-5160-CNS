import os
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES
from Crypto.Util import Counter

def encrypt_block_parallel(block_data, key, nonce, block_index):
    ctr = Counter.new(64, prefix=nonce, initial_value=block_index)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(block_data)

def process_parallel_ctr(data, key, nonce):
    block_size = AES.block_size
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(encrypt_block_parallel, block, key, nonce, idx)
            for idx, block in enumerate(blocks)
        ]
        results = [f.result() for f in futures]
        
    return b"".join(results)

def main():
    print("--- AES CTR Mode Parallel Program ---")
    
    plaintext = input("Enter a message to encrypt: ")
    plaintext_bytes = plaintext.encode('utf-8')
    
    key = os.urandom(16)
    nonce = os.urandom(8)
    
    print("\n--- Parameters ---")
    print(f"Key (Hex):   {key.hex().upper()}")
    print(f"Nonce (Hex): {nonce.hex().upper()}")
    
    ciphertext = process_parallel_ctr(plaintext_bytes, key, nonce)
    print(f"\n[+] Parallel Encrypted Ciphertext (Hex): {ciphertext.hex().upper()}")
    
    decrypted_bytes = process_parallel_ctr(ciphertext, key, nonce)
    recovered_plaintext = decrypted_bytes.decode('utf-8')
    print(f"[+] Parallel Decrypted Plaintext:        {recovered_plaintext}")
    
    if plaintext == recovered_plaintext:
        print("\n[Verification] Success! Parallel recovery verified.")

if __name__ == "__main__":
    main()