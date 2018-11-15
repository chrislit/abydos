================
  Introduction
================

Abydos
======

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
    - Chebyshev distance
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

To install from `conda-forge <https://anaconda.org/conda-forge/abydos>`_::

   conda install abydos

It should run on Python 2.7 and Python 3.3-3.7.

Testing & Contributing
======================

To run the whole test-suite just call tox::

    tox

The tox setup has the following environments: black, py36, py27, doctest,
py36-regression, py27-regression, py36-fuzz, py27-fuzz, pylint, pycodestyle,
pydocstyle, flake8, doc8, badges, docs, & dist. So if you only want to generate
documentation (in HTML, EPUB, & PDF formats), just call::

    tox -e docs

In order to only run & generate Flake8 reports, call::

    tox -e flake8

Contributions such as bug reports, PRs, suggestions, desired new features, etc.
are welcome through Github
`Issues <https://github.com/chrislit/abydos/issues>`_ &
`Pull requests <https://github.com/chrislit/abydos/pulls>`_.

Badges
======

The `project's main page <https://github.com/chrislit/abydos>`_ has quite a
few badges, some seemingly redundant, and a bit of explanation is perhaps
warranted.

- CI & Test Status

    - `Travis-CI <https://travis-ci.org/chrislit/abydos>`_ is the primary CI
      used for Linux CI of all supported Python platforms (2.7-3.8-dev). Only
      the tests in the tests directory are run.
    - `CircleCI <https://circleci.com/gh/chrislit/abydos/tree/master>`_ runs
      only the Python 3.6 tests on Linux and is used for quick tests of each
      commit.
    - `Appveyor <https://ci.appveyor.com/project/chrislit/abydos>`_ is used to
      check for Windows CI of all supported Python platforms (2.7-3.7, with
      both 32-bit & 64-bit Python). Only the tests in the tests directory are
      run.
    - `Semaphore <https://semaphoreci.com/chrislit/abydos>`_ is used to run
      the tests in the tests directory, doctests, regression tests, and fuzz
      tests.
    - `Coveralls <https://coveralls.io/github/chrislit/abydos?branch=master>`_
      is used to track test coverage.

- Code Quality (some may be removed at a later date)

    - `Code Climate <https://codeclimate.com/github/chrislit/abydos>`_ is used
      to check maintainability, but mostly just complains about McCabe
      complexity.
    - `Scrutinizer <https://scrutinizer-ci.com/g/chrislit/abydos/>`_ is used
      to check complexity and compliance with best practices.
    - `Codacy <https://app.codacy.com/project/chrislit/abydos/dashboard>`_ is
      used to check code style, security issues, etc.
    - `CodeFactor <https://www.codefactor.io/repository/github/chrislit/abydos>`_
      is used to track hotspot files in need of attention.

- Dependencies

    - `Requires.io <https://requires.io/github/chrislit/abydos/requirements/?branch=master>`_
      tracks whether Abydos can be used with the most recent releases of its
      dependencies.
    - `Snyk <https://snyk.io/test/github/chrislit/abydos?targetFile=requirements.txt>`_
      tracks whether there are security vulnerabilities in any dependencies.
    - `Pyup.io <https://pyup.io/repos/github/chrislit/abydos/>`_ tracks updates
      and security vulnerabilities in dependencies.
    - `FOSSA <https://app.fossa.io/projects/git%2Bgithub.com%2Fchrislit%2Fabydos?ref=badge_shield>`_
      checks license compliance.

- Local Analysis

    - Pylint score run locally
    - flake8 score run locally, should be 0
    - pydocstyle score run locally, shoule be 0
    - code style black signals that black is used for code styling

- Usage

    - `Read the Docs <https://abydos.readthedocs.org/en/latest/>`_ hosts
      Abydos documentation online.
    - `Binder <https://mybinder.org/v2/gh/chrislit/abydos/master?filepath=binder>`_
      provides an online notebook environment for the demo notebooks.
    - `GPL v3+ <https://www.gnu.org/licenses/gpl-3.0>`_ is the license used by
      Abydos.
    - `Libraries.io <https://libraries.io/pypi/abydos>`_ assigns a SourceRank
      to indicate project quality and popularity.
    - `zenodo <https://zenodo.org/record/1463204>`_ publishes the DOI and
      citation information for Abydos.

- Contribution

    - `CII Best Practices <https://bestpractices.coreinfrastructure.org/en/projects/1598>`_
      identifies compliance with Core Infrastructure Initiative best practices.
    - `waffle.io <https://waffle.io/chrislit/abydos>`_ is used for issue
      tracking and planning.
    - `OpenHub <https://www.openhub.net/p/abydosnlp>`_ tracks project activity
      and KLOC and estimates project value.

- PyPI

    - `PyPI <https://pypi.python.org/pypi/abydos>`_ hosts the pip installable
      packages. The pypi badge indicates the most recent pip installable
      version.
    - The downloads badge indicates the number of downloads from PyPI per
      month.
    - The python badge indicates the versions of Python that are supported.

- conda-forge

    - `conda-forge <https://anaconda.org/conda-forge/abydos>`_ hosts the
      conda installable packages. The conda-forge badge indicates the most
      recent conda installable version.
    - The downloads badge indicates the number of downloads from conda-forge.
    - The platform badge indicates that Abydos is a pure Python project,
      without platform-specific builds.


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
