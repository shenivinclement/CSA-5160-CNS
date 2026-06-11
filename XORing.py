def shift_left_one_bit(b):
    out = bytearray(len(b))
    carry = 0
    for i in range(len(b) - 1, -1, -1):
        next_carry = (b[i] & 0x80) >> 7
        out[i] = ((b[i] << 1) & 0xFF) | carry
        carry = next_carry
    return bytes(out), carry

def derive_subkeys(block_size, encrypted_zeros):
    if block_size == 64:
        rb = bytes([0] * 7 + [0x1B])
    elif block_size == 128:
        rb = bytes([0] * 15 + [0x87])
    else:
        raise ValueError("Unsupported block size")

    k1_shift, carry1 = shift_left_one_bit(encrypted_zeros)
    if carry1:
        k1 = bytes(a ^ b for a, b in zip(k1_shift, rb))
    else:
        k1 = k1_shift

    k2_shift, carry2 = shift_left_one_bit(k1)
    if carry2:
        k2 = bytes(a ^ b for a, b in zip(k2_shift, rb))
    else:
        k2 = k2_shift

    return k1, k2

if __name__ == "__main__":
    mock_l_128 = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    k1, k2 = derive_subkeys(128, mock_l_128)
    print("--- 128-bit CMAC Subkeys ---")
    print(f"L:  {mock_l_128.hex()}")
    print(f"K1: {k1.hex()}")
    print(f"K2: {k2.hex()}\n")

    mock_l_64 = bytes.fromhex("4e6f6e6365426c6b")
    k1_64, k2_64 = derive_subkeys(64, mock_l_64)
    print("--- 64-bit CMAC Subkeys ---")
    print(f"L:  {mock_l_64.hex()}")
    print(f"K1: {k1_64.hex()}")
    print(f"K2: {k2_64.hex()}")