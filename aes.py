import random
def vec_to_matrix(v, size):
    matrix_keys = []
    while v != []:
        matrix_keys.append(v[:size])
        v = v[size:]
    return matrix_keys      

def key_expand(key):
    key = key.to_bytes(16, byteorder = 'big')
    matrix_keys = vec_to_matrix(list(key), 4)
    return matrix_keys

def run():
    key=random.randint(10**31, 2**128)
    round_keys = key_expand(key)
