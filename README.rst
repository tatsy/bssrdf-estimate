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

-------------------------
Linux (Ubuntu 14.04 LTS)
-------------------------

First, please install ``LAPACK`` and ``BLAS`` with ``apt-get``.

.. code-block:: bash

  $ sudo apt-get install liblapack-dev libblas-dev

Second, please install required python modules. The modules list is stored in `requirements.txt <https://github.com/tatsy/bssrdf-estimate/blob/master/requirements.txt>`_, which you can install them with ``pip``. If you install them for global environment, please do not forget ``sudo``.

.. code-block:: bash

  $ sudo pip install -r requirements.txt

Next, please install `spica <https://github.com/tatsy/spica.git>`_ (a renderer package). ``spica`` can be easily built with ``cmake``. As ``spica`` is recorded as a submodule, you can install it with the following command.

.. code-block:: bash

  $ git submodule update --init --recursive
  $ cmake -DSPICA_BUILD_EXAMPLE=OFF -DSPICA_BUILD_TEST=OFF -DBUILD_SPICA_VIEWER=OFF -DENABLE_AVX=OFF .
  $ cmake --build .


Finally, please run ``setup.py`` to finish installation. Again, please do not forget to add ``sudo`` when you install this package for your global environment.

.. code-block:: bash

  $ sudo python setup.py install


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
