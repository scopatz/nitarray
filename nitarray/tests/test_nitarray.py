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




#
# Test general methods
# 

def test_append():
    n = nitarray([1, 2, 0], 3)
    nid = id(n)
    assert_equal(n._bitarray, ba.bitarray('011000'))

    n.append(1)
    assert_equal(id(n), nid)
    assert_equal(n._bitarray, ba.bitarray('01100001'))

    n.append('2')
    assert_equal(id(n), nid)
    assert_equal(n._bitarray, ba.bitarray('0110000110'))

    assert_raises(AssertionError, n.append, 42)
    

def test_count():
    n = nitarray([0, 2, 0], 3)
    assert_equal(n.count(0), 2)
    assert_equal(n.count(1), 0)
    assert_equal(n.count(2), 1)
    assert_equal(n.count(42), 0)



def test_extend():
    n = nitarray([], 3)
    assert_equal(n._bitarray, ba.bitarray(''))

    n.extend([1, 2])
    assert_equal(n._bitarray, ba.bitarray('0110'))

    n.extend([0])
    assert_equal(n._bitarray, ba.bitarray('011000'))

    assert_raises(AssertionError, n.extend, [42])
