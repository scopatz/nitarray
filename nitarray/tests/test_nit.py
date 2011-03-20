from nose.tools import assert_equal

from ..nitarray import nit


def test_nit2():
    for i in range(1000):
        yield check_bin, i


def check_bin(i):
    n = nit(i, 2)
    b = [int(c) for c in bin(i)[2:]]
    assert_equal(n, b)


def test_nit3():
    assert_equal(nit(2, 3), [2])
    assert_equal(nit(8, 3), [2, 2])
    assert_equal(nit(9, 3), [1, 0, 0])
    assert_equal(nit(25, 3), [2, 2, 1])
