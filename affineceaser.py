import math

def encrypt_affine(plaintext, a, b):
    if math.gcd(a, 26) != 1:
        raise ValueError(f"Key 'a' ({a}) must be coprime to 26 for the cipher to be one-to-one.")
        
    ciphertext = []
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p = ord(char) - base
            c = (a * p + b) % 26
            ciphertext.append(chr(c + base))
        else:
            ciphertext.append(char)
    return "".join(ciphertext)

def decrypt_affine(ciphertext, a, b):
    if math.gcd(a, 26) != 1:
        raise ValueError(f"Key 'a' ({a}) must be coprime to 26 for the cipher to be one-to-one.")
        
    a_inv = pow(a, -1, 26)
    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c = ord(char) - base
            p = (a_inv * (c - b)) % 26
            plaintext.append(chr(p + base))
        else:
            plaintext.append(char)
    return "".join(plaintext)

if __name__ == "__main__":
    msg = "AffineCipher"
    
    valid_a = 7
    b = 3
    
    print(f"--- Demonstration with Valid Key (a={valid_a}, b={b}) ---")
    ct = encrypt_affine(msg, valid_a, b)
    pt = decrypt_affine(ct, valid_a, b)
    print(f"Plaintext:  {msg}")
    print(f"Ciphertext: {ct}")
    print(f"Decrypted:  {pt}\n")
    
    invalid_a = 2
    print(f"--- Demonstration of Failure with Invalid Key (a={invalid_a}, b={b}) ---")
    p1 = 0   
    p2 = 13  
    
    c1 = (invalid_a * p1 + b) % 26
    c2 = (invalid_a * p2 + b) % 26
    
    print(f"Plaintext index {p1} ('A') maps to ciphertext index: {c1}")
    print(f"Plaintext index {p2} ('N') maps to ciphertext index: {c2}")
    if c1 == c2:
        print("Collision confirmed: Mapping is not one-to-one, decryption is impossible.")