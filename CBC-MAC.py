import os
from Cryptodome.Cipher import AES

def pad(data):
    padding_len = 16 - (len(data) % 16)
    return data + bytes([padding_len] * padding_len)

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

class CBCMACServer:
    def __init__(self):
        self.__key = os.urandom(16)

    def generate_mac(self, message):
        if len(message) % 16 != 0:
            return None
        cipher = AES.new(self.__key, AES.MODE_CBC, iv=bytes(16))
        ct = cipher.encrypt(message)
        return ct[-16:]

    def verify_mac(self, message, mac):
        computed_mac = self.generate_mac(message)
        if computed_mac is None:
            return False
        return secrets.compare_digest(computed_mac, mac)

if __name__ == "__main__":
    import secrets

    server = CBCMACServer()

    m1 = pad(b"Transfer 100 USD to Alice")
    mac1 = server.generate_mac(m1)

    m2 = pad(b"Transfer 500 USD to Bob")
    mac2 = server.generate_mac(m2)

    forged_block = xor_bytes(m2[:16], mac1)
    m3 = m1 + forged_block + m2[16:]

    mac3 = server.generate_mac(m3)

    print("--- CBC-MAC Forgery Analysis ---")
    print(f"Message 1: {m1}")
    print(f"MAC 1:     {mac1.hex()}")
    print(f"Message 2: {m2}")
    print(f"MAC 2:     {mac2.hex()}\n")
    print(f"Forged Message 3: {m3}")
    print(f"Expected MAC 3:   {mac2.hex()}")
    print(f"Actual MAC 3:     {mac3.hex()}\n")

    if mac3 == mac2:
        print("Verification: SUCCESS")
        print("Weakness: Standard CBC-MAC is insecure for variable-length messages without length separation.")
    else:
        print("Verification: FAILURE")