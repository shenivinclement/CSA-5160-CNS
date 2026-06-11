import os
from Cryptodome.Cipher import AES

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def shift_left_one_bit(b):
    out = bytearray(len(b))
    carry = 0
    for i in range(len(b) - 1, -1, -1):
        next_carry = (b[i] & 0x80) >> 7
        out[i] = ((b[i] << 1) & 0xFF) | carry
        carry = next_carry
    return bytes(out), carry

def generate_cmac_subkeys(key):
    cipher = AES.new(key, AES.MODE_ECB)
    L = cipher.encrypt(bytes(16))
    
    rb = bytes([0] * 15 + [0x87])
    
    L_shift, carry1 = shift_left_one_bit(L)
    if carry1:
        K1 = xor_bytes(L_shift, rb)
    else:
        K1 = L_shift
        
    K1_shift, carry2 = shift_left_one_bit(K1)
    if carry2:
        K2 = xor_bytes(K1_shift, rb)
    else:
        K2 = K1_shift
        
    return K1, K2

if __name__ == "__main__":
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    
    expected_k1 = bytes.fromhex("fbeed618357133667c85e08f7236a8de")
    expected_k2 = bytes.fromhex("f7ddac306ae266ccf90bc11ef46d513b")
    
    k1, k2 = generate_cmac_subkeys(key)
    
    print(f"Key: {key.hex()}")
    print(f"K1:  {k1.hex()}")
    print(f"K2:  {k2.hex()}\n")
    
    if k1 == expected_k1 and k2 == expected_k2:
        print("Verification: SUCCESS")
    else:
        print("Verification: FAILURE")