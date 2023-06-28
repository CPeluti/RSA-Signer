import random
import hashlib
import base64
def millerRabin(d,n):
    a  = 2 + random.randint(1,(n-4))
    x = pow(a,d,n)
    if(x==n-1 or x ==1): return True
    while(d!=n-1):
        x = (x*x) % n
        d *= 2
        if(x==1): return False
        if (x==n-1): return True
    return False

def isPrime(n, k):
    if (n <= 1 or n == 4):
        return False;
    if n <= 3:
        return True
    d = n-1
    while(d%2 == 0):
        d //= 2

    for i in range(k):
        if(not millerRabin(d,n)): return False
    return True

def genPrime():
    while(True):
        num = random.getrandbits(1024)
        if(isPrime(num,15)):
            return num
        
def extendEuclid(a, b):
    # a * x + b * y = euclid(a, b)
    print(a, b)
    if a == 0:
        return b, 0, 1
    
    gcd,x1,y1 = extendEuclid(b%a, a)

    x = y1 - (b//a) * x1
    y = x1
     
    return gcd,x,y
    
def invertedModule(a, b):
    # d * e = 1 (mod lcm) <=> d * e + k * lcm = 1 
    gcd, x, y = extendEuclid(a, b)

    if (gcd != 1):
        return None
    else:
        return (x % b + b) % b
    
def genPrivateKey(e, p, q):
    phi = (p-1)*(q-1)
    
    d = invertedModule(e, phi)
    return d
    

def genKey(p, q, e=None):
    #public key
    if(e == None):
        while(isPrime(e, phi)):
            e = random.randrange(1, phi)
    n = p*q

    # private key
    d = genPrivateKey(e, p, q)
    return ((e, n), (d, n)) # (public, private)

def oaep_encode(message, public_key):
    seed = random.getrandbits(512).to_bytes(64,'big')
    #result da hash da função g
    g = hashlib.sha3_512()
    g.update(seed)
    res_g = g.digest()
    # print(len(res_g))

    m = message.encode('ascii')
    # m = base64.b64encode(m)
    m = m+(len(res_g)-len(m))*b'\0'
    res_g = int.from_bytes(res_g, 'big')
    m = int.from_bytes(m,'big')
    x = m^res_g
    x = x.to_bytes(64,'big')
    h=hashlib.sha3_512()
    h.update(x)
    res_h = h.digest()
    # seed_hex = seed.hex()
    seed_int = int.from_bytes(seed,'big')
    res_h = int.from_bytes(res_h,'big')
    y = res_h ^ seed_int
    # xor_m_with_res_g = hex(res_g_hex)^hex(m_hex)
    print(len(x))
    print(len(y.to_bytes(64,'big')))
    return g.digest()

def run():
    # gera os dois números primos
    # p = genPrime()
    # q = genPrime()
    # e = 65537
    # print(f"NUMERO P = {p}")
    # print(f"NUMERO Q = {q}")
    # p = 5
    # q = 17
    # e = 11

    # k = genKey(p, q, e)
    # print(k)
    
    oaep_encode("teste", "teste2")
    return
