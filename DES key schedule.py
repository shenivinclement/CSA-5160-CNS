PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def hex_to_bin(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(64)

def bin_to_hex(bin_str):
    return hex(int(bin_str, 2))[2:].upper().zfill(12)

def permute(block, table):
    return "".join(block[pos - 1] for pos in table)

def left_shift(block, num_shifts):
    return block[num_shifts:] + block[:num_shifts]

def generate_round_keys(hex_key):
    bin_key = hex_to_bin(hex_key)
    
    permuted_key = permute(bin_key, PC1)
    
    c = permuted_key[:28]
    d = permuted_key[28:]
    
    round_keys = []
    
    for round_num in range(16):
        shifts = SHIFT_SCHEDULE[round_num]
        c = left_shift(c, shifts)
        d = left_shift(d, shifts)
        
        combined = c + d
        round_key_bin = permute(combined, PC2)
        round_keys.append(bin_to_hex(round_key_bin))
        
    return round_keys

def main():
    print("--- DES Key Schedule Generator ---")
    
    hex_key = input("Enter a 16-character Hexadecimal Key (64-bit): ").strip()
    
    if len(hex_key) != 16 or not all(c in "0123456789ABCDEFabcdef" for c in hex_key):
        print("Error: Key must be exactly 16 hexadecimal characters long.")
        return
        
    round_keys = generate_round_keys(hex_key)
    
    print(f"\nOriginal Key (Hex): {hex_key.upper()}")
    print("-" * 35)
    for i, key in enumerate(round_keys):
        print(f"Round {str(i+1).zfill(2)} Key: {key}")

if __name__ == "__main__":
    main()
