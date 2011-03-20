from nose.tools import assert_equal, assert_raises

import bitarray as ba

from ..nitarray import nitarray

#
# Test init method
#

def test_nit_array_init2():
    # Iterable init
    n = nitarray([1, 0, 1, 1], 2)
    assert_equal(n._n, 2)
    assert_equal(n._allowed_nits, set([0, 1]))
    assert_equal(n._bitarray, ba.bitarray('1011'))

    # String init
    n = nitarray('1,0,1,1', 2)
    assert_equal(n._n, 2)
    assert_equal(n._allowed_nits, set([0, 1]))
    assert_equal(n._bitarray, ba.bitarray('1011'))

    # Zeros init
    n = nitarray(3, 2)
    assert_equal(n._n, 2)
    assert_equal(n._allowed_nits, set([0, 1]))
    assert_equal(n._bitarray, ba.bitarray('000'))

    # Confirm valid inits
    assert_raises(AssertionError, nitarray, [0, 1, 42], n=2)


def test_nit_array_init3():
    # Iterable init
    n = nitarray([1, 0, 2, 2, 0], 3)
    assert_equal(n._n, 3)
    assert_equal(n._allowed_nits, set([0, 1, 2]))
    assert_equal(n._bitarray, ba.bitarray('0100101000'))

    # String init
    n = nitarray('1,0,2,2,0', 3)
    assert_equal(n._n, 3)
    assert_equal(n._allowed_nits, set([0, 1, 2]))
    assert_equal(n._bitarray, ba.bitarray('0100101000'))

    # Zeros init
    n = nitarray(3, 3)
    assert_equal(n._n, 3)
    assert_equal(n._allowed_nits, set([0, 1, 2]))
    assert_equal(n._bitarray, ba.bitarray('000000'))

    # Confirm valid inits
    assert_raises(AssertionError, nitarray, [0, 1, 42], n=2)

