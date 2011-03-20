from nose.tools import assert_equal

import bitarray as ba

from ..nitarray import nit_encoding


def test_nit_array1():
    n = 2 
    ne = nit_encoding(n)

    expected = {0: ba.bitarray('0'),
                1: ba.bitarray('1'),
                }

    assert_equal(ne, expected)
