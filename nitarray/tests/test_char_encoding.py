from nose.tools import assert_equal

import bitarray as ba

from ..nitarray import char_encoding, nitarray


def test_char_encoding2():
    n = 2 
    ce = char_encoding(n)

    for key in ce:
        yield check_length, ce[key], 8

    assert_equal(len(ce), 256)


def test_char_encoding3():
    n = 3
    ce = char_encoding(n)

    for key in ce:
        yield check_length, ce[key], 6

    assert_equal(len(ce), 256)


def test_char_encoding8():
    n = 8
    ce = char_encoding(n)

    for key in ce:
        yield check_length, ce[key], 3

    assert_equal(len(ce), 256)


def test_char_encoding42():
    n = 42
    ce = char_encoding(n)

    for key in ce:
        yield check_length, ce[key], 2

    assert_equal(len(ce), 256)


def test_char_encoding256():
    n = 256
    ce = char_encoding(n)

    for key in ce:
        yield check_length, ce[key], 1

    assert_equal(len(ce), 256)


def test_char_encoding1337():
    n = 1337
    ce = char_encoding(n)

    for key in ce:
        yield check_length, ce[key], 1

    assert_equal(len(ce), 256)


def check_length(a, l):
    assert_equal(len(a), l)
