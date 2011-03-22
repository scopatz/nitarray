===================================
nitarray: a base n 'bit' array type
===================================
This project asks the question 'What if computer architecture weren't binary?'
Rather than having 2-bits as the fundamental unit, what if there were 3-bits, 
4-bits, etc.   This package provides N-bit (nit) arrays as well and hooks into 
encoding and decoding these arrays.

The nitarrays are stored efficiently in memory by using the minimum number 
of physical bits possible.  To do this without too much headache, we 
rely on the bitarray package by Ilan Schnell.
