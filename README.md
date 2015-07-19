bssrdf-estimate
===

[![Build Status](https://travis-ci.org/tatsy/bssrdf-estimate.svg)](https://travis-ci.org/tatsy/bssrdf-estimate)
[![Coverage Status](https://coveralls.io/repos/tatsy/bssrdf-estimate/badge.svg?branch=master&service=github)](https://coveralls.io/github/tatsy/bssrdf-estimate?branch=master)

> Implementation of "BSSRDF Estimation from Single Images" by Munoz et al. (Eurographics 2011)

### Build

#### 1. Install packages required

```shell
pip install -r requirements.txt
```

#### 2. Install PyQt5

* Please make that sure Qt5 is installed to your system and that path/to/qmake is added to environment PATH.
* Access [http://www.riverbankcomputing.co.uk/software/pyqt/download5](http://www.riverbankcomputing.co.uk/software/pyqt/download5) and download SIP and PyQt5 packages.
* Build SIP with ```make & make install```.
* Finally, build PyQt5 with ```make & make install```.

#### 3. Install this package

```shell
python setup.py install
```

### Usage

```shell
python main.py
```
