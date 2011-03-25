.. Abstract submission template for SciPy2011: The 10th
.. Python in Science Conference, to be held in Austin, Tx,
.. July 11 - 16 2011.
..
.. Programme chairs:
..
..  Stefan van der Walt <stefan at sun.ac.za>
..  Warren Weckesser <warren.weckesser at enthought.com>
..
.. For more information, visit
.. http://conference.scipy.org/scipy2011/


========================================
atobrute: why plaintext isn't so vanilla
========================================

:Author: Anthony Scopatz <ascopatz@enthought.com>
:Affiliation: Enthought, Inc.

When shopping for a database or persistence mechanism in the modern world, 
there are a lot of options.  Plain text files, proprietary formats (eg Microsoft Excel), 
SQL and NoSQL databases all confer certain advantages/disadvantages.  However, 
most scientist and engineers simply want to store numerical data.
More efficient binary formats, which store the in-memory representation of numeric types, 
are often overlooked in the quantitative space.

This talk will first explore the structure of how plaintext is stored on the hard disk, 
and why using plaintext is to store numbers is inefficient (spatially).  
Then because of the need for conversion from human-readable to machine-readable, 
this talk will next tackle why canonical functions such as *atoi()* and *atof()* 
are inefficient (temporally).

Next, suppose we were able to break free from the tyranny of binary architecture.  
This talk will also explore the numerical advantages and disadvantages to moving
to ternary (or higher) order computer architectures and why this is not a remote
possibility within our lifetimes.  

To enable the efficient modeling of base-n architectures, the author developed 
the `nitarray`_ python package.  Nitarrays automatically map sequences of integers, valued 
on the range [0, n-1] (*nits*), to the minimum number of bits required in physical memory.
Additionally, much like traditional bit- and byte-arrays, hooks to encode/decode nitarrays
from other python objects are also included.

Naturally, the most common encodings come from length-1 strings to *nytes*, the 
nit-equivalent of bytes.  From here, atoi() and atof() functions in nitspace can be 
implemented.  The relative merits of using exotic architectures to the traditional 
binary structure of data are then compared from a scientist's perspective.

While this talk embodies a clean application of power and log arithmetic, it is the 
hope of the author that it makes other scientists and engineers more cognizant of 
data storage and retrieval issues.  

.. nitarray: http://scopatz.github.com/nitarray/

...............................................................

Please indicate with an X whether you are willing to prepare an
accompanying paper::

  [X] Yes  [ ] No

...............................................................


...............................................................

Optional: Indicate your preference for a specialized track::
 
  [ ] Python in Data Science 

  [ ] Python and Core Technologies

Even if you don't select a track, we may schedule your talk
in a track if it seems appropriate.  Also, if you select a
track, we will also consider your submission for the regular
session.

...............................................................

Please email this form to 2011submissions@scipy.org
