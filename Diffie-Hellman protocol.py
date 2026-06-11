import math

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def standard_diffie_hellman():
    q = 23
    a = 5

    x_alice = 6
    x_bob = 15

    A = pow(a, x_alice, q)
    B = pow(a, x_bob, q)

    secret_alice = pow(B, x_alice, q)
    secret_bob = pow(A, x_bob, q)

    print("--- Standard Diffie-Hellman ---")
    print(f"Alice Public: {A}, Bob Public: {B}")
    print(f"Alice Secret: {secret_alice}, Bob Secret: {secret_bob}\n")

def linear_variant_with_attack():
    q = 23
    a = 5

    x_alice = 6
    x_bob = 15

    X_A = (x_alice * a) % q
    X_B = (x_bob * a) % q

    key_alice = (X_B * x_alice) % q
    key_bob = (X_A * x_bob) % q

    print("--- Linear Variant (x * a % q) ---")
    print(f"Alice Public Exchange: {X_A}")
    print(f"Bob Public Exchange:   {X_B}")
    print(f"Alice Derived Key:     {key_alice}")
    print(f"Bob Derived Key:       {key_bob}\n")

    print("--- Eve's Attack ---")
    a_inv = mod_inverse(a, q)
    
    recovered_x_alice = (X_A * a_inv) % q
    recovered_x_bob = (X_B * a_inv) % q
    print(f"Eve recovered Alice's secret number: {recovered_x_alice}")
    print(f"Eve recovered Bob's secret number:   {recovered_x_bob}")

    recovered_key = (X_A * X_B * a_inv) % q
    print(f"Eve intercepted shared key directly: {recovered_key}")

if __name__ == "__main__":
    standard_diffie_hellman()
    linear_variant_with_attack()