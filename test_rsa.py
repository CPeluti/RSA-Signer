import rsa

def test_isPrime():
    assert rsa.isPrime(5,40) == True

def test_extendedEuclid():
    assert rsa.extendEuclid(35, 15) == (5, 1, -2)

def test_invertedModule():
    assert rsa.invertedModule(7, 108) == 31

def test_invertedModule2():
    assert rsa.invertedModule(13, 160) == 37

def test_genKey():
    assert rsa.genKey(17, 11, 13) == ((13, 187), (37, 187))

def test_genKey2():
    assert rsa.genKey(19, 7, 7) == ((7, 133), (31, 133))

def test_genKey3():
    assert rsa.genKey(5, 17, 11) == ((11, 85), (35, 85))

def test_oaep():
    x = "teste"
    e = rsa.oaep_encode(x)
    print(e)
    res = rsa.oaep_decode(e["maskedSeed"], e["maskedDB"])
    assert x == res
    
# def test_rsa():
#     p = rsa.genPrime()
#     q = rsa.genPrime()
#     e = 65537
#     keys = rsa.genKey(p, q, e)
#     msg = 8645

#     res = rsa.rsa_cypher(msg,keys[0])
#     deciphred_text = rsa.rsa_decypher(res,keys[1])
#     assert msg == deciphred_text

def test_rsa_oaep():
    p = rsa.genPrime()
    q = rsa.genPrime()
    e = 65537
    keys = rsa.genKey(p, q, e)
    msg = "attackatdawn"

    oaep_msg = rsa.oaep_encode(msg)
    deciphered_text = rsa.oaep_decode(oaep_msg['maskedSeed'], oaep_msg['maskedDB'])
    # print(len(oaep_msg["maskedSeed"]))
    # print(len(oaep_msg["maskedDB"]))
    # seed_int = int.from_bytes(oaep_msg["maskedSeed"], 'big')
    # db_int = int.from_bytes(oaep_msg["maskedDB"], 'big')
    oaep_bytes = bytearray(oaep_msg["maskedSeed"]) + bytearray(oaep_msg["maskedDB"])
    oaep_msg_concat = int.from_bytes(oaep_bytes, 'big')
    # 
    res = rsa.rsa_cypher(oaep_msg_concat,keys[0])
    deciphered_text = rsa.rsa_decypher(res,keys[1])
    msg_bytes = bytearray(deciphered_text.to_bytes(128, 'big'))
    
    # print((deciphered_text.bit_length() + 7)// 8) 
    deciphered_text = rsa.oaep_decode(msg_bytes[:64],msg_bytes[64:])
    assert msg==deciphered_text 