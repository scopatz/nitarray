import math

import bitarray as ba


encodings_cache = {}
char_bin_encodings = {chr(i): ba.bitarray('{0:0>8}'.format(bin(i)[2:])) for i in range(256)}


def nit_encoding(n):
    """Generates a bit encoding dictionary for nits of base n."""
    # Find the number of bits that it will 
    # take to represent a single nit
    nit_bin_len = len(bin(n-1)) - 2

    ne = {i: ba.bitarray('{b:0>{l}}'.format(b=bin(i)[2:], l=nit_bin_len)) for i in range(n)}
    return ne


class nitarray(ba.bitarray):

    def __init__(self, initial, n=2):
        """Creates an array of nits.  A nit is a generalized bit.  Rather than being
        base 2, they instead have base n.
        """
        self._n = n
        self._allowed = set(range(n))

        if n not in encodings_cache:
            encodings_cache[n] = nit_encoding(n)
