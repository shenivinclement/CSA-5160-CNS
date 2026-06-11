import hashlib

def simulate_dsa_signatures(message):
    print("--- DSA Signature Generation Simulation ---")
    print(f"Message to sign: \"{message}\"\n")

    q = 101
    g = 2
    x = 7
    p = 1007
    h = 42

    k1 = 13
    r1 = pow(g, k1, p) % q
    s1 = (pow(k1, q - 2, q) * (h + x * r1)) % q

    k2 = 29
    r2 = pow(g, k2, p) % q
    s2 = (pow(k2, q - 2, q) * (h + x * r2)) % q

    print(f"Occasion 1 (using random nonce k = {k1}):")
    print(f"  Signature R1: {r1}")
    print(f"  Signature S1: {s1}\n")

    print(f"Occasion 2 (using random nonce k = {k2}):")
    print(f"  Signature R2: {r2}")
    print(f"  Signature S2: {s2}\n")


def simulate_rsa_signatures(message):
    print("--- RSA Signature Generation Simulation ---")
    print(f"Message to sign: \"{message}\"\n")

    d = 7
    n = 33
    h = 4

    sig1 = pow(h, d, n)
    sig2 = pow(h, d, n)

    print("Occasion 1 (Deterministic hashing + private key):")
    print(f"  Signature: {sig1}\n")

    print("Occasion 2 (Deterministic hashing + private key):")
    print(f"  Signature: {sig2}\n")


if __name__ == "__main__":
    msg = "Authorize transaction ID 54032"
    simulate_dsa_signatures(msg)
    simulate_rsa_signatures(msg)