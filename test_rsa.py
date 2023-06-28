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
def teste_oaep():
    assert rsa.oaep("teste","teste")