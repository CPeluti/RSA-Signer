import aes
def test_key_expand():
    assert aes.key_expand(00000000000000000000000000000000)==[[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 
                                                              [[98, 99, 99, 99], [98, 99, 99, 99], [98, 99, 99, 99], [98, 99, 99, 99]], 
                                                              [[155, 152, 152, 201], [249, 251, 251, 170], [155, 152, 152, 201], [249, 251, 251, 170]], 
                                                              [[144, 151, 52, 80], [105, 108, 207, 250], [242, 244, 87, 51], [11, 15, 172, 153]], 
                                                              [[238, 6, 218, 123], [135, 106, 21, 129], [117, 158, 66, 178], [126, 145, 238, 43]], 
                                                              [[127, 46, 43, 136], [248, 68, 62, 9], [141, 218, 124, 187], [243, 75, 146, 144]], 
                                                              [[236, 97, 75, 133], [20, 37, 117, 140], [153, 255, 9, 55], [106, 180, 155, 167]], 
                                                              [[33, 117, 23, 135], [53, 80, 98, 11], [172, 175, 107, 60], [198, 27, 240, 155]], 
                                                              [[14, 249, 3, 51], [59, 169, 97, 56], [151, 6, 10, 4], [81, 29, 250, 159]], 
                                                              [[177, 212, 216, 226], [138, 125, 185, 218], [29, 123, 179, 222], [76, 102, 73, 65]], 
                                                              [[180, 239, 91, 203], [62, 146, 226, 17], [35, 233, 81, 207], [111, 143, 24, 142]]]

def test_vec_to_matrix():
    assert aes.vec_to_matrix([1, 2, 3, 4], 2) == [[1,2], [3, 4]]

def test_rot_word():
    assert aes.rot_word([1, 2, 3, 4]) == [2, 3, 4, 1]

# def test_shiftRows():
    # assert aes.shiftRows([[144, 151, 52, 80], [105, 108, 207, 250], [242, 244, 87, 51], [11, 15, 172, 153]]) == [[144, 108, 87, 153], [151, 207, 51, 11], [52, 250, 242, 15], [80, 105, 244, 172]]

def test_cypher():
    assert aes.cypher(00000000000000000000000000000000, [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 
                                                              [[98, 99, 99, 99], [98, 99, 99, 99], [98, 99, 99, 99], [98, 99, 99, 99]], 
                                                              [[155, 152, 152, 201], [249, 251, 251, 170], [155, 152, 152, 201], [249, 251, 251, 170]], 
                                                              [[144, 151, 52, 80], [105, 108, 207, 250], [242, 244, 87, 51], [11, 15, 172, 153]], 
                                                              [[238, 6, 218, 123], [135, 106, 21, 129], [117, 158, 66, 178], [126, 145, 238, 43]], 
                                                              [[127, 46, 43, 136], [248, 68, 62, 9], [141, 218, 124, 187], [243, 75, 146, 144]], 
                                                              [[236, 97, 75, 133], [20, 37, 117, 140], [153, 255, 9, 55], [106, 180, 155, 167]], 
                                                              [[33, 117, 23, 135], [53, 80, 98, 11], [172, 175, 107, 60], [198, 27, 240, 155]], 
                                                              [[14, 249, 3, 51], [59, 169, 97, 56], [151, 6, 10, 4], [81, 29, 250, 159]], 
                                                              [[177, 212, 216, 226], [138, 125, 185, 218], [29, 123, 179, 222], [76, 102, 73, 65]], 
                                                              [[180, 239, 91, 203], [62, 146, 226, 17], [35, 233, 81, 207], [111, 143, 24, 142]]]) == [[102, 233, 75, 212], [239, 138, 44, 59], [136, 76, 250, 89], [202, 52, 43, 46]]
    
def test_sub_word():
    assert aes.sub_word([[198, 228, 228, 139], [164, 135, 135, 232], [198, 228, 228, 139], [164, 135, 135, 232]]) == [[180, 105, 105, 61], [73, 23, 23, 155], [180, 105, 105, 61], [73, 23, 23, 155]]