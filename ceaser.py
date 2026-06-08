def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    
    
    if mode == 'decrypt':
        shift = -shift
        
    for char in text:
       
        if char.isupper():
           
            result += chr((ord(char) - 65 + shift) % 26 + 65)
       
        elif char.islower():
            result += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
           
            result += char
            
    return result

def main():
    print("--- Caesar Cipher Program ---")
    
   
    plaintext = input("Enter the plaintext: ")
    while True:
        try:
            key = int(input("Enter the key (integer shift): "))
            break
        except ValueError:
            print("Invalid key! Please enter a valid integer.")
            
    
    ciphertext = caesar_cipher(plaintext, key, mode='encrypt')
    print(f"\n[+] Encrypted Cipher Text: {ciphertext}")
    
    
    decrypted_text = caesar_cipher(ciphertext, key, mode='decrypt')
    print(f"[+] Recovered Plaintext:   {decrypted_text}")

if __name__ == "__main__":
    main()