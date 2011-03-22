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



.. _trits: http://en.wikipedia.org/wiki/Trit
