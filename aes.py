import random
import copy

Sbox = [    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

Rcon = [ 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36 ]

def xor(l1, l2):
    check1 = all(isinstance(l, list) for l in l1)
    check2 = all(isinstance(l, list) for l in l2)
    if(not (check1 and check2)):
        res = []
        for a, b in zip(l1, l2):
            res.append(a^b)
    else:
        res=[[], [], [], []]
        for i in range(4):
            for a, b in zip(l1[i], l2[i]):
                res[i].append(a^b)

    return res

def vec_to_matrix(v, size):
    matrix_keys = []
    while v != []:
        matrix_keys.append(v[:size])
        v = v[size:]
    return matrix_keys

# -------------- EXPANSÃO DA CHAVE -------------------------------#

def rot_word(last_v_keys):
    last_v_keys[1], last_v_keys[0] = last_v_keys[0], last_v_keys[1]
    last_v_keys[2], last_v_keys[1] = last_v_keys[1], last_v_keys[2]
    last_v_keys[3], last_v_keys[2] = last_v_keys[2], last_v_keys[3]
    return last_v_keys

def sub_word(rotated_v):
    check = all(isinstance(l, list) for l in rotated_v)
    if(not check):
        sub_v = []
        for b in rotated_v:
            sub_v.append(Sbox[b])
    else:
        sub_v=[[], [], [], []]
        for i in range(4):
            for b in rotated_v[i]:
                sub_v[i].append(Sbox[b])
    return sub_v

def key_expand(key):
    round_keys = []  # todas as round keys
    result_matrix = [[], [], [], []]
    temp = []
    rcon_var = 1
    key = key.to_bytes(16, byteorder = 'big')
    key_matrix = vec_to_matrix(list(key), 4)
    # round_keys.append(key_matrix[0]+key_matrix[1]+key_matrix[2]+key_matrix[3])
    round_keys.append(key_matrix)
    for i in range(0, 40):

        if(i % 4 == 0):
            if(i != 0):
                key_matrix=result_matrix
                # result_matrix = result_matrix[0]+result_matrix[1]+result_matrix[2]+result_matrix[3]
                round_keys.append(result_matrix) 
                result_matrix = [[], [], [], []]

            temp2=copy.deepcopy(key_matrix[3])
            rotated_v = rot_word(temp2)
            sub_v = sub_word(rotated_v)
            temp = xor(sub_v, [Rcon[rcon_var], 0, 0, 0])
            rcon_var+=1
            temp = xor(temp, key_matrix[0])
        else:
            temp = xor(temp, key_matrix[i%4])
        result_matrix[i%4]=temp

    # result_matrix = result_matrix[0]+result_matrix[1]+result_matrix[2]+result_matrix[3]
    round_keys.append(result_matrix) 
    return round_keys

# --------------------- CIFRAÇÃO ------------------------------ #
def addRoundKey(input, key):
    return xor(input, key)

def shiftRows(state):
    state[0][1], state[1][1], state[2][1], state[3][1] = state[1][1], state[2][1], state[3][1], state[0][1]
    state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
    state[0][3], state[1][3], state[2][3], state[3][3] = state[3][3], state[0][3], state[1][3], state[2][3]
    return state

def xtime(x):
    if(x & 0x80):
        return ((x << 1) ^ 0x1B) & 0xFF
    return x << 1

def mixAColumn(col):
    all_columns_xor = col[0] ^ col[1] ^ col[2] ^ col[3]
    col0 = col[0]
    col[0] ^= xtime(col[0] ^ col[1]) ^ all_columns_xor
    col[1] ^= xtime(col[1] ^ col[2]) ^ all_columns_xor
    col[2] ^= xtime(col[2] ^ col[3]) ^ all_columns_xor
    col[3] ^= xtime(col0 ^ col[3]) ^ all_columns_xor
    return col

def mixColumns(state):
    for i in range(4):
        state[i] = mixAColumn(state[i])
    return state

def cypher(input, round_keys):
    # round inicial
    input = input.to_bytes(16, byteorder = 'big')
    input = vec_to_matrix(list(input), 4)
    state = addRoundKey(input, round_keys[0]) 

    # rounds de 1 a 9
    for i in range(1, 10):
        state = sub_word(state)
        state = shiftRows(state)
        state = mixColumns(state)
        state = addRoundKey(state, round_keys[i])

    # ultimo round
    state = sub_word(state)
    state = shiftRows(state)
    state = addRoundKey(state, round_keys[10])

    return state

def run():
    key=random.randint(10**31, 2**128)
    key=00000000000000000000000000000000
    # input=00000101030307070f0f1f1f3f3f7f7f
    input=00000000000000000000000000000000

    round_keys = key_expand(key)
    cyphered_text = cypher(input, round_keys)
    # print(cyphered_text)
    # print(f"ROUND: {round_keys}")

