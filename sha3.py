import numpy as np

ROUND_CONSTANTS = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008
]

ROTATION_OFFSETS = [
    [0,  1, 62, 28, 27],
    [36, 44,  6, 55, 20],
    [3, 10, 43, 25, 39],
    [41, 45, 15, 21,  8],
    [18,  2, 61, 56, 14]
]

def keccak_round(state, rc):
    C = np.zeros(5, dtype=np.uint64)
    for x in range(5):
        C[x] = state[x, 0] ^ state[x, 1] ^ state[x, 2] ^ state[x, 3] ^ state[x, 4]
    
    D = np.zeros(5, dtype=np.uint64)
    for x in range(5):
        D[x] = C[(x - 1) % 5] ^ ((C[(x + 1) % 5] << np.uint64(1)) | (C[(x + 1) % 5] >> np.uint64(63)))
    
    for x in range(5):
        for y in range(5):
            state[x, y] ^= D[x]
            
    B = np.zeros((5, 5), dtype=np.uint64)
    for x in range(5):
        for y in range(5):
            r = ROTATION_OFFSETS[x][y]
            B[y, (2 * x + 3 * y) % 5] = (state[x, y] << np.uint64(r)) | (state[x, y] >> np.uint64(64 - r))
            
    for x in range(5):
        for y in range(5):
            state[x, y] = B[x, y] ^ ((~B[(x + 1) % 5, y]) & B[(x + 2) % 5, y])
            
    state[0, 0] ^= rc
    return state

def hamming_distance(state1, state2):
    diff = state1 ^ state2
    distance = 0
    for x in range(5):
        for y in range(5):
            distance += bin(diff[x, y]).count('1')
    return distance

if __name__ == "__main__":
    state_a = np.zeros((5, 5), dtype=np.uint64)
    state_b = np.zeros((5, 5), dtype=np.uint64)
    
    state_b[0, 0] ^= np.uint64(1)
    
    print(f"{'Round':<6}{'Hamming Distance':<18}{'Diffusion %':<12}")
    print("-" * 38)
    
    init_dist = hamming_distance(state_a, state_b)
    print(f"{'Init':<6}{init_dist:<18}{((init_dist / 1600) * 100):.2f}%")
    
    for r in range(24):
        state_a = keccak_round(state_a, ROUND_CONSTANTS[r])
        state_b = keccak_round(state_b, ROUND_CONSTANTS[r])
        
        dist = hamming_distance(state_a, state_b)
        percentage = (dist / 1600) * 100
        print(f"{r+1:<6}{dist:<18}{percentage:.2f}%")