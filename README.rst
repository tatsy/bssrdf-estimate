****
bssrdf-estimate
****

.. image:: https://travis-ci.org/tatsy/bssrdf-estimate.svg?branch=master
  :target: https://travis-ci.org/tatsy/bssrdf-estimate

.. image:: https://coveralls.io/repos/tatsy/bssrdf-estimate/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/tatsy/bssrdf-estimate?branch=master

Implementation of "BSSRDF Estimation from Single Images" by Munoz et al. (Eurographics 2011)

=============
Installation
=============


On **Linux**, you can easily install bssrdf-estimate with some commands.

------
Linux
------

Install LAPACK/BLAS

.. code-block:: bash

  $ sudo apt-get install liblapack-dev libblas-dev

Install required packages. You can do it easily with ``pip``

.. code-block:: bash

  $ sudo pip install -r requirements.txt


Install ``spica`` (renderer). You can do it easily with ``cmake``

.. code-block:: bash

  $ git submodule update --init --recursive
  $ cmake .
  $ cmake --build .


Run ``setup.py`` to finish installation.

.. code-block:: bash

  $ python setup.py install


--------
Windows
--------

#. Install required packages from http://www.lfd.uci.edu/~gohlke/pythonlibs/ (check requirements.txt)

#. Install Qt5, PyQt5 (with SIP)

#. Build spica renderer. Using CMake is the best choice.

#. Run setup.py

.. code-block:: bash

  $ python setup.py install
  
======
Usage
======

Run main.py::

  $ python main.py

========
License
========

MIT license 2015 (c) Tatsuya Yatagawa
