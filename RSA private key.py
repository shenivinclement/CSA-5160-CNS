def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, y = gcd_extended(e, phi)
    if gcd != 1:
        return None
    else:
        return (x % phi + phi) % phi

def compute_rsa_private_key(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    if phi % e == 0 or gcd_extended(e, phi)[0] != 1:
        raise ValueError("Public exponent 'e' is not coprime with phi(n).")
        
    d = mod_inverse(e, phi)
    return n, d

def main():
    print("--- RSA Private Key Calculator ---")
    
    try:
        p = int(input("Enter prime number p: "))
        q = int(input("Enter prime number q: "))
        e = int(input("Enter public exponent e (often 65537): "))
    except ValueError:
        print("Error: All inputs must be integers.")
        return

    try:
        n, d = compute_rsa_private_key(p, q, e)
        
        print("\n--- Computed RSA Parameters ---")
        print(f"Modulus (n) = p * q:       {n}")
        print(f"Totient (phi(n)):          {(p - 1) * (q - 1)}")
        print(f"Public Exponent (e):       {e}")
        print("-" * 32)
        print(f"Private Exponent (d):      {d}")
        print(f"\n[+] Complete Private Key Components: (n={n}, d={d})")
        
    except ValueError as err:
        print(f"\n[!] Configuration Error: {err}")

if __name__ == "__main__":
    main()