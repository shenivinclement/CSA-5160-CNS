import secrets

SHARED_PRIME_P = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF", 16
)
SHARED_GENERATOR_G = 2

class Party:
    def __init__(self, name):
        self.name = name
        self.__private_key = secrets.randbelow(SHARED_PRIME_P - 2) + 2
        self.public_key = None
        self.shared_secret = None

    def generate_public_key(self):
        self.public_key = pow(SHARED_GENERATOR_G, self.__private_key, SHARED_PRIME_P)
        return self.public_key

    def compute_shared_secret(self, received_public_key):
        self.shared_secret = pow(received_public_key, self.__private_key, SHARED_PRIME_P)
        return self.shared_secret


if __name__ == "__main__":
    print("--- Starting Diffie-Hellman Key Exchange Simulation --- \n")

    alice = Party("Alice")
    bob = Party("Bob")

    alice_public = alice.generate_public_key()
    bob_public = bob.generate_public_key()

    print(f"[Alice] Public Key generated (truncated): {hex(alice_public)[:20]}...")
    print(f"[Bob]   Public Key generated (truncated): {hex(bob_public)[:20]}...\n")
    print("... Exchanging Public Keys over an insecure channel ...\n")

    alice_secret = alice.compute_shared_secret(bob_public)
    bob_secret = bob.compute_shared_secret(alice_public)

    print(f"[Alice] Computed Shared Secret (truncated): {hex(alice_secret)[:20]}...")
    print(f"[Bob]   Computed Shared Secret (truncated): {hex(bob_secret)[:20]}...\n")

    print("--- Verification ---")
    if alice_secret == bob_secret:
        print("Success! Both parties derived the exact same shared secret key.")
    else:
        print("Error: Shared secrets do not match.")