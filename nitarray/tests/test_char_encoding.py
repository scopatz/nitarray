from nose.tools import assert_equal

import bitarray as ba

from ..nitarray import char_encoding, nitarray


def test_char_encoding2():
    n = 2 
    ce = char_encoding(n)
    print ce
    raise TypeError

    expected = {0: ba.bitarray('0'),
                1: ba.bitarray('1'),
                }

    assert_equal(ne, expected)

"""\
def test_nit_encoding3():
    n = 3 
    ne = nit_encoding(n)

    expected = {0: ba.bitarray('00'),
                1: ba.bitarray('01'),
                2: ba.bitarray('10'),
                }

    assert_equal(ne, expected)


def test_nit_encoding8():
    n = 8
    ne = nit_encoding(n)

    expected = {0: ba.bitarray('000'),
                1: ba.bitarray('001'),
                2: ba.bitarray('010'),
                3: ba.bitarray('011'),
                4: ba.bitarray('100'),
                5: ba.bitarray('101'),
                6: ba.bitarray('110'),
                7: ba.bitarray('111'),
                }

    assert_equal(ne, expected)
"""\
