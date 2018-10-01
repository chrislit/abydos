================
  Introduction
================

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

.. image:: https://img.shields.io/badge/Pylint-9.79/10-green.svg
   :target: #
   :alt: Pylint Score

.. image:: https://img.shields.io/badge/pycodestyle-0-brightgreen.svg
   :target: #
   :alt: pycodestyle Errors

.. image:: https://img.shields.io/badge/flake8-61-yellow.svg
   :target: #
   :alt: flake8 Errors

.. image:: https://img.shields.io/pypi/v/abydos.svg
    :target: https://pypi.python.org/pypi/abydos
    :alt: PyPI

.. image:: https://readthedocs.org/projects/abydos/badge/?version=latest
    :target: https://abydos.readthedocs.org/en/latest/
    :alt: Documentation Status

|

.. image:: https://raw.githubusercontent.com/chrislit/abydos/master/abydos-small.png
    :alt: abydos
    :align: right

|
| Abydos NLP/IR library
| Copyright 2014-2018 by Christopher C. Little

Abydos is a library of phonetic algorithms, string distance measures & metrics,
stemmers, and string fingerprinters including:

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
    - Davidson's Consonant Code
    - SoundD
    - PSHP Soundex/Viewex Coding
    - an early version of Henry Code
    - Norphone
    - Dolby Code
    - Phonetic Spanish
    - Spanish Metaphone
    - MetaSoundex
    - SoundexBR
    - NRL English-to-phoneme
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
    - Indel distance
    - Synoname
- Stemmers
    - the Lovins stemmer
    - the Porter and Porter2 (Snowball English) stemmers
    - Snowball stemmers for German, Dutch, Norwegian, Swedish, and Danish
    - CLEF German, German plus, and Swedish stemmers
    - Caumann's German stemmer
    - UEA-Lite Stemmer
    - Paice-Husk Stemmer
    - Schinke Latin stemmer
    - S stemmer
- String Fingerprints
    - string fingerprint
    - q-gram fingerprint
    - phonetic fingerprint
    - Pollock & Zomora's skeleton key
    - Pollock & Zomora's omission key
    - Cisłak & Grabowski's occurrence fingerprint
    - Cisłak & Grabowski's occurrence halved fingerprint
    - Cisłak & Grabowski's count fingerprint
    - Cisłak & Grabowski's position fingerprint
    - Synoname Toolcode

-----

Installation
============

Required libraries:

- Numpy
- Six

Recommended libraries:

- PylibLZMA   (Python 2 only--for LZMA compression string distance metric)


To install Abydos (master) from Github source::

   git clone https://github.com/chrislit/abydos.git --recursive
   cd abydos
   python setup install

If your default python command calls Python 2.7 but you want to install for
Python 3, you may instead need to call::

   python3 setup install


To install Abydos (latest release) from PyPI using pip::

   pip install abydos

It should run on Python 2.7 and Python 3.3-3.7.

Testing & Contributing
======================

To run the whole test-suite just call tox::

    tox

The tox setup has the following environments: py27, py36, pylint, pycodestyle,
flake8, badges, docs. So if only want to generate documentation (in HTML, EPUB,
& PDF formats), just call::

    tox -e docs

In order to only run & generate Flake8 reports, call::

    tox -e flake8

Contributions such as bug reports, PRs, suggestions, desired new features, etc.
are welcome through the Github Issues & Pull requests.

-----

License
=======

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see
<https://www.gnu.org/licenses/gpl.txt>.
