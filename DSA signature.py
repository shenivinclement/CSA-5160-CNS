import os
import hashlib

def mod_inverse(a, m):
    g, x, y = ext_gcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = ext_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

class DSAMock:
    def __init__(self):
        self.p = 0xFD7F53023D4718331C94002FD721171A429B0013685824D5BBCD631015FA61B8FAF7DF45FBC6FA7D60F4D086A8ED0AD7BD23215DAB4C95A97DFFDA08A58D8AD5D8E42646FC79282927BA13978C3B1278C64CEEC49DF4BEEDC4A73111453CA640ED0FD1CBCC2400C54784EF4D857E4DF2DC587974CA68ACF5F89A50F6126E2D0C79FB97B76D743770415A5A43CA4DAF48467A604AA5FCBE3DA7DA0CD3EB3E3DCEBE5BFC1486FA1B4AFB9BD12404FEA97FF72F9A95EC3B55276D36DA7128DFCD2AA14D3507BE2A3AA2CD9331AC3206A46AFED25A4CCCEAE164A4A28B10BE6FA78CC7B918E298F1E80BEF4EFE7950E5590D0190CE9A39ED18059A1D0E4D5174087E30E0FD69
        self.q = 0x95475CF4E422E3A17A2832AC2C1236CBE976F861
        self.g = 0xF75654321727EF1A9C4C61530A24A69A5780A79E2E958ED15BE0CA0ECA6F0AD2826CEA7D69116B2786B6AAE0A6F4E8D1D137748B47E64B29BE4B8E179F93ADCA2F6ED8E3DA8929A6624DF8DA4D4A1CEB9E66CE6EF6A0DA53A233DE74724E3BE7AF58C0B9F740D8FBD737DFE9FB2EED6CB8D540A2C9107F8A5DAA8A8EBCC1AA28AFEE546747EAFFB8E5F482DF0078A1ED8D5A3A05FF9FA75DFFB13A2AA16AE8BB7B6EB126AD7AA78E29BCFA518AA3BD72EE964098FF249FA29EF9A60DF414F5A29FAAAAB7B9AD8091E0A081F78A1D391A23CCBB51B5A3BF754593E9FCB170B1CA6B198A62EAEE54C62B034EFC997A8D3BF2386DFAD27855C6CA7A8007DCB8624E62CC
        self.__x = 0x5D33A29B72F4102CE75DFA8D1214A36B698AA850
        self.y = pow(self.g, self.__x, self.p)

    def sign_with_nonce(self, message, k):
        h = int(hashlib.sha1(message).hexdigest(), 16)
        r = pow(self.g, k, self.p) % self.q
        k_inv = mod_inverse(k, self.q)
        s = (k_inv * (h + self.__x * r)) % self.q
        return r, s

if __name__ == "__main__":
    dsa = DSAMock()
    
    msg1 = b"Transaction details for block A"
    msg2 = b"Transaction details for block B"
    
    h1 = int(hashlib.sha1(msg1).hexdigest(), 16)
    h2 = int(hashlib.sha1(msg2).hexdigest(), 16)
    
    reused_k = 0x76239102482A102DEE84120398410293AA810234
    
    r1, s1 = dsa.sign_with_nonce(msg1, reused_k)
    r2, s2 = dsa.sign_with_nonce(msg2, reused_k)
    
    print(f"Message 1: {msg1}")
    print(f"Signature 1 (r, s): ({hex(r1)}, {hex(s1)})\n")
    print(f"Message 2: {msg2}")
    print(f"Signature 2 (r, s): ({hex(r2)}, {hex(s2)})\n")
    
    s_diff_inv = mod_inverse((s1 - s2) % dsa.q, dsa.q)
    recovered_k = ((h1 - h2) * s_diff_inv) % dsa.q
    
    r_inv = mod_inverse(r1, dsa.q)
    recovered_x = (((s1 * recovered_k) - h1) * r_inv) % dsa.q
    
    print(f"Recovered Nonce (k):  {hex(recovered_k)}")
    print(f"Recovered Private Key: {hex(recovered_x)}")
    
    if recovered_x == dsa._DSAMock__x:
        print("\nVerification: SUCCESS - Private key completely leaked due to nonce reuse.")
    else:
        print("\nVerification: FAILURE")