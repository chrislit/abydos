Release History
---------------


0.3.5 (2018-10-31) *cantankerous carl*
++++++++++++++++++++++++++++++++++++++

doi:10.5281/zenodo.1463204

Version 0.3.5 focuses on refactoring the whole project. The API itself remains
largely the same as in previous versions, but underlyingly modules have been
split up. Essentially no new features are added (bugfixes aside) in this
version.

Changes:

- Refactored library and tests into smaller modules
- Broke compression distances (NCD) out into separate functions
- Adopted Black code style
- Added pyproject.toml to use Poetry for packaging (but will continue using
  setuptools and setup.py for the present)
- Minor bug fixes


0.3.0 (2018-10-15) *carl*
+++++++++++++++++++++++++

doi:10.5281/zenodo.1462443

Version 0.3.0 focuses on additional phonetic algorithms, but does add numerous
distance measures, fingerprints, and even a few stemmers. Another focus was
getting everything to build again (including docs) and to move to more
standard modern tools (flake8, tox, etc.).

Changes:

- Fixed implementation of Bag distance
- Updated BMPM to version 3.10
- Fixed Sphinx documentation on readthedocs.org
- Split string fingerprints out of clustering into their own module
- Added support for q-grams to skip-n characters
- New phonetic algorithms:
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
- New string fingerprints:
   - Cisłak & Grabowski's occurrence fingerprint
   - Cisłak & Grabowski's occurrence halved fingerprint
   - Cisłak & Grabowski's count fingerprint
   - Cisłak & Grabowski's position fingerprint
   - Synoname Toolcode
- New distance measures:
   - Minkowski distance & similarity
   - Manhattan distance & similarity
   - Euclidean distance & similarity
   - Chebyshev distance & similarity
   - Eudex distances
   - Sift4 distance
   - Baystat distance & similarity
   - Typo distance
   - Indel distance
   - Synoname
- New stemmers:
   - UEA-Lite Stemmer
   - Paice-Husk Stemmer
   - Schinke Latin stemmer
- Eliminated ._compat submodule in favor of six
- Transitioned from PEP8 to flake8, etc.
- Phonetic algorithms now consistently use max_length=-1 to indicate that
  there should be no length limit
- Added example notebooks in binder directory


0.2.0 (2015-05-27) *berthold*
+++++++++++++++++++++++++++++

- Added Caumanns' German stemmer
- Added Lovins' English stemmer
- Updated Beider-Morse Phonetic Matching to 3.04
- Added Sphinx documentation


0.1.1 (2015-05-12) *albrecht*
+++++++++++++++++++++++++++++

- First Beta release to PyPI
