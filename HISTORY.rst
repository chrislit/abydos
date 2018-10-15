Release History
---------------

0.3.0 (2018-10-15)
++++++++++++++++++

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


0.2.0 (2015-05-27)
++++++++++++++++++

- Added Caumanns' German stemmer
- Added Lovins' English stemmer
- Updated Beider-Morse Phonetic Matching to 3.04
- Added Sphinx documentation


0.1.1 (2015-05-12)
++++++++++++++++++

- First Beta release to PyPI
