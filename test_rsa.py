import rsa
import base64
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
    msg = "teste"
    x = msg.encode('ascii')
    x = base64.b64encode(x)
    e = rsa.oaep_encode(x)
    res = rsa.oaep_decode(e["maskedSeed"], e["maskedDB"])
    assert msg == res
    
def test_rsa():
    private = (65537, 29821469956828750595568607200332435872239627472969813551166932891370912679541796837550801074724387822812268435755530486122582049330887134530187804551455800795734074858831184252651091075387601259986871632212064356624231976782455726191923306138006105731958817844226327786878430986968786636231325663002041988825171610764741060744145108463575243281291861204465284056870636647863762560142906021116398886306214357369399989946297148887341375306825367687505618769492400624751768824612736381541576901044153773884200623346220924564660209326060136928027666739644598823159765642202689593181023169966438613524487849286842024647947)
    public = (25436321018458689874304364595550348127900196465187795863561523240728657381118855657401006760716744423687471284293363354658472871165854262786479366990041949806697511094628426686042937441661457046145934727568463578364810221739464349819621172972741219622755053137803862295901617287510187725488366946332821874289451403647286406110973570312655204410671836552567096624724951792563833739732839099684000151927460573809778395712074255279988656781392991059498483601246815077820846107503605398511416174883981357508258422991504364543118970523643788340450298267917531270915185687336432534155015080476537623059768502497163325656673, 29821469956828750595568607200332435872239627472969813551166932891370912679541796837550801074724387822812268435755530486122582049330887134530187804551455800795734074858831184252651091075387601259986871632212064356624231976782455726191923306138006105731958817844226327786878430986968786636231325663002041988825171610764741060744145108463575243281291861204465284056870636647863762560142906021116398886306214357369399989946297148887341375306825367687505618769492400624751768824612736381541576901044153773884200623346220924564660209326060136928027666739644598823159765642202689593181023169966438613524487849286842024647947)
    keys = {"public": public, "private": private}
    msg = 8645

    res = rsa.rsa_cypher(msg,keys["public"])
    deciphred_text = rsa.rsa_decypher(res,keys["private"])
    assert msg == deciphred_text

def test_rsa_oaep():
    private = (65537, 29821469956828750595568607200332435872239627472969813551166932891370912679541796837550801074724387822812268435755530486122582049330887134530187804551455800795734074858831184252651091075387601259986871632212064356624231976782455726191923306138006105731958817844226327786878430986968786636231325663002041988825171610764741060744145108463575243281291861204465284056870636647863762560142906021116398886306214357369399989946297148887341375306825367687505618769492400624751768824612736381541576901044153773884200623346220924564660209326060136928027666739644598823159765642202689593181023169966438613524487849286842024647947)
    public = (25436321018458689874304364595550348127900196465187795863561523240728657381118855657401006760716744423687471284293363354658472871165854262786479366990041949806697511094628426686042937441661457046145934727568463578364810221739464349819621172972741219622755053137803862295901617287510187725488366946332821874289451403647286406110973570312655204410671836552567096624724951792563833739732839099684000151927460573809778395712074255279988656781392991059498483601246815077820846107503605398511416174883981357508258422991504364543118970523643788340450298267917531270915185687336432534155015080476537623059768502497163325656673, 29821469956828750595568607200332435872239627472969813551166932891370912679541796837550801074724387822812268435755530486122582049330887134530187804551455800795734074858831184252651091075387601259986871632212064356624231976782455726191923306138006105731958817844226327786878430986968786636231325663002041988825171610764741060744145108463575243281291861204465284056870636647863762560142906021116398886306214357369399989946297148887341375306825367687505618769492400624751768824612736381541576901044153773884200623346220924564660209326060136928027666739644598823159765642202689593181023169966438613524487849286842024647947)
    keys = {"public": public, "private": private}
    msg = "attackatdawn"
    x = msg.encode('ascii')
    x = base64.b64encode(x)
    cipher = rsa.rsa_oaep_encode(x, keys["public"])

    assert msg==rsa.rsa_oaep_decode(cipher,keys["private"]) 