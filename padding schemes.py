def pkcs7_pad(data, block_size):
    if block_size < 1 or block_size > 255:
        raise ValueError("Block size must be between 1 and 255 bytes.")
        
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len] * padding_len)
    return data + padding

def pkcs7_unpad(padded_data, block_size):
    if len(padded_data) == 0:
        raise ValueError("Data is empty.")
        
    if len(padded_data) % block_size != 0:
        raise ValueError("Data length is not a multiple of the block size.")
        
    padding_len = padded_data[-1]
    
    if padding_len < 1 or padding_len > block_size:
        raise ValueError("Invalid padding value.")
        
    for i in range(len(padded_data) - padding_len, len(padded_data)):
        if padded_data[i] != padding_len:
            raise ValueError("Invalid padding bytes detected.")
            
    return padded_data[:-padding_len]

def demonstrate_padding(input_string, block_size):
    data_bytes = input_string.encode('utf-8')
    padded = pkcs7_pad(data_bytes, block_size)
    unpadded = pkcs7_unpad(padded, block_size)
    
    print(f"Original Text:   '{input_string}' (Length: {len(data_bytes)} bytes)")
    print(f"Padded Hex:      {padded.hex().upper()} (Length: {len(padded)} bytes)")
    print(f"Unpadded Hex:    {unpadded.hex().upper()}")
    print(f"Recovered Text:  '{unpadded.decode('utf-8')}'")
    print("-" * 50)

def main():
    print("--- PKCS#7 Block Cipher Padding Program ---")
    block_size = 8
    print(f"Using Block Size: {block_size} bytes\n")
    
    test_cases = [
        "HELLO",          
        "PADDING1",       
        "A VERY LONG SENTENCE FOR TESTING", 
        ""                
    ]
    
    for test in test_cases:
        demonstrate_padding(test, block_size)

if __name__ == "__main__":
    main()