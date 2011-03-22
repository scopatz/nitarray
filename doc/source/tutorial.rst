========
Tutorial
========
Computers function based on arrays of bits.  Physically, this is the state of a transitor or 
some other device that can be measured to have a clear voltage difference between two levels.
In software, we represent the on and off states by 1 and 0 (our bits). 

--------------
What is a nit?
--------------
A nit is very similar to a bit except that is of base-n, rather than base-2.  So as bit can be 
represented by [0, 1], a nit (base-n) may be any interger [0, 1, 2, ..., n-1].  In fact, bits 
are simply a special case of nits!  Many of the following examples will use base-3 nits, 
sometimes known as `trits`_.

Any integer may be converted to a nit-representation using the :func:`nit() <nitarray.nit>`
function.  This function takes x, the number to convert, and the base to cast it into.
It returns a list of nits that are the base-n digits of x.
(Note that the term 'nit' is a not-so-clever anagram of 'int'.)

.. code-block:: ipython

   In [1]: from nitarray import nit

   In [2]: nit(10, 3)
   Out[2]: [1, 0, 1]

   In [3]: nit(1794864036260549376542, 42)
   Out[3]: [1L, 17L, 24L, 0L, 20L, 37L, 22L, 15L, 16L, 20L, 26L, 19L, 34L, 14L]

   In [4]: nit(16, 2)
   Out[4]: [1, 0, 0, 0, 0]

   In [5]: nit(101, 256)
   Out[5]: [101]

As you can see, because of python's native long support you can go a bit crazy with the
nits that you represent.  

You can read the above nits the same way you read base-10 numbers.  The last element is the 
n^0 place, the second to last element is the n^1 place, and so until you get the front of 
the list which is the n^(length - 1) place.

Reversing the 10-base-3 example above, we see that the last element is 1 so we start a running
tally with 1 as the initial value.  The second to last element is 0, so we don't add anything to 
our tally.  The third-to-last, or the first, element is 1 so we add 1 * 3^2 = 9 to the tally.
Now our tally is 10, which was our original integer.

The rest are left as an exercise for the reader.


---------------
Why a nitarray?
---------------
From the previous section, you can see that nits are just sequences of integers that are 
less than base-n that represent some *other* interger!  This process is analogous to how
32-bits are often used to represent a base-10 integer.

However in the above, every digit in the nit-list is itself a 32 bit (or longer) integer 
in memory.  This is a huge waste of resources for a data type that can be represneted
by fundementally smaller units.  (For example, it only takes 2 bits to represent base-3 or
base-4 digits, not 32.  It takes 3 bits to represent base-5 through base-8 digits.)

**Enter: nitarray.**  The nitarray class stores nits in the smallest number of bits possible.
Thus space and time are saved on common opperations on nitarrays over using standard python 
lists of 32-bit integers or longs.  As such, a nitarray is just a special way of encoding 
bits (using the `bitarray`_ package).  You can generate mappings from normal python 
intergers to their binary represnetation using the :func:`nit_endocding() <nitarray.nit_encoding>`  
function.  For example, 

.. code-block:: ipython

    In [1]: from nitarray import nit_encoding

    In [2]: nit_encoding(6)
    Out[2]: 
    {0: bitarray('000'),
     1: bitarray('001'),
     2: bitarray('010'),
     3: bitarray('011'),
     4: bitarray('100'),
     5: bitarray('101')}


---------------
Using nitarrays
---------------
Now that we know 'what' and 'why', it is time to get out hands dirty.  You can make a new 
nitarray in a few different ways.

.. code-block:: ipython

    In [1]: from nitarray import nitarray    

    In [2]: nitarray([1, 0, 2, 2, 0], 3)
    Out[2]: nitarray('1,0,2,2,0', 3)

    In [3]: nitarray('1,6,2,0,4', 7)
    Out[3]: nitarray('1,6,2,0,4', 7)

    In [4]: nitarray(37, 42)
    Out[4]: nitarray('0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0', 42)

In the first instance we passed the :class:`nitarray <nitarray.nitarray>` an iterartor
whose values are the nits.  In the second, we gave it a string of comma-separated nits.
In the third, an integer passed in means that we want a zero-array of this length. 
For all cases, we must pass in the base of the nitarray as the second argument.

Once you have a :class:`nitarray <nitarray.nitarray>`, there are a number of useful
methods that you may apply.

.. code-block:: ipython

    In [5]: n = nitarray([1, 0, 2, 2, 0], 3)

    In [6]: n.append(2)

    In [7]: n
    Out[7]: nitarray('1,0,2,2,0,2', 3)

    In [8]: n.count(2)
    Out[8]: 3

    In [9]: n.remove(0)

    In [10]: n
    Out[10]: nitarray('1,2,2,0,2', 3)

    In [11]: n.tolist()
    Out[11]: [1, 2, 2, 0, 2]

    In [12]: n.to01()
    Out[12]: '1,2,2,0,2'


Trying to append a nit that is greater than or equal to the base value is clearly not
allowed.

.. code-block:: ipython

    In [13]: n.append(42)
    ---------------------------------------------------------------------------
    AssertionError                            Traceback (most recent call last)

    /home/scopatz/<ipython console> in <module>()

    /home/scopatz/nitarray/nitarray/nitarray.pyc in append(self, x)
        382         """Appends the nit x to the end of the array."""
        383         x = int(x)
    --> 384         assert (x in self._allowed_nits)
        385         x_array = encodings_cache[self._n][x]
        386         self._bitarray += x_array

    AssertionError: 

As with other sequence types in Python, :class:`nitarrays <nitarray.nitarray>` can 
be indexed into and sliced.  Assigment can also take place from indexes and slices.  

.. warning:: 

    Striding is not currently supported because the underlying implementation is tricky.
    Currently, for speed, we pass slices down to bitarrays.  Striding would require
    reading out discrete chucks of bitarrays, which is not supported by the Python 
    syntax.  Since we cannot pass strides down to bitarray, this would have to be done
    at a higher level.
             
.. code-block:: ipython

    In [1]: from nitarray import nitarray

    In [2]: n = nitarray(10, 3)

    In [3]: n
    Out[3]: nitarray('0,0,0,0,0,0,0,0,0,0', 3)

    In [4]: n.setall(1)

    In [5]: n
    Out[5]: nitarray('1,1,1,1,1,1,1,1,1,1', 3)

    In [6]: n[3:8] = 5 * nitarray([2], 3)

    In [7]: n
    Out[7]: nitarray('1,1,1,2,2,2,2,2,1,1', 3)

    In [8]: del n[4:]

    In [9]: n
    Out[9]: nitarray('1,1,1,2', 3)

    In [10]: n += nitarray('1,2,0', 3)

    In [11]: n
    Out[11]: nitarray('1,1,1,2,1,2,0', 3)

    In [12]: n[3] = 0

    In [13]: n
    Out[13]: nitarray('1,1,1,0,1,2,0', 3)

    In [14]: n[2:4] = '0,2'

    In [15]: n
    Out[15]: nitarray('1,1,0,2,1,2,0', 3)

    In [16]: n[-5:-2]
    Out[16]: nitarray('0,2,1', 3)

    In [17]: n += [2,2,2,2]

    In [18]: n
    Out[18]: nitarray('1,1,0,2,1,2,0,2,2,2,2', 3)


Other standard Python sequence interfaces are also available.

.. code-block:: ipython

    In [19]: n.pop(0)
    Out[19]: 1

    In [20]: n
    Out[20]: nitarray('1,0,2,1,2,0,2,2,2,2', 3)

    In [21]: n.index(2)
    Out[21]: 2

    In [22]: n.remove(0)

    In [23]: n
    Out[23]: nitarray('1,2,1,2,0,2,2,2,2', 3)

    In [24]: n.extend([0, 1])

    In [25]: n
    Out[25]: nitarray('1,2,1,2,0,2,2,2,2,0,1', 3)

    In [26]: n.insert(5, 0)

    In [27]: n
    Out[27]: nitarray('1,2,1,2,0,0,2,2,2,2,0,1', 3)

    In [28]: n.sort()

    In [29]: n
    Out[29]: nitarray('0,0,0,1,1,1,2,2,2,2,2,2', 3)


------------------------------
Ecoding and Decoding nitarrays
------------------------------
The major use of bits is that arrays of bits can be encoded and decoded into other objects 
(*e.g.* characters).  To fully simulate other computer architectures, hooks into 
encoding and decoding :class:`nitarrays <nitarray.nitarray>` are also provided.

An encoding is simply a mapping from unique objects to nitarrays.  We acomplish this very 
naturally in Python using dictionaries.  We can then extend an existing nitarray using the
:meth:`encode() <nitarray.nitarray.encode>` method, this dictionary, and an iterable of 
the keys of the dictionary.  The following example uses strings, but any iterable of hashable
objects would work as well.


.. code-block:: ipython

    In [1]: from nitarray import nitarray

    In [2]: n = nitarray([], 42)

    In [3]: d = {'L': nitarray([7], 42), 'O': nitarray(6, 42)}

    In [4]: n.encode(d, 'LOL')

    In [5]: n
    Out[5]: nitarray('7,0,0,0,0,0,0,7', 42)


To decode a nitarray pass in the same mapping as before to the 
:meth:`decode() <nitarray.nitarray.decode>` method.  This will return a list  of the 
keys of the coding.  

.. code-block:: ipython

    In [6]: n.decode(d)
    Out[6]: ['L', 'O', 'L']

As seen here, if you decode with the same dictionary as that you encoded with, 
you obtain an equivelent iterable.  Hoever, you could have chosen to decode with another
mapping.

.. code-block:: ipython

    In [7]: d1 = {1: nitarray([7], 42), '!': nitarray(2, 42)}
    
    In [8]: n.decode(d1)
    Out[8]: [1, '!', '!', '!', 1]

Encoding and decoding becomes very useful when dealing with sequences of characters, or strings.
In fact, this is such a common use case that we provide a function to generate ASCII-to-nitarray
encoding dictionaries, :func:`char_encoding() <nitarray.char_encoding>`.

.. code-block:: ipython

    In [1]: from nitarray import char_encoding

    In [2]: char_encoding(3)
    Out[2]: 
    {'\x00': nitarray('0,0,0,0,0,0', 3),
     '\x01': nitarray('0,0,0,0,0,1', 3),
     '\x02': nitarray('0,0,0,0,0,2', 3),
    ...
     ' ': nitarray('0,0,1,0,1,2', 3),
     '!': nitarray('0,0,1,0,2,0', 3),
     '"': nitarray('0,0,1,0,2,1', 3),
     '#': nitarray('0,0,1,0,2,2', 3),
     '$': nitarray('0,0,1,1,0,0', 3),
    ...
     'A': nitarray('0,0,2,1,0,2', 3),
     'B': nitarray('0,0,2,1,1,0', 3),
     'C': nitarray('0,0,2,1,1,1', 3),
    ...
    }

It is these character encodings that are used automatically when you use the 
:meth:`tostring() <nitarray.nitarray.fromstring>`,
:meth:`fromstring() <nitarray.nitarray.fromstring>`,
:meth:`tofile() <nitarray.nitarray.fromstring>`, or
:meth:`fromfile() <nitarray.nitarray.fromstring>` methods.

.. code-block:: ipython

    In [1]: from nitarray import nitarray

    In [2]: n = nitarray([], 42)

    In [3]: n.fromstring("No one expects the Spanish Inquisition!")

    In [4]: n
    Out[4]: nitarray('1,36,2,27,0,32,2,27,2,26,2,17,0,32,2,17,2,36,2,28,2,17,'
                     '2,15,2,32,2,31,0,32,2,32,2,20,2,17,0,32,1,41,2,28,2,13,'
                     '2,26,2,21,2,31,2,20,0,32,1,31,2,26,2,29,2,33,2,21,2,31,'
                     '2,21,2,32,2,21,2,27,2,26,0,33', 42)

    In [5]: n.tostring()
    Out[5]: 'No one expects the Spanish Inquisition!'



.. _trits: http://en.wikipedia.org/wiki/Trit

.. _bitarray: http://pypi.python.org/pypi/bitarray
