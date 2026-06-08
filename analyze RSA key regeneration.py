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

def analyze_shared_prime(n1, n2, e=65537):
    p = gcd_extended(n1, n2)[0]
    if p > 1 and p != n1 and p != n2:
        q1 = n1 // p
        phi1 = (p - 1) * (q1 - 1)
        d1 = mod_inverse(e, phi1)
        return True, {"p": p, "q1": q1, "d1": d1}
    return False, {}

def analyze_common_modulus(n, e1, e2, c1, c2):
    gcd, r, s = gcd_extended(e1, e2)
    if gcd != 1:
        return False, None
    
    if r < 0:
        c1 = mod_inverse(c1, n)
        r = -r
    if s < 0:
        c2 = mod_inverse(c2, n)
        s = -s
        
    if c1 is None or c2 is None:
        return False, None
        
    recovered_message = (pow(c1, r, n) * pow(c2, s, n)) % n
    return True, recovered_message

def main():
    print("--- RSA Key Regeneration & Parameter Reuse Security Lab ---")
    
    p_shared = 104729
    q1 = 1299827
    q2 = 15485863
    
    n1 = p_shared * q1
    n2 = p_shared * q2
    
    print("\n[Test 1] Testing Shared Prime Factor Vulnerability...")
    print(f"Key A Modulus (n1): {n1}")
    print(f"Key B Modulus (n2): {n2}")
    
    vuln_detected, leaked_data = analyze_shared_prime(n1, n2)
    if vuln_detected:
        print(" -> RISK DETECTED: Shared prime factor identified instantly via GCD!")
        print(f" -> Leaked Factor p: {leaked_data['p']}")
        print(f" -> Recovered Key A Private Exponent d1: {leaked_data['d1']}")
        
    print("\n[Test 2] Testing Common Modulus Vulnerability (Reusing n with different e)...")
    p_common = 179424673
    q_common = 275604541
    n_common = p_common * q_common
    e1 = 11
    e2 = 13
    
    secret_message = 42
    c1 = pow(secret_message, e1, n_common)
    c2 = pow(secret_message, e2, n_common)
    
    print(f"Common Modulus (n): {n_common}")
    print(f"Ciphertext 1 (encrypted with e1={e1}): {c1}")
    print(f"Ciphertext 2 (encrypted with e2={e2}): {c2}")
    
    attack_success, recovered_msg = analyze_common_modulus(n_common, e1, e2, c1, c2)
    if attack_success:
        print(" -> RISK DETECTED: Message decrypted without factoring n!")
        print(f" -> Intercepted Secret Message: {recovered_msg}")

if __name__ == "__main__":
    main()