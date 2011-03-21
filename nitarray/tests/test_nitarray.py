from StringIO import StringIO
from copy import copy, deepcopy

from nose.tools import assert_equal, assert_not_equal, assert_raises
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


def test_repr():
    n = nitarray([1, 0, 2, 2, 0], 3)
    r = repr(n)
    assert_equal(r, "nitarray('1,0,2,2,0', 3)")


def test_len():
    n = nitarray([1, 0, 2, 2, 0], 3)
    l = len(n)
    assert_equal(l, 5)

    n = nitarray([], 42)
    l = len(n)
    assert_equal(l, 0)


def test_add():
    x = nitarray('0,2,1', 3)
    y = nitarray('1', 3)

    z = x + y
    assert_equal(z._bitarray, ba.bitarray('00100101'))

    z = y + x
    assert_equal(z._bitarray, ba.bitarray('01001001'))

    q = nitarray(6, 42)
    assert_raises(AssertionError, x.__add__, q)

    z = x + [0]
    assert_equal(z._bitarray, ba.bitarray('00100100'))

    z = [2] + y
    assert_equal(z._bitarray, ba.bitarray('1001'))

    z = x + '0,2'
    assert_equal(z._bitarray, ba.bitarray('0010010010'))

    z = '1,1' + y
    assert_equal(z._bitarray, ba.bitarray('010101'))

    z = x + 3
    assert_equal(z._bitarray, ba.bitarray('001001000000'))

    z = 3 + y
    assert_equal(z._bitarray, ba.bitarray('00000001'))



def test_contains():
    n = nitarray('1,0', 3)

    assert (0 in n)
    assert (1 in n)
    assert (2 not in n)
    assert (42 not in n)


def test_copy():
    x = nitarray('0,2,1', 3)

    y = copy(x)
    assert_equal(x._n, y._n)
    assert_equal(x._bitarray, y._bitarray)
    assert_not_equal(id(x._bitarray), id(y._bitarray))
    assert_not_equal(id(x), id(y))

    y = deepcopy(x)
    assert_equal(x._n, y._n)
    assert_equal(x._bitarray, y._bitarray)
    assert_not_equal(id(x._bitarray), id(y._bitarray))
    assert_not_equal(id(x), id(y))


def test_delitem():
    n = nitarray('2,0,0,2,0', 3)
    assert_equal(n._bitarray, ba.bitarray('1000001000'))

    del n[0]
    assert_equal(n._bitarray, ba.bitarray('00001000'))

    del n[-1]
    assert_equal(n._bitarray, ba.bitarray('000010'))

    del n[1]
    assert_equal(n._bitarray, ba.bitarray('0010'))


def test_eq():
    x = nitarray('0,2,1', 3)
    y = nitarray('1', 3)
    z = nitarray('0,2,1,1', 3)

    assert (x == x)
    assert (y == y)
    assert (z == z)    

    assert (z == (x + y))

    y1 = nitarray('1', 4)
    assert not (y == y1)

    y2 = nitarray('1', 2)
    assert not (y == y2)


def test_ge():
    x = nitarray('0,2,1', 3)
    y = nitarray('1', 3)
    z = nitarray('0,2,1,1', 3)

    assert (y <= x)
    assert (y <= z)
    assert (x <= z)    
    assert (z <= (x + y))

    assert not (x <= y)
    assert not (z <= y)
    assert not (z <= x)    
    assert ((x + y) <= z)


def test_getitem():
    x = nitarray('0,2,1,1,0,0,2', 3)

    y = x[1:3]
    assert_equal(y._bitarray, ba.bitarray('1001'))

    y = x[0]
    assert_equal(y._bitarray, ba.bitarray('00'))

    y = x[2]
    assert_equal(y._bitarray, ba.bitarray('01'))

    y = x[-2]
    assert_equal(y._bitarray, ba.bitarray('00'))

    y = x[-1]
    assert_equal(y._bitarray, ba.bitarray('10'))

    y = x[-5:-2]
    assert_equal(y._bitarray, ba.bitarray('010100'))


def test_gt():
    x = nitarray('0,2,1', 3)
    y = nitarray('1', 3)
    z = nitarray('0,2,1,1', 3)

    assert (y < x)
    assert (y < z)
    assert (x < z)    
    assert not (z < (x + y))

    assert not (x < y)
    assert not (z < y)
    assert not (z < x)    
    assert not ((x + y) < z)



def test_hash():
    x = nitarray('0,2,1', 3)
    y = nitarray('1', 3)
    z = nitarray('0,2,1,1', 3)

    assert_equal(hash(x), hash(x._bitarray))
    assert_equal(hash(y), hash(y._bitarray))
    assert_equal(hash(z), hash(z._bitarray))


def test_iadd():
    x = nitarray('0,2,1', 3)
    y = nitarray('1', 3)

    x += y    
    assert_equal(x._bitarray, ba.bitarray('00100101'))

    y += x
    assert_equal(y._bitarray, ba.bitarray('0100100101'))


def test_imul():
    x = nitarray('0,2,1', 3)
    y = nitarray('1', 3)

    x *= 2
    assert_equal(x._bitarray, ba.bitarray('001001001001'))

    y *= 4
    assert_equal(y._bitarray, ba.bitarray('01010101'))


def test_iter():
    x = nitarray('0,2,1,1,0,2', 3)


    for i in x:
        assert_equal(i._n, 3)
        assert_equal(len(i), 1)

    l = [i.tolist()[0] for i in x]
    assert_equal(l, [0, 2, 1, 1, 0, 2])


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


def test_to01():
    n = nitarray('2,0,1,2,0', 3)
    s = n.to01()
    assert_equal(s, '2,0,1,2,0')


def test_tofile():
    f = StringIO()
    n = nitarray([], 2)
    n._bitarray = ba.bitarray('010011000100111101001100')
    n.tofile(f)
    assert_equal(f.getvalue(), "LOL")

    f = StringIO()
    n = nitarray([], 3)
    n._bitarray = ba.bitarray('000010100101000010101001000010100101')
    n.tofile(f)
    assert_equal(f.getvalue(), "LOL")


def test_tolist():
    n = nitarray('2,0,1,2,0', 3)
    l = n.tolist()
    assert_equal(l, [2, 0, 1, 2, 0])


def test_tostring():
    n = nitarray([], 2)
    n._bitarray = ba.bitarray('010011000100111101001100')
    s = n.tostring()
    assert_equal(s, "LOL")

    n = nitarray([], 3)
    n._bitarray = ba.bitarray('000010100101000010101001000010100101')
    s = n.tostring()
    assert_equal(s, "LOL")
