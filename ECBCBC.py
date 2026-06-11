import os
from Cryptodome.Cipher import AES

def pad_iso7816_4(data, block_size=16):
    padding_len = block_size - (len(data) % block_size)
    if padding_len == 0:
        padding_len = block_size
    return data + b'\x80' + b'\x00' * (padding_len - 1)

def unpad_iso7816_4(padded_data):
    idx = len(padded_data) - 1
    while idx >= 0 and padded_data[idx] == 0x00:
        idx -= 1
    if idx >= 0 and padded_data[idx] == 0x80:
        return padded_data[:idx]
    raise ValueError("Invalid padding detected")

class CryptoEngine:
    def __init__(self):
        self.key = os.urandom(16)
        self.iv = os.urandom(16)

    def encrypt_ecb(self, plaintext):
        padded = pad_iso7816_4(plaintext)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(padded)

    def decrypt_ecb(self, ciphertext):
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded = cipher.decrypt(ciphertext)
        return unpad_iso7816_4(padded)

    def encrypt_cbc(self, plaintext):
        padded = pad_iso7816_4(plaintext)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(padded)

    def decrypt_cbc(self, ciphertext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded = cipher.decrypt(ciphertext)
        return unpad_iso7816_4(padded)

    def encrypt_cfb(self, plaintext):
        padded = pad_iso7816_4(plaintext)
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
        return cipher.encrypt(padded)

    def decrypt_cfb(self, ciphertext):
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
        padded = cipher.decrypt(ciphertext)
        return unpad_iso7816_4(padded)

if __name__ == "__main__":
    engine = CryptoEngine()
    msg = b"Secure Communications"
    
    ct_ecb = engine.encrypt_ecb(msg)
    pt_ecb = engine.decrypt_ecb(ct_ecb)
    
    ct_cbc = engine.encrypt_cbc(msg)
    pt_cbc = engine.decrypt_cbc(ct_cbc)
    
    ct_cfb = engine.encrypt_cfb(msg)
    pt_cfb = engine.decrypt_cfb(ct_cfb)
    
    print(f"Original: {msg.decode()}\n")
    print(f"ECB Decrypted: {pt_ecb.decode()}")
    print(f"CBC Decrypted: {pt_cbc.decode()}")
    print(f"CFB Decrypted: {pt_cfb.decode()}")