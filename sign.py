import  aes
import rsa
import base64
import hashlib
def sign(msg):
    aes_k = aes.cipher(msg)[0].to_bytes(32, 'big')
    
    # keys = rsa.generate_key_pair()
    # print(keys)
    private = (65537, 29821469956828750595568607200332435872239627472969813551166932891370912679541796837550801074724387822812268435755530486122582049330887134530187804551455800795734074858831184252651091075387601259986871632212064356624231976782455726191923306138006105731958817844226327786878430986968786636231325663002041988825171610764741060744145108463575243281291861204465284056870636647863762560142906021116398886306214357369399989946297148887341375306825367687505618769492400624751768824612736381541576901044153773884200623346220924564660209326060136928027666739644598823159765642202689593181023169966438613524487849286842024647947)
    public = (25436321018458689874304364595550348127900196465187795863561523240728657381118855657401006760716744423687471284293363354658472871165854262786479366990041949806697511094628426686042937441661457046145934727568463578364810221739464349819621172972741219622755053137803862295901617287510187725488366946332821874289451403647286406110973570312655204410671836552567096624724951792563833739732839099684000151927460573809778395712074255279988656781392991059498483601246815077820846107503605398511416174883981357508258422991504364543118970523643788340450298267917531270915185687336432534155015080476537623059768502497163325656673, 29821469956828750595568607200332435872239627472969813551166932891370912679541796837550801074724387822812268435755530486122582049330887134530187804551455800795734074858831184252651091075387601259986871632212064356624231976782455726191923306138006105731958817844226327786878430986968786636231325663002041988825171610764741060744145108463575243281291861204465284056870636647863762560142906021116398886306214357369399989946297148887341375306825367687505618769492400624751768824612736381541576901044153773884200623346220924564660209326060136928027666739644598823159765642202689593181023169966438613524487849286842024647947)
    keys = {"public": public, "private": private}
    f = hashlib.sha3_512()
    f.update(aes_k)
    aes_h = f.digest()
    b64 = base64.b64encode(aes_h).decode('ascii')
    # print(len(aes_h.decode('ISO-8859-1')))
    # print(int(aes_h).to_bytes(64, 'big'))
    x = rsa.convert_message(b64)
    # print(x)
    rsa_ka_s = rsa.rsa_oaep_encode(x, keys['private'])
    return (b64, rsa_ka_s, keys['public'])

def verify(assig):
    aes_k, rsa_ka_s, key_p = assig
    barray = base64.b64decode(rsa_ka_s)
    blocks = [barray[i:i+256] for i in range(0, len(barray), 256)]
    rsa_ka_p = rsa.rsa_oaep_decode(blocks, key_p)

    return aes_k == rsa_ka_p



def run():
    msg = 'attackatdawn'
    
    signature = sign(msg)
    print(signature)
    is_assig = verify(signature)

    # print(is_assig)

    return
