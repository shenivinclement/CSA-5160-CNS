import os
import secrets
from Cryptodome.Cipher import AES

class PaddingOracleServer:
    def __init__(self):
        self.__key = os.urandom(16)

    def encrypt(self, plaintext):
        iv = os.urandom(16)
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        
        padding_len = 16 - (len(plaintext) % 16)
        padded_data = plaintext + bytes([padding_len] * padding_len)
        
        ciphertext = cipher.encrypt(padded_data)
        return iv + ciphertext

    def decrypt_and_verify_padding(self, iv_and_ciphertext):
        if len(iv_and_ciphertext) < 32 or len(iv_and_ciphertext) % 16 != 0:
            return False
            
        iv = iv_and_ciphertext[:16]
        ciphertext = iv_and_ciphertext[16:]
        
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        
        padding_len = decrypted[-1]
        if padding_len < 1 or padding_len > 16:
            return False
            
        for i in range(len(decrypted) - padding_len, len(decrypted)):
            if decrypted[i] != padding_len:
                return False
                
        return True


def padding_oracle_attack_block(ct_block, iv_or_prev_ct, oracle_func):
    intermediate_block = bytearray(16)
    decrypted_plaintext = bytearray(16)
    
    for padding_val in range(1, 17):
        modified_iv = bytearray(16)
        
        for i in range(1, padding_val):
            modified_iv[16 - i] = intermediate_block[16 - i] ^ padding_val
            
        found = False
        for byte_guess in range(256):
            modified_iv[16 - padding_val] = byte_guess
            
            payload = bytes(modified_iv) + ct_block
            if oracle_func(payload):
                if padding_val == 1:
                    modified_iv[14] ^= 1
                    payload_check = bytes(modified_iv) + ct_block
                    if not oracle_func(payload_check):
                        continue
                
                intermediate_byte = byte_guess ^ padding_val
                intermediate_block[16 - padding_val] = intermediate_byte
                decrypted_plaintext[16 - padding_val] = intermediate_byte ^ iv_or_prev_ct[16 - padding_val]
                found = True
                break
                
        if not found:
            return None
            
    return bytes(decrypted_plaintext)


if __name__ == "__main__":
    server = PaddingOracleServer()
    secret_data = b"TopSecretPayload"
    
    encrypted_packet = server.encrypt(secret_data)
    
    print(f"Original Ciphertext (hex): {encrypted_packet.hex()}")
    print(f"Intercepted Packet Size:   {len(encrypted_packet)} bytes\n")
    
    iv = encrypted_packet[:16]
    target_block = encrypted_packet[16:32]
    
    print("--- Starting Padding Oracle Attack ---")
    recovered_bytes = padding_oracle_attack_block(target_block, iv, server.decrypt_and_verify_padding)
    
    if recovered_bytes:
        print(f"\nRecovered Padded Block (hex): {recovered_bytes.hex()}")
        pad_len = recovered_bytes[-1]
        unpadded = recovered_bytes[:-pad_len]
        print(f"Recovered Plaintext string:   {unpadded.decode('utf-8')}")
    else:
        print("\nAttack failed.")