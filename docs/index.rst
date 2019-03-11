mr_utils: magnetic resonance utilities
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   modules/index


This repo is a collection of my implementations of algorithms and tools for
MR image reconstruction, mostly in python.

Orientation
===========

There are few different things going on here.  There are algorithms, like
the geometric solution to the elliptical signal model, as well as simulations,
like simulated bSSFP contrast.

There's also some python functions and objects that interact with more polished
tools such as Gadgetron and BART. You can use these python interfaces to easily
write in Gadgetron, MATLAB, or BART functionality into your python scripts.
These functions are written with the assumption of Gadgetron, MATLAB, etc.
being run on some processing server (not necessarily on your local machine). If
you use these, you'll want to create a config file.

Documentation and Tests
=======================

Documentation is almost exclusively found in the docstrings of modules,
functions, and classes.

Another great way to learn how things are used is by looking in the examples.
Run examples from the root directory (same directory as setup.py) like this:

.. code-block:: bash

    python3 examples/cs/reordering/cartesian_pe_fd_iht.py


If there's not an example, there might be some tests.  Individual tests can be
run like this from the root directory (I recommend that you run tests from the
home directory - imports will get messed up otherwise):

.. code-block:: bash

    python3 -m unittest mr_utils/tests/recon/test_gs_recon.py

All tests can be run like so:

.. code-block:: bash

    pyhon3 -m unittest discover

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
