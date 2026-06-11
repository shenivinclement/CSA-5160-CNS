import numpy as np

RATE_LANES = 16
CAPACITY_LANES = 9

state = np.zeros((5, 5), dtype=np.uint64)

lane_idx = 0
for y in range(5):
    for x in range(5):
        if lane_idx < RATE_LANES:
            state[x, y] = np.uint64(1)
        else:
            state[x, y] = np.uint64(0)
        lane_idx += 1

def theta_step(st):
    C = np.zeros(5, dtype=np.uint64)
    for x in range(5):
        C[x] = st[x, 0] ^ st[x, 1] ^ st[x, 2] ^ st[x, 3] ^ st[x, 4]
        
    D = np.zeros(5, dtype=np.uint64)
    for x in range(5):
        left = C[(x + 4) % 5]
        right = C[(x + 1) % 5]
        rotated_right = (right << np.uint64(1)) | (right >> np.uint64(63))
        D[x] = left ^ rotated_right
        
    for x in range(5):
        for y in range(5):
            st[x, y] ^= D[x]
    return st

def count_nonzero_capacity(st):
    count = 0
    checked = 0
    for y in range(5):
        for x in range(5):
            if checked >= RATE_LANES:
                if st[x, y] != 0:
                    count += 1
            checked += 1
    return count

print("Before Permutation Round:")
print(f"Non-zero capacity lanes: {count_nonzero_capacity(state)} / {CAPACITY_LANES}\n")

state = theta_step(state)

print("After 1 Round (Theta Step Execution):")
print(f"Non-zero capacity lanes: {count_nonzero_capacity(state)} / {CAPACITY_LANES}")