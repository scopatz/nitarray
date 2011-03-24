======================================
Welcome to the nitarray documentation!
======================================
This project asks the question 'What if computer architecture weren't binary?'
Rather than having 2-bits as the fundamental unit, what if there were 3-bits,
4-bits, etc.  This package provides N-bit (nit) arrays as well and hooks into
encoding and decoding these arrays.

The nitarrays are stored efficiently in memory by using the minimum number
of physical bits possible.  To do this without too much headache, we
rely on the bitarray package by Ilan Schnell.

Nitarray has only one dependency, bitarray:
   #. `bitarray <http://pypi.python.org/pypi/bitarray>`_

The source code for nitarray may be found at the
`GitHub project site <http://github.com/scopatz/char>`_.
Or you may simply clone from the master using git::

    git clone git://github.com/scopatz/nitarray.git

No Windows builds are currently available because I am lazy and don't use Windows.
However, this project is pure python so installing is very easy.  Either download 
and unzip the project from github, or clone it as above.  Then, in a terminal::

    cd path/to/source/
    python setup.py install

--------
Contents
--------

.. toctree::
   :maxdepth: 1

   tutorial
   api
   contact

=============
Helpful Links
=============
	
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
