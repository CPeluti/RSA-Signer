import random
import hashlib
import base64
from textwrap import wrap
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
        return False
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
        if(isPrime(num,40)):
            return num
        
def extendEuclid(a, b):
    # a * x + b * y = euclid(a, b)
    # print(a, b)
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

def generate_random_number(bits):
    return random.getrandbits(bits).to_bytes(128, 'big')

def convert_message(message):
    m = message.encode('ISO-8859-1')
    if(len(m)>=128):
        n = 128
        m = [m[i:i+n] for i in range(0, len(m), n)]
    else:
        m = [m]
    return m
def deconvert_message(message_bytes):
    message = message_bytes.decode('ISO-8859-1').strip('\0')
    return message
def gen_message(message, size):
    # m = message.encode('ISO-8859-1')
    # m = base64.b64decode(message)
    m = message+(size-len(message))*b'\0'
    return m
def MGF1(seed, length):
    b = bytes()
    for i in range(0, length//64+1):
        b+=hashlib.sha3_512(seed + int.to_bytes(i, 4, 'big')).digest()
    return b[0:length]
def hash(input):
    h = MGF1(input, 128)
    return h

def xor(a,b):
    int_a=int.from_bytes(a,'big')
    int_b=int.from_bytes(b,'big')
    res = int_a^int_b
    return res.to_bytes(128,'big')

def oaep_encode(message):
    seed = generate_random_number(1024)
    #result da hash da função g
    res_g = hash(seed)
    # mensagem com o padding
    m =  gen_message(message, len(res_g))
    # primeiro xor
    x = xor(res_g, m)
    
    res_h = hash(x)    

    y = xor(res_h, seed)
    # xor_m_with_res_g = hex(res_g_hex)^hex(m_hex)
    return {"maskedDB": x, "maskedSeed": y}

def rsa_cypher(message, public_key):
    e, n = public_key
    return pow(message, e, n)

def oaep_decode(maskedSeed, maskedDB):
    seedMask = hash(maskedDB)
    seed = xor(seedMask, maskedSeed)
    dbMask = hash(seed)
    db = xor(dbMask, maskedDB)
    # db = db.decode('ISO-8859-1').strip('\0')
    # print(db.decode('ascii'))
    return db

def rsa_decypher(cypher_text, private_key):
    d, n = private_key
    return pow(cypher_text, d, n)

def generate_key_pair():
    p = genPrime()
    q = genPrime()
    e = 65537
    keys = genKey(p, q, e)
    return {"private": keys[0], "public": keys[1]}

def rsa_oaep_encode(message, public_key):
    rsa_encoded = bytearray()
    for byte_array in message:
        oaep_msg = oaep_encode(byte_array)
        oaep_bytes = bytearray(oaep_msg["maskedSeed"]) + bytearray(oaep_msg["maskedDB"])
        oaep_msg_concat = int.from_bytes(oaep_bytes, 'big')
        cipher = rsa_cypher(oaep_msg_concat,public_key)

        cipher = cipher.to_bytes(256,'big')
        rsa_encoded+=cipher
    # 
    # 
    b64 = base64.b64encode(rsa_encoded)
    return b64

def rsa_oaep_decode(cipher, private_key):
    decoded_msg = ''
    for block in cipher:
        number = int.from_bytes(block, 'big')
        deciphered_text = rsa_decypher(number,private_key)
        msg_bytes = bytearray(deciphered_text.to_bytes(256, 'big'))
        res = oaep_decode(msg_bytes[:128],msg_bytes[128:])
        decoded_msg+=deconvert_message(res)
    
    # print((deciphered_text.bit_length() + 7)// 8) 
    return decoded_msg

def run():
     # res = oaep_encode("teste")
    # res2= oaep_decode(res["maskedSeed"], res["maskedDB"])
    # print(res, res2)

    print("Escolha o modo do RSA:")
    print("1 - RSA")
    print("2 - RSA-OAEP")
    op = input("Digite sua escolha: ")
    match op:
        case "1":
            print("1 - Cifração em RSA")
            print("2 - Decifração em RSA")
            op = input("Digite sua escolha: ")
            if(op == "1"):
                print("---------------- CIFRAÇÃO -----------------")
                msg = input("Digite a mensagem que será cifrada: ")
                keys = generate_key_pair()
                print(f"CHAVE PÚBLICA: {keys['public']}")
                print(f"CHAVE PRIVADA: {keys['private']}")
                ciphered_text = rsa_cypher(int(msg), keys['public'])
                print("Essa é a mensagem cifrada:")
                print(ciphered_text)
            else:
                print("---------------- DECIFRAÇÃO -----------------")
                msg = input("Digite a mensagem que será decifrada: ")
                key = input("Digite a sua chave privada: ")
                private_key = []
                for i, x in enumerate(key):
                    if(x == ","):
                        private_key.append(int(key[1:i]))
                        private_key.append(int(key[(i+2):-1]))
                        break
                deciphered_text = rsa_decypher(int(msg), private_key)
                print("Essa é a mensagem decifrada:")
                print(deciphered_text)
        case "2":
            print("1 - Cifração em RSA-OAEP")
            print("2 - Decifração em RSA-OAEP")
            op = input("Digite sua escolha: ")
            if(op == "1"):
                print("---------------- CIFRAÇÃO -----------------")
                msg = input("Digite a mensagem que será cifrada: ")
                keys = generate_key_pair()
                print(f"CHAVE PÚBLICA: {keys['public']}")
                print(f"CHAVE PRIVADA: {keys['private']}")
                msg = convert_message(msg)
                ciphered_text = rsa_oaep_encode(msg, keys['public'])
                ciphered_text= ciphered_text.decode('ascii')
                print("Essa é a mensagem cifrada com o RSA-OAEP:")
                print(ciphered_text)
            else:
                print("---------------- DECIFRAÇÃO -----------------")
                msg = input("Digite a mensagem que será decifrada: ")
                msg = msg.encode('ascii')
                barray = base64.b64decode(msg)
                blocks = [barray[i:i+256] for i in range(0, len(barray), 256)]
                key = input("Digite a sua chave privada: ")
                private_key = []
                for i, x in enumerate(key):
                    if(x == ","):
                        private_key.append(int(key[1:i]))
                        private_key.append(int(key[(i+2):-1]))
                        break
                deciphered_text=rsa_oaep_decode(blocks, private_key)
                print("Essa é a mensagem decifrada:")
                print(deciphered_text)
    return