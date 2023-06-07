import aes
def test_key_expand():
    assert aes.key_expand(288081484012728429345163884354115083578)==[[216,186,121,196],[23,81,243,133],[74,67,254,78],[7,42,29,58]]

def test_vec_to_matrix():
    assert aes.vec_to_matrix([1, 2, 3, 4], 2) == [[1,2], [3, 4]]