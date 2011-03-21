import math

import bitarray as ba


encodings_cache = {}
char_bin_encodings = {chr(i): ba.bitarray('{0:0>8}'.format(bin(i)[2:])) for i in range(256)}


def nit(x, n):
    """Converts an int x to a sequence of nits of base n."""
    # Special case zero, do avoid log issues
    if x == 0:
        return [0]

    # Init variables
    l = []
    e = 1

    s = 0
    S = int(math.ceil(math.log(x, n)))

    # Loop through all powers of n 
    while s < S:
        d = (x // e) % n
        l.append(d)

        # Prep for next iter
        e = e*n
        s += 1

    # Get to the next order of mag, if x is a power of n
    if (x == e):
        l.append(1)

    # Put the nits in the proper order
    l.reverse()
    return l


def nit_encoding(n):
    """Generates a bit encoding dictionary for nits of base n."""
    # Find the number of bits that it will 
    # take to represent a single nit
    nit_bin_len = len(bin(n-1)) - 2

    # Generate encoding dictionaries
    ne = {i: ba.bitarray('{b:0>{l}}'.format(b=bin(i)[2:], l=nit_bin_len)) for i in range(n)}
    return ne


def char_encoding(n):
    """Generates a char encoding dictionary to nits of base n."""
    # Find the number of nits that it will 
    # take to represent all 256 characters
    nit_len = math.log(256, n)
    nit_len = math.ceil(nit_len)
    nit_len = int(nit_len)

    # Create char encoding map
    ce = {}
    for i in range(256):
        ce_i = [0 for nl in range(nit_len)]
        char_nit = nit(i, n)
        ce_i[-len(char_nit):] = char_nit
        ce[chr(i)] = nitarray(ce_i, n)

    return ce


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

        # Sets the length of the nit
        self._bits_per_nit = encodings_cache[self._n][0].length()

        # Create underlying bit array
        self._bitarray = ba.bitarray()
        self._bitarray.encode(encodings_cache[n], initial)


    def __repr__(self):
        decoded = self._bitarray.decode(encodings_cache[self._n])
        decoded = ",".join([str(i) for i in decoded])
        r = "nitarray('{na}', {n})".format(na=decoded, n=self._n)
        return r


    def __str__(self):
        s = self.__repr__()
        return s


    def __len__(self):
        l_this_array = self._bitarray.length()
        l = l_this_array / self._bits_per_nit
        return l

    #
    # General methods
    # 

    def append(self, x):
        """Appends the nit x to the end of the array."""
        x = int(x)
        assert (x in self._allowed_nits)
        x_array = encodings_cache[self._n][x]
        self._bitarray += x_array

    
    def count(self, x):
        """Counts the number of times the nit x appears in the array."""
        x = int(x)

        if x not in self._allowed_nits:
            c = 0
        else:
            d = self._bitarray.decode(encodings_cache[self._n])
            c = d.count(x)

        return c


    def decode(self, code):
        """Translates the nitarray into a list of keys of code.

        Args:
            * code: a dict of keys (any hashable object) to a nitarray.
              These nitarrays must have the same base as the nitarray
              to be extended.

        Returns:
            * decoded: a list of code keys, in the order they appear
              in the nitarray.
        """
        # Ensure that nitarrays are of the correct base
        for key in code:
            assert (self._n == code[key]._n)

        # Perform decoding 
        bit_code = {key: value._bitarray for key, value in code.items()}
        decoded = self._bitarray.decode(bit_code)
        return decoded


    def encode(self, code, seq):
        """Extends the nitarray with [code[s] for all s in seq].

        Args:
            * code: a dict of keys (any hashable object) to a nitarray.
              These nitarrays must have the same base as the nitarray
              to be extended.
            * seq: a sequence of keys present in code.
        """
        # Ensure that nitarrays are of the correct base
        for key in code:
            assert (self._n == code[key]._n)

        # Create temp seq_encoding
        seq_array = ba.bitarray()
        for s in seq:
            seq_array += code[s]._bitarray

        # Extend the current bitarray
        self._bitarray += seq_array


    def extend(self, seq):
        """Appends a sequence of nits to the nitarray."""
        assert (set(seq) <= self._allowed_nits)

        seq_array = ba.bitarray()
        seq_array.encode(encodings_cache[self._n], seq)
        self._bitarray += seq_array


    def fromfile(self, f):
        """Extends the nitarray with values from a file f."""
        # Allow f to be a path to a file or a file object
        opened_here = False
        if isinstance(f, basestring):
            f = open(f, 'r')
            opened_here = True

        # Get the contents of the file
        s = f.read()

        # Close the file if f was initially a path
        if opened_here:
            f.close()

        # Ensure that this char encoding is available
        if ('char', self._n) not in encodings_cache:
            encodings_cache['char', self._n] = char_encoding(self._n)

        # Encode this file as nits and extend the current bitarray
        self.encode(encodings_cache['char', self._n], s)       


    def fromstring(self, s):
        """Extend the nitarray from a string interpreting the characters 
        as nitarrays themselves."""
        # Ensure that this char encoding is available
        if ('char', self._n) not in encodings_cache:
            encodings_cache['char', self._n] = char_encoding(self._n)

        # Encode this string as nits and extend the current bitarray
        self.encode(encodings_cache['char', self._n], s)       


    def index(self, x):
        """Returns the index of the first occurence of x.  
        Raises an error if x does not occur in the nitarray."""
        decoded = self._bitarray.decode(encodings_cache[self._n])

        try:
            idx = decoded.index(x)
        except ValueError:
            msg = "{0} does not occur in {1}.".format(x, self)
            raise ValueError(msg)

        return idx


    def insert(self, i, x):
        """Inserts the nit x before position i in the array."""
        assert (x in self._allowed_nits)

        # Init prefix
        ba_i = i * self._bits_per_nit
        temp_bitarray = ba.bitarray(self._bitarray[:ba_i])

        # Append nit
        temp_bitarray += encodings_cache[self._n][x]

        # Append rest of original array
        temp_bitarray += self._bitarray[ba_i:]

        # Replace bitarray in-place
        self._bitarray = temp_bitarray


    def pop(self, i=-1):
        """Removes a nit from position i of the array and returns its value."""
        # Find indices
        if i < 0:
            i = self.__len__() + i
        ba_i = i * self._bits_per_nit
        ba_j = ba_i + self._bits_per_nit

        # calulated the popped value
        popped_bitarray = ba.bitarray(self._bitarray[ba_i:ba_j])
        decoded = popped_bitarray.decode(encodings_cache[self._n])
        print ba_i, ba_j, popped_bitarray
        p = decoded[0]

        # Temp. pop the bits from the underlying array
        temp_bitarray = ba.bitarray(self._bitarray[:ba_i])
        temp_bitarray += self._bitarray[ba_j:]

        # Replace bitarray in-place
        self._bitarray = temp_bitarray

        return p        


    def remove(self, x):
        """Removes the first occurence of the nit x in the array."""
        # Find indices
        i = self.index(x)
        ba_i = i * self._bits_per_nit
        ba_j = ba_i + self._bits_per_nit

        # Construct temporary array
        temp_bitarray = ba.bitarray(self._bitarray[:ba_i])
        temp_bitarray += self._bitarray[ba_j:]

        # Replace bitarray in-place
        self._bitarray = temp_bitarray


    def setall(self, x):
        """Sets all nits in the array to x."""
        assert (x in self._allowed_nits)

        xnit = encodings_cache[self._n][x]

        # Initialize indices
        i = -self._bits_per_nit
        j = 0
        J = self._bitarray.length()

        # set all nits
        while j != J:
            i += self._bits_per_nit
            j += self._bits_per_nit

            self._bitarray[i:j] = xnit


    def sort(self, reverse=False):
        """Sorts the nitarray in-place.  The reverse keyword reverses this sort."""
        # Decode the array and sort in integer space
        decoded = self._bitarray.decode(encodings_cache[self._n])
        decoded.sort(reverse=reverse)

        # Create a temp array that is sorted
        temp_bitarray = ba.bitarray()
        temp_bitarray.encode(encodings_cache[self._n], decoded)

        # Replace the bitarray in-place
        self._bitarray = temp_bitarray


    def to01(self):
        """Returns the nitarray to as a comma-separated string of ints cooresponding to the nits."""
        l = self.tolist()
        s = ",".join([str(i) for i in l])
        return s


    def tofile(self, f):
        """Writes the nitarray to a file f, interpreting the nits as characters."""
        # Ensure that this char encoding is available
        if ('char', self._n) not in encodings_cache:
            encodings_cache['char', self._n] = char_encoding(self._n)

        # Decode this nitarray as characters and make into a string
        decoded = self.decode(encodings_cache['char', self._n])
        s = "".join(decoded)

        # Allow f to be a path to a file or a file object
        opened_here = False
        if isinstance(f, basestring):
            f = open(f, 'a')
            opened_here = True

        # Write the string rep to the file.
        f.write(s)

        # Close the file if f was initially a path
        if opened_here:
            f.close()


    def tolist(self):
        """Returns the nitarray to as a list of ints cooresponding to the nits."""
        # Decode this nitarray
        decoded = self._bitarray.decode(encodings_cache[self._n])
        return decoded


    def tostring(self):
        """Returns the nitarray to as a string, interpreting the nits as characters."""
        # Ensure that this char encoding is available
        if ('char', self._n) not in encodings_cache:
            encodings_cache['char', self._n] = char_encoding(self._n)

        # Decode this nitarray as characters and make into a string
        decoded = self.decode(encodings_cache['char', self._n])
        s = "".join(decoded)

        return s
        
