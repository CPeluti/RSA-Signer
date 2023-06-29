import random
import hashlib
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
    return random.getrandbits(bits).to_bytes(64, 'big')

def gen_message(message, size):
    m = message.encode('ascii')
    m = m+(size-len(m))*b'\0'
    return m

def hash(input):
    f = hashlib.sha3_512()
    f.update(input)
    return f.digest()

def xor(a,b):
    int_a=int.from_bytes(a,'big')
    int_b=int.from_bytes(b,'big')
    res = int_a^int_b
    return res.to_bytes(64,'big')

def oaep_encode(message):
    seed = generate_random_number(512)
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
    return db.decode('ascii', errors='ignore').strip("\0")

def rsa_decypher(cypher_text, private_key):
    d, n = private_key
    return pow(cypher_text, d, n)

def run():
    return
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
    
    # res = oaep_encode("teste")
    # res2= oaep_decode(res["maskedSeed"], res["maskedDB"])
    # print(res, res2)

    # print("Escolha o modo do RSA:")
    # print("1 - RSA")
    # print("2 - RSA-OAEP")
    # op = input("Digite sua escolha: ")
    # match op:
    #     case "1":
    #         print("1 - Cifração em RSA")
    #         print("2 - Decifração em RSA")
    #         op = input("Digite sua escolha: ")
    #         if(op == "1"):
    #             print("---------------- CIFRAÇÃO -----------------")
    #             msg = input("Digite a mensagem que será cifrada: ")
    #             p = genPrime()
    #             q = genPrime()
    #             e = 65537
    #             keys = genKey(p, q, e)
    #             print(f"CHAVE PÚBLICA: {keys[0]}")
    #             print(f"CHAVE PRIVADA: {keys[1]}")
    #             ciphered_text = rsa_cypher(int(msg), keys[0])
    #             print("Essa é a mensagem cifrada:")
    #             print(ciphered_text)
    #         else:
    #             print("---------------- DECIFRAÇÃO -----------------")
    #             msg = input("Digite a mensagem que será decifrada: ")
    #             key = input("Digite a sua chave privada: ")
    #             private_key = []
    #             for i, x in enumerate(key):
    #                 if(x == ","):
    #                     private_key.append(int(key[1:i]))
    #                     private_key.append(int(key[(i+2):-1]))
    #                     break
    #             deciphered_text = rsa_decypher(int(msg), private_key)
    #             print("Essa é a mensagem decifrada:")
    #             print(deciphered_text)
    #     case "2":
    #         print("1 - Cifração em RSA-OAEP")
    #         print("2 - Decifração em RSA-OAEP")
    #         op = input("Digite sua escolha: ")
    #         if(op == "1"):
    #             print("---------------- CIFRAÇÃO -----------------")
    #             msg = input("Digite a mensagem que será cifrada: ")
    #             p = genPrime()
    #             q = genPrime()
    #             e = 65537
    #             keys = genKey(p, q, e)
    #             print(f"CHAVE PÚBLICA: {keys[0]}")
    #             print(f"CHAVE PRIVADA: {keys[1]}")

    #             oaep_msg = oaep_encode(msg)
    #             oaep_msg_concat = int(str(int.from_bytes(oaep_msg["maskedSeed"], 'big'))+str(int.from_bytes(oaep_msg["maskedDB"], 'big')))
    #             ciphered_text = rsa_cypher(int(oaep_msg_concat), keys[0])
    #             print("Essa é a mensagem cifrada com o RSA-OAEP:")
    #             print(ciphered_text)
    #         else:
    #             # print("---------------- DECIFRAÇÃO -----------------")
    #             # msg = input("Digite a mensagem que será decifrada: ")
    #             # key = input("Digite a sua chave privada: ")
    #             msg = 140608373743894420094705076714598476334710525372947962204733899842824127165738020684550241980957906332284595668976685379863159325707337997364494384682937283627427749856803066272789693711656645104146493035849651747691248286854259041590216230902145852277432212539108245437589455477507823938250529052081526524919210011796828757794546726434449006105321938515623149484972402508549601228501701988315182417906467540981455093180863964147557517656506348099622157900642946461273711466130475656840466471951760249074465496441724844457300613929626232607950465469580757193613625414196282091716521278800174447601930583692618166811
    #             private_key = (204013194114180835160589151243792080938013903934521973798128225508967086790737718683860869580377652180532417068566201764037069171950223856945629424981234974919907466824586373536927571364981435975896684525179692430703777639490553972774452658043184855649449168915869186228652015001151035002148136417314324215712916407869212220385456193675444973954881018629938822333846839542664071576588823373614552405819103580528073092214476239900055021620132449688778017259071799525557897452253037002086664600929589280008776087194311248626494972737692014345669014744482765803591243927521528324008303212977667331679995226357233838593, 326044008551040513897764611906564611988748956841513036402846505930091103370185765445381140501590182182880243304297287480728087259122654626235020377121420126593005648977831573412251810489338382012103516721778713978517203354450166692199553839499029601168014782072749679522706962230063289624848381203217149486189008957909510516863725960694588135733142293948584097501860738570944386876932919723687828124645329430515444048080357377937017377588164392425620990636885108528441956177603756940427923160178771512166182594136359352469970702287425016577704021014055826844587431994247210948151024403553309041600017906870497308907)
    #             # for i, x in enumerate(key):
    #             #     if(x == ","):
    #             #         private_key.append(int(key[1:i]))
    #             #         private_key.append(int(key[(i+2):-1]))
    #             #         break
    #             deciphered_text = rsa_decypher(int(msg), private_key)
    #             deciphered_text = deciphered_text.to_bytes(128, byteorder = 'big')
    #             print(deciphered_text)
    #             deciphered_text = oaep_decode(deciphered_text[:63],deciphered_text[64:])
    #             print("Essa é a mensagem decifrada:")
    #             print(deciphered_text)
    # text_to_cypher = "attackatdawn"
    # p = genPrime()
    # q = genPrime()
    # e = 65537
    # keys = genKey(p, q, e)
    # oaep_msg = oaep_encode(text_to_cypher)
    # oaep_msg_concat = int(str(int.from_bytes(oaep_msg["maskedSeed"], 'big'))+str(int.from_bytes(oaep_msg["maskedDB"], 'big')))
    # ciphered_text = rsa_cypher(oaep_msg_concat, keys[0])
    # p_key = keys[1]
    # deciphered_text = rsa_decypher(ciphered_text, p_key)
    # print(len(str(deciphered_text)))
    # deciphered_text = deciphered_text.to_bytes(128, 'big')
    # deciphered_text = oaep_decode(deciphered_text[:63],deciphered_text[64:])
    # print(deciphered_text)
    # return