import math

import bitarray as ba


encodings_cache = {}
char_bin_encodings = {chr(i): ba.bitarray('{0:0>8}'.format(bin(i)[2:])) for i in range(256)}


def nit_encoding(n):
    """Generates a bit encoding dictionary for nits of base n."""
    # Find the number of bits that it will 
    # take to represent a single nit
    nit_bin_len = len(bin(n-1)) - 2

    # Generate encoding dictionaries
    ne = {i: ba.bitarray('{b:0>{l}}'.format(b=bin(i)[2:], l=nit_bin_len)) for i in range(n)}
    return ne


class nitarray(object):

    def __init__(self, initial, n=2):
        """Creates an array of nits.  A nit is a generalized bit.  Rather than being
        base 2, they instead have base n.

        Args:
            * initial: Initial value of the nitarray. Behavior determined by type:

                * iterable of ints: nit values in sequence.  
                * string: nit values reprensted as a string.
                  Here nits must be separated by commas.
                * int or long: creates a zero array of the length given.

            * n (int): nit base.

        All nits must be on the range [0, n-1].        
        """
        self._n = n

        # Turn initial string types into appropriate list
        if isinstance(initial, basestring):
            initial = [int(i) for i in initial.split(',')]

        # Turn initial int or long types into approriate lis
        if isinstance(initial, int) or isinstance(initial, long):
            initial = [0] * initial

        # Ensure that the initial value contains only valid nits        
        self._allowed_nits = set(range(n))
        assert (set(initial) <= self._allowed_nits)

        # Ensure that this nit encoding is available
        if n not in encodings_cache:
            encodings_cache[n] = nit_encoding(n)

        # Create underlying bit array
        self._bitarray = ba.bitarray()
        self._bitarray.encode(encodings_cache[n], initial)


    #
    # General methods
    # 

    def append(self, x):
        """Appends the nit x to the end of the array."""
        x = int(x)
        assert (x in self._allowed_nits)
        x_array = encodings_cache[self._n][x]
        self._bitarray = self._bitarray + x_array
