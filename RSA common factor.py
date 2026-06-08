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
    return (x % phi + phi) % phi

def rsa_common_factor_attack(n1, n2, e=65537):
    shared_prime = gcd_extended(n1, n2)[0]
    
    if shared_prime == 1 or shared_prime == n1 or shared_prime == n2:
        return None
        
    p1 = shared_prime
    q1 = n1 // p1
    phi1 = (p1 - 1) * (q1 - 1)
    d1 = mod_inverse(e, phi1)
    
    p2 = shared_prime
    q2 = n2 // p2
    phi2 = (p2 - 1) * (q2 - 1)
    d2 = mod_inverse(e, phi2)
    
    return {
        "shared_prime": shared_prime,
        "key1": {"p": p1, "q": q1, "d": d1},
        "key2": {"p": p2, "q": q2, "d": d2}
    }

def main():
    print("--- RSA Common Factor Attack Demonstration ---")
    
    p = 3242295733
    q1 = 3988012679
    q2 = 4222234199
    
    n1 = p * q1
    n2 = p * q2
    e = 65537
    
    print(f"Public Key 1 Modulus (n1): {n1}")
    print(f"Public Key 2 Modulus (n2): {n2}")
    print(f"Shared Public Exponent (e): {e}")
    print("-" * 50)
    
    print("\nExecuting Attack... Calculating gcd(n1, n2)")
    result = rsa_common_factor_attack(n1, n2, e)
    
    if result:
        print("\n[!] Attack Successful! Shared prime factor detected.")
        print(f"Shared Prime (p): {result['shared_prime']}")
        
        print("\n--- Recovered Key 1 Components ---")
        print(f"p: {result['key1']['p']}")
        print(f"q: {result['key1']['q']}")
        print(f"Private Exponent (d1): {result['key1']['d']}")
        
        print("\n--- Recovered Key 2 Components ---")
        print(f"p: {result['key2']['p']}")
        print(f"q: {result['key2']['q']}")
        print(f"Private Exponent (d2): {result['key2']['d']}")
    else:
        print("\n[-] Attack Failed. No shared prime factors found.")

if __name__ == "__main__":
    main()