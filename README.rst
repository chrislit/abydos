Abydos
======

.. image:: https://travis-ci.org/chrislit/abydos.svg
    :target: https://travis-ci.org/chrislit/abydos
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/chrislit/abydos/badge.svg?branch=master
    :target: https://coveralls.io/github/chrislit/abydos?branch=master
    :alt: Coverage Status

.. image:: https://codeclimate.com/github/chrislit/abydos/badges/gpa.svg
   :target: https://codeclimate.com/github/chrislit/abydos
   :alt: Code Climate

.. image:: https://landscape.io/github/chrislit/abydos/master/landscape.svg?style=flat
   :target: https://landscape.io/github/chrislit/abydos/master
   :alt: Code Health

.. image:: https://snyk.io/test/github/chrislit/abydos/badge.svg?targetFile=requirements.txt
    :target: https://snyk.io/test/github/chrislit/abydos?targetFile=requirements.txt
    :alt: Known Vulnerabilities

.. image:: https://scrutinizer-ci.com/g/chrislit/abydos/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/chrislit/abydos/?branch=master
    :alt: Scrutinizer

.. image:: https://bestpractices.coreinfrastructure.org/projects/1598/badge
    :target: https://bestpractices.coreinfrastructure.org/projects/1598
    :alt: CII Best Practices

.. image:: https://ci.appveyor.com/api/projects/status/d3yw3d9r6c8ai63j/branch/master?svg=true
    :target: https://ci.appveyor.com/project/chrislit/abydos
    :alt: AppVeyor

.. image:: https://api.codacy.com/project/badge/Grade/db79f2c31ea142fb9b5938abe87b0854
    :target: https://www.codacy.com/app/chrislit/abydos?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=chrislit/abydos&amp;utm_campaign=Badge_Grade
    :alt: Codacy

.. image:: https://requires.io/github/chrislit/abydos/requirements.svg?branch=master
    :target: https://requires.io/github/chrislit/abydos/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://img.shields.io/librariesio/sourcerank/pypi/abydos.svg
    :target: https://libraries.io/pypi/abydos
    :alt: Libraries.io SourceRank

.. image:: https://img.shields.io/badge/Pylint-9.75/10-green.svg
   :target: #
   :alt: Pylint Score

.. image:: https://img.shields.io/badge/pycodestyle-5-green.svg
   :target: #
   :alt: pycodestyle Errors

.. image:: https://img.shields.io/badge/flake8-56-yellow.svg
   :target: #
   :alt: flake8 Errors

.. image:: https://img.shields.io/pypi/v/abydos.svg
    :target: https://pypi.python.org/pypi/abydos
    :alt: PyPI

.. image:: 	https://img.shields.io/pypi/pyversions/abydos.svg
    :target: https://pypi.python.org/pypi/abydos
    :alt: PyPI versions

.. image:: https://img.shields.io/conda/vn/conda-forge/abydos.svg
    :target: #
    :alt: conda-forge

.. image:: 	https://img.shields.io/conda/dn/conda-forge/abydos.svg
    :target: #
    :alt: conda-forge downloads

.. image:: https://img.shields.io/conda/pn/conda-forge/abydos.svg
    :target: #
    :alt: conda-forge platforms

.. image:: https://readthedocs.org/projects/abydos/badge/?version=latest
    :target: https://abydos.readthedocs.org/en/latest/
    :alt: Documentation Status

.. image:: https://badge.waffle.io/chrislit/abydos.svg?columns=all
    :target: https://waffle.io/chrislit/abydos
    :alt: 'Waffle.io - Columns and their card count'

.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0
    :alt: License: GPL v3

.. image:: https://www.openhub.net/p/abydosnlp/widgets/project_thin_badge.gif
    :target: https://www.openhub.net/p/abydosnlp
    :alt: OpenHUB

|

.. image:: https://raw.githubusercontent.com/chrislit/abydos/master/abydos-small.png
    :alt: abydos
    :align: right

|
| Abydos NLP/IR library
| Copyright 2014-2018 by Chris Little

Abydos is a library of phonetic algorithms, string distance metrics, stemmers, and keyers, including:

- Phonetic algorithms
    - Robert C. Russell's Index
    - American Soundex
    - Refined Soundex
    - Daitch-Mokotoff Soundex
    - Kölner Phonetik
    - NYSIIS
    - Match Rating Algorithm
    - Metaphone
    - Double Metaphone
    - Caverphone
    - Alpha Search Inquiry System
    - Fuzzy Soundex
    - Phonex
    - Phonem
    - Phonix
    - SfinxBis
    - phonet
    - Standardized Phonetic Frequency Code
    - Statistics Canada
    - Lein
    - Roger Root
    - Oxford Name Compression Algorithm (ONCA)
    - Eudex phonetic hash
    - Haase Phonetik
    - Reth-Schek Phonetik
    - FONEM
    - Parmar-Kumbharana
    - Beider-Morse Phonetic Matching
- String distance metrics
    - Levenshtein distance
    - Optimal String Alignment distance
    - Levenshtein-Damerau distance
    - Hamming distance
    - Tversky index
    - Sørensen–Dice coefficient & distance
    - Jaccard similarity coefficient & distance
    - overlap similarity & distance
    - Tanimoto coefficient & distance
    - Minkowski distance & similarity
    - Manhattan distance & similarity
    - Euclidean distance & similarity
    - Chebyshev distance & similarity
    - cosine similarity & distance
    - Jaro distance
    - Jaro-Winkler distance (incl. the strcmp95 algorithm variant)
    - Longest common substring
    - Ratcliff-Obershelp similarity & distance
    - Match Rating Algorithm similarity
    - Normalized Compression Distance (NCD) & similarity
    - Monge-Elkan similarity & distance
    - Matrix similarity
    - Needleman-Wunsch score
    - Smither-Waterman score
    - Gotoh score
    - Length similarity
    - Prefix, Suffix, and Identity similarity & distance
    - Modified Language-Independent Product Name Search (MLIPNS) similarity &
      distance
    - Bag distance
    - Editex distance
    - Eudex distances
    - Sift4 distance
    - Baystat distance & similarity
    - Typo distance
- Stemmers
    - the Lovins stemmer
    - the Porter and Porter2 (Snowball English) stemmers
    - Snowball stemmers for German, Dutch, Norwegian, Swedish, and Danish
    - CLEF German, German plus, and Swedish stemmers
    - Caumann's German stemmer
    - UEA-Lite Stemmer
    - Paice-Husk Stemmer
- Keyers
    - string fingerprint
    - q-gram fingerprint
    - phonetic fingerprint
    - Pollock & Zomora's skeleton key
    - Pollock & Zomora's omission key
    - Cisłak & Grabowski's occurrence fingerprint
    - Cisłak & Grabowski's occurrence halved fingerprint
    - Cisłak & Grabowski's count fingerprint
    - Cisłak & Grabowski's position fingerprint

Required:

- Numpy

Recommended:

- PylibLZMA   (Python 2 only--for LZMA compression string distance metric)

Suggested for development, testing, & QA:

- Nose        (for unit testing)
- coverage.py (for code coverage checking)
- Pylint      (for code quality checking)
- PEP8        (for code quality checking)

-----

Installation
============

To install Abydos from PyPI using pip::

   pip install abydos

It should run on Python 2.7 and Python 3.3+


To build/install/unittest from source in Python 2::

    sudo python setup.py install
    nosetests -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=abydos .

To build/install/unittest from source in Python 3::

    sudo python3 setup.py install
    nosetests3 -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=abydos .

For pylint testing, run::

    pylint --rcfile=pylint.rc abydos > pylint.log

A simple shell script is also included, which will build,
install, test, and code-quality check (with Pylint & PEP8)
the package and build the documentations. To run it, execute::

    ./btest.sh
