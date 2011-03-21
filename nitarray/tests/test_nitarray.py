from nose.tools import assert_equal, assert_raises

import bitarray as ba

from ..nitarray import nitarray
from StringIO import StringIO

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



def test_decode():
    n = nitarray('2,0,0,2,0', 3)
    assert_equal(n._bitarray, ba.bitarray('1000001000'))

    d = {'L': nitarray('2,0', 3), 
         'O': nitarray('0', 3),
         }

    decoded = n.decode(d)
    assert_equal(decoded, ['L', 'O', 'L'])

    d['L'] = nitarray('2,0', 42) 
    assert_raises(AssertionError, n.decode, d)



def test_encode():
    n = nitarray([], 3)

    d = {'L': nitarray('2,0', 3), 
         'O': nitarray('0', 3),
         }

    n.encode(d, 'LOL')
    assert_equal(n._bitarray, ba.bitarray('1000001000'))

    n.encode(d, 'LOL')
    assert_equal(n._bitarray, ba.bitarray('10000010001000001000'))

    d['I'] = nitarray('0,2', 42)
    assert_raises(AssertionError, n.encode, d, 'ILL')


def test_extend():
    n = nitarray([], 3)
    assert_equal(n._bitarray, ba.bitarray(''))

    n.extend([1, 2])
    assert_equal(n._bitarray, ba.bitarray('0110'))

    n.extend([0])
    assert_equal(n._bitarray, ba.bitarray('011000'))

    assert_raises(AssertionError, n.extend, [42])


def test_fromfile():
    f = StringIO("LOL")
    n = nitarray([], 2)
    n.fromfile(f)
    assert_equal(n._bitarray, ba.bitarray('010011000100111101001100'))

    f = StringIO("LOL")
    n = nitarray([], 3)
    n.fromfile(f)
    assert_equal(n._bitarray, ba.bitarray('000010100101000010101001000010100101'))


def test_fromstring():
    s = "LOL"
    n = nitarray([], 2)
    n.fromstring(s)
    assert_equal(n._bitarray, ba.bitarray('010011000100111101001100'))

    s = "LOL"
    n = nitarray([], 3)
    n.fromstring(s)
    assert_equal(n._bitarray, ba.bitarray('000010100101000010101001000010100101'))


def test_index():
    n = nitarray('2,0,0,2,0', 3)

    assert_equal(n.index(2), 0)
    assert_equal(n.index(0), 1)

    assert_raises(ValueError, n.index, 1)
    assert_raises(ValueError, n.index, 42)


def test_insert():
    n = nitarray([1], 3)
    assert_equal(n._bitarray, ba.bitarray('01'))

    n.insert(0, 0)
    assert_equal(n._bitarray, ba.bitarray('0001'))

    n.insert(1, 2)
    assert_equal(n._bitarray, ba.bitarray('001001'))

    n.insert(-1, 0)
    assert_equal(n._bitarray, ba.bitarray('00100001'))

    n.insert(-3, 2)
    assert_equal(n._bitarray, ba.bitarray('0010100001'))

    assert_raises(AssertionError, n.insert, 0, 42)
    assert_raises(AssertionError, n.insert, 42, 42)


def test_pop():
    n = nitarray('2,0,0,2,0', 3)
    assert_equal(n._bitarray, ba.bitarray('1000001000'))

    p = n.pop(0)
    assert_equal(p, 2)
    assert_equal(n._bitarray, ba.bitarray('00001000'))

    p = n.pop()
    assert_equal(p, 0)
    assert_equal(n._bitarray, ba.bitarray('000010'))

    p = n.pop(1)
    assert_equal(p, 0)
    assert_equal(n._bitarray, ba.bitarray('0010'))


def test_remove():
    n = nitarray('2,0,0,2,0', 3)
    assert_equal(n._bitarray, ba.bitarray('1000001000'))

    n.remove(0)
    assert_equal(n._bitarray, ba.bitarray('10001000'))

    n.remove(2)
    assert_equal(n._bitarray, ba.bitarray('001000'))

    n.append(1)
    assert_equal(n._bitarray, ba.bitarray('00100001'))

    n.remove(1)
    assert_equal(n._bitarray, ba.bitarray('001000'))


def test_setall():
    n = nitarray('2,0,0,2,0', 3)
    assert_equal(n._bitarray, ba.bitarray('1000001000'))

    n.setall(2)
    assert_equal(n._bitarray, ba.bitarray('1010101010'))

    n.setall(1)
    assert_equal(n._bitarray, ba.bitarray('0101010101'))

    n.setall(0)
    assert_equal(n._bitarray, ba.bitarray('0000000000'))

    assert_raises(AssertionError, n.setall, 42)


def test_sort():
    n = nitarray('2,0,1,2,0', 3)
    assert_equal(n._bitarray, ba.bitarray('1000011000'))

    n.sort()
    assert_equal(n._bitarray, ba.bitarray('0000011010'))

    n = nitarray('2,0,1,2,0', 3)
    n.sort(reverse=True)
    assert_equal(n._bitarray, ba.bitarray('1010010000'))
