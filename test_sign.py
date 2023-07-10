import sign

def test_sign():
    msg = "AttackAtDawn"
    s = sign.sign(msg)
    v = sign.verify(s)
    assert v == True
