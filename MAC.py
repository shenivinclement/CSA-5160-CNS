import os
from Cryptodome.Cipher import AES

def pad(data):
    padding_len = 16 - (len(data) % 16)
    return data + bytes([padding_len] * padding_len)

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

class CBCMACSystem:
    def __init__(self):
        self.__key = os.urandom(16)

    def compute_mac(self, message):
        cipher = AES.new(self.__key, AES.MODE_CBC, iv=bytes(16))
        ct = cipher.encrypt(message)
        return ct[-16:]

if __name__ == "__main__":
    server = CBCMACSystem()

    X = pad(b"OneBlockMessage")
    T = server.compute_mac(X)

    block2 = xor_bytes(X, T)
    two_block_message = X + block2

    T_forged = server.compute_mac(two_block_message)

    print(f"Message X (hex):          {X.hex()}")
    print(f"MAC T = MAC(K, X) (hex):  {T.hex()}\n")
    print(f"Forged Message X || (X ^ T) (hex):\n{two_block_message.hex()}\n")
    print(f"MAC of Forged Message (hex): {T_forged.hex()}")
    print(f"Original MAC T (hex):        {T.hex()}\n")

    if T_forged == T:
        print("Verification: SUCCESS")