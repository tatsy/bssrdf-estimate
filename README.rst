****************
bssrdf-estimate
****************

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

Second, please install required python modules. The modules are listed in `requirements.txt <https://github.com/tatsy/bssrdf-estimate/blob/master/requirements.txt>`_, which you can install with ``pip``. When you install them to the global environment, please do not forget to add ``sudo``.

.. code-block:: bash

  $ sudo pip install -r requirements.txt

Please note that ``PyQt5`` is not listed in `requirements.txt <https://github.com/tatsy/bssrdf-estimate/blob/master/requirements.txt>`_ because its installation varies for different Linux versions.

So, please separately install ``Qt5``, ``SIP`` and ``PyQt5`` from following websites.

* https://www.qt.io/download-open-source/ (for ``Qt5``)
* http://www.riverbankcomputing.com/software/sip/download (for ``SIP``)
* http://www.riverbankcomputing.com/software/pyqt/download5 (for ``PyQt5``)

Next, please install `spica <https://github.com/tatsy/spica.git>`_ (a renderer package). ``spica`` can be easily built with ``cmake`` (ver. 3.0.0 or higher). As ``spica`` is recorded as a submodule, you can install it with the following command.

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

Installation for **Windows** is rather complicated due to absense of the package manager. Please follow the instruction below to complete the installation.

First, please install required python modules from http://www.lfd.uci.edu/~gohlke/pythonlibs/. Required modules are listed below.

* numpy
* scipy
* matplotlib
* cvxopt

As ``PyQt5`` is not provided in the website, please install ``Qt5``, ``SIP`` and ``PyQt5`` manually. For ``Qt5``, please visit https://www.qt.io/download-open-source/ to get web installer. After that get source files of ``SIP`` and ``PyQt5`` from following websites.

* http://www.riverbankcomputing.com/software/sip/download (for ``SIP``)
* http://www.riverbankcomputing.com/software/pyqt/download5 (for ``PyQt5``)

Please make sure that you have MSVC compiler and nmake to install ``PyQt5``.

Second, please build `spica <https://github.com/tatsy/spica.git>`_ (renderer). For this package, CMakeLists are provided and you can build it with ``cmake`` (ver. 3.0.0 or higher).

Finally, please run ``setup.py`` with appropriate VC compiler. For example, you have to use **VC 2008** for python 2.7 and **VC 2010** for python 3.4. You can find these compilers in the following links.

* `Microsoft Visual C++ Compiler for Python 2.7  <http://www.microsoft.com/en-us/download/details.aspx?id=44266>`_
* `Microsoft Windows SDK for Windows 7 and .NET Framework 4 <http://www.microsoft.com/en-us/download/details.aspx?id=8279>`_

.. code-block::

  // Launch VC 20xx command prompt
  $ python setup.py install

======
Usage
======

Running main.py will display a main window.

.. code-block:: bash

  $ python main.py

You can load project file by pushing ``Load`` button. The project sample is as follows.

.. code-block:: xml

  <content>
    <entry type="image">target_image.hdr</entry>
    <ettry type="mask">target_mask.png</entry>
  </content>
  
The required files are two. One is input HDR (high-dynamic-range) image of Exposure .hdr format. The second one is binary mask image. You can find the sample files in `sample <https://github.com/tatsy/bssrdf-estimate/tree/master/sample>`_ folder.

=======
Result
=======

------
input
------

.. image:: https://raw.githubusercontent.com/tatsy/bssrdf-estimate/master/sample/milk_image.png

-------
result
-------

.. image:: https://raw.githubusercontent.com/tatsy/bssrdf-estimate/master/sample/render_image.png
   :width: 400 px

========
License
========

The MIT License 2015 (c) tatsy, Tatsuya Yatagawa
