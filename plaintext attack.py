import numpy as np

def mod26(a):
    return int(a) % 26

def find_mod_inverse(a, m=26):
    a = mod26(a)
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1

def invert_matrix_2x2(P):
    det = mod26(P[0, 0] * P[1, 1] - P[0, 1] * P[1, 0])
    det_inv = find_mod_inverse(det, 26)
    
    if det_inv == -1:
        return None
        
    P_inv = np.zeros((2, 2), dtype=int)
    P_inv[0, 0] = mod26(P[1, 1] * det_inv)
    P_inv[0, 1] = mod26(-P[0, 1] * det_inv)
    P_inv[1, 0] = mod26(-P[1, 0] * det_inv)
    P_inv[1, 1] = mod26(P[0, 0] * det_inv)
    return P_inv

if __name__ == "__main__":
    target_K = np.array([[7, 8], [11, 11]], dtype=int)
    
    P = np.array([[4, 19], [13, 19]], dtype=int)
    
    C = mod26(np.dot(P, target_K))
    
    print("--- Known Plaintext Attack on Hill Cipher (Python) ---")
    print(f"Intercepted Plaintext Matrix P:\n{P}\n")
    print(f"Intercepted Ciphertext Matrix C:\n{C}\n")
    
    P_inv = invert_matrix_2x2(P)
    
    if P_inv is None:
        print("Error: Plaintext matrix is not invertible modulo 26.")
    else:
        recovered_K = mod26(np.dot(P_inv, C))
        print(f"Recovered Secret Key Matrix K:\n{recovered_K}\n")
        
        if np.array_equal(recovered_K, target_K):
            print("Verification: SUCCESS - Key recovered perfectly.")