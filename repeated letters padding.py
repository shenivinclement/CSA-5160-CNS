def prepare_key_matrix(key):
    key = key.upper().replace('J', 'I')
    seen = set()
    matrix = []
    
    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            matrix.append(char)
            
    for i in range(26):
        char = chr(65 + i)
        if char != 'J' and char not in seen:
            seen.add(char)
            matrix.append(char)
            
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return None

def prepare_text(text):
    text = "".join([c.upper() for c in text if c.isalpha()]).replace('J', 'I')
    prepared = ""
    i = 0
    
    while i < len(text):
        char1 = text[i]
        if i + 1 < len(text):
            char2 = text[i+1]
            if char1 == char2:
                prepared += char1 + 'X'
                i += 1
            else:
                prepared += char1 + char2
                i += 2
        else:
            prepared += char1 + 'X'
            i += 1
            
    return prepared

def playfair_cipher(text, matrix, mode='encrypt'):
    shift = 1 if mode == 'encrypt' else -1
    result = ""
    
    for i in range(0, len(text), 2):
        r1, c1 = find_position(matrix, text[i])
        r2, c2 = find_position(matrix, text[i+1])
        
        if r1 == r2:
            result += matrix[r1][(c1 + shift) % 5]
            result += matrix[r2][(c2 + shift) % 5]
        elif c1 == c2:
            result += matrix[(r1 + shift) % 5][c1]
            result += matrix[(r2 + shift) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]
            
    return result

def main():
    print("--- Playfair Cipher Demonstration ---")
    
    keyword = input("Enter the keyword: ")
    plaintext = input("Enter the plaintext: ")
    
    matrix = prepare_key_matrix(keyword)
    
    print("\n[+] Generated 5x5 Key Matrix:")
    for row in matrix:
        print(" ".join(row))
        
    prepared_text = prepare_text(plaintext)
    ciphertext = playfair_cipher(prepared_text, matrix, mode='encrypt')
    
    print("\n--- Process Details ---")
    print(f"Original Text:       {plaintext}")
    print(f"After Padding Rules: {prepared_text} (split into digraphs: {[prepared_text[i:i+2] for i in range(0, len(prepared_text), 2)]})")
    print(f"Ciphertext Output:   {ciphertext}")
    
    decrypted_text = playfair_cipher(ciphertext, matrix, mode='decrypt')
    print(f"Decryption Output:   {decrypted_text}")

if __name__ == "__main__":
    main()
