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
    m = message.encode('ISO-8859-1')
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
    return db.decode('ISO-8859-1').strip('\0')

def rsa_decypher(cypher_text, private_key):
    d, n = private_key
    return pow(cypher_text, d, n)

def run():
    # return
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
                p = genPrime()
                q = genPrime()
                e = 65537
                keys = genKey(p, q, e)
                print(f"CHAVE PÚBLICA: {keys[0]}")
                print(f"CHAVE PRIVADA: {keys[1]}")
                ciphered_text = rsa_cypher(int(msg), keys[0])
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
                p = genPrime()
                q = genPrime()
                e = 65537
                keys = genKey(p, q, e)
                print(f"CHAVE PÚBLICA: {keys[0]}")
                print(f"CHAVE PRIVADA: {keys[1]}")

                oaep_msg = oaep_encode(msg)
                oaep_msg_concat = int(str(int.from_bytes(oaep_msg["maskedSeed"], 'big'))+str(int.from_bytes(oaep_msg["maskedDB"], 'big')))
                ciphered_text = rsa_cypher(int(oaep_msg_concat), keys[0])
                print("Essa é a mensagem cifrada com o RSA-OAEP:")
                print(ciphered_text)
            else:
                # print("---------------- DECIFRAÇÃO -----------------")
                # msg = input("Digite a mensagem que será decifrada: ")
                # key = input("Digite a sua chave privada: ")
                msg = 157424687759212365244449020441756603996495792562463331873565666862269210829336310368675072318566802286040951539774510533085025222017962019643207312959154723848370323747785384195428573163269244489060088306689297865417774968314864631925461011753200625533284602791855788796723320275672774226829822359725954102090729603986019211800337703858629000432921010996055253234440737123492286402151805090879988547682709362899852492321274394475799398295626214934358669865356340083732408708696513641470850113840929507273396650170329574109850400476201164086251927123238836474217927900261134011052222125358971842365779162011192292427
                private_key = (714164357447161594623214466293478900096848804199480026143331895587810368805153926721168253762277530020018292172443763978362483560675855225739433118752378755242103411362717975414838571766755559854478018813266474600314936769811909223415615741635697082540656311829771057804523300629687293274020106100485513070094028455528410924365365768637848403013338139543419781682644082543427545965483252604699644341703671446328419415970941516741746274247762460471889572052167481583454239678541238021332043166365525763059428730016518639992870474227216239375158926907045402421500872080603782653170134137306805287160491829967487670273, 2192028357718931689154252832403321781362269580405644551955579919498797683607314204548763762027837321324556894628392982383380577234732742784249027177954039269497083705061748218188566667191731881143823806620693375134921319365078826094744717537447484062311118054907629534251360226366046091199862106290161065477629369405254833663691739389025231258674092235484327650796186479766353253316903410281994552526130369178580016558632024410396253251702235915334916023111757116898441903715520343386957265968599732878259881197841928328896341190271322549853690666577819549041719028633240879241335455817056377177015437675574527132761)
                # private_key = []
                # for i, x in enumerate(key):
                #     if(x == ","):
                #         private_key.append(int(key[1:i]))
                #         private_key.append(int(key[(i+2):-1]))
                #         break
                deciphered_text = rsa_decypher(int(msg), private_key)
                deciphered_text = deciphered_text.to_bytes(128, byteorder = 'big')
                print(deciphered_text)
                deciphered_text = oaep_decode(deciphered_text[:63],deciphered_text[64:])
                print("Essa é a mensagem decifrada:")
                print(deciphered_text)

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
    return