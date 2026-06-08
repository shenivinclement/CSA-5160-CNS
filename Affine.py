def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt_affine(text, a, b):
    result = ""
    for char in text:
        if char.isupper():
            result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
        elif char.islower():
            result += chr(((a * (ord(char) - 97) + b) % 26) + 97)
        else:
            result += char
    return result

def decrypt_affine(text, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return None
        
    for char in text:
        if char.isupper():
            result += chr(((a_inv * ((ord(char) - 65) - b)) % 26) + 65)
        elif char.islower():
            result += chr(((a_inv * ((ord(char) - 97) - b)) % 26) + 97)
        else:
            result += char
    return result

def main():
    print("--- Affine Cipher Program ---")
    
    plaintext = input("Enter the plaintext: ")
    try:
        a = int(input("Enter key 'a' (must be coprime with 26): "))
        b = int(input("Enter key 'b' (any integer): "))
    except ValueError:
        print("Error: Keys must be integers.")
        return

    if gcd(a, 26) != 1:
        print(f"Error: Key 'a' ({a}) is not coprime with 26. Valid choices are: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25.")
        return

    ciphertext = encrypt_affine(plaintext, a, b)
    print(f"\n[+] Encrypted Ciphertext: {ciphertext}")
    
    recovered_text = decrypt_affine(ciphertext, a, b)
    print(f"[+] Decrypted Plaintext:  {recovered_text}")

if __name__ == "__main__":
    main()