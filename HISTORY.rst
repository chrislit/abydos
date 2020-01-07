Release History
---------------

0.4.1 (2020-01-07) *distant dietrich*
+++++++++++++++++++++++++++++++++++++

doi:10.5281/zenodo.3600548

Changes:

- Support for Python 3.4 was removed. (3.4 reached end-of-life on March 18,
  2019)
- Fuzzy intersections were corrected to avoid over-counting partial
  intersection instances.
- Levenshtein can now return an optimal alignment
- Added the following distance measures:
    - Indice de Similitude-Guth (ISG)
    - INClusion Programme
    - Guth
    - Victorian Panel Study (VPS) score
    - LIG3 similarity
    - Discounted Levenshtein
    - Relaxed Hamming
    - String subsequence kernel (SSK) similarity
    - Phonetic edit distance
    - Henderson-Heron dissimilarity
    - Raup-Crick similarity
    - Millar's binomial deviance dissimilarity
    - Morisita similarity
    - Horn-Morisita similarity
    - Clark's coefficient of divergence
    - Chao's Jaccard similarity
    - Chao's Dice similarity
    - Cao's CY similarity (CYs) and dissimilarity (CYd)
- Added the following fingerprint classes:
    - Taft's Consonant coding
    - Taft's Extract - letter list
    - Taft's Extract - position & frequency
    - L.A. County Sheriff's System
    - Library of Congres Cutter table encoding
- Added the following phonetic algorithms:
    - Ainsworth's grapheme-to-phoneme
    - PHONIC


0.4.0 (2019-05-30) *dietrich*
+++++++++++++++++++++++++++++

doi:10.5281/zenodo.3235034

Version 0.4.0 focuses on distance measures, adding 211 new measures. Attempts
were made to provide normalized version for measure that did not inherently
range from 0 to 1. The other major focus was the addition of 12 tokenizers, in
service of expanding distance measure options.

Changes:

- Support for Python 3.3 was dropped.
- Deprecated functions that merely wrap class methods to maintain API
  compatibility, for removal in 0.6.0
- Added methods to ConfusionTable to return:
    - its internal representation
    - false negative rate
    - false omission rate
    - positive & negative likelihood ratios
    - diagnostic odds ratio
    - error rate
    - prevalence
    - Jaccard index
    - D-measure
    - Phi coefficient
    - joint, actual, & predicted entropies
    - mutual information
    - proficiency (uncertainty coefficient)
    - information gain ratio
    - dependency
    - lift
- Deprecated f-measure & g-measure from ConfusionTable for removal in
  0.6.0
- Added notes to indicate when functions, classes, & methods were added
- Added the following 12 tokenizers:
    - QSkipgrams
    - CharacterTokenizer
    - RegexpTokenizer, WhitespaceTokenizer, & WordpunctTokenizer
    - COrVClusterTokenizer, CVClusterTokenizer, & VCClusterTokenizer
    - SonoriPyTokenizer & LegaliPyTokenizer
    - NLTKTokenizer
    - SAPSTokenizer
- Added the UnigramCorpus class & a facility for downloading data, such as
  pre-processed/trained data, from storage on GitHub
- Added the Wåhlin phonetic encoding
- Added the following 211 similarity/distance/correlation measures:
    - ALINE
    - AMPLE
    - Anderberg
    - Andres & Marzo's Delta
    - Average Linkage
    - AZZOO
    - Baroni-Urbani & Buser I & II
    - Batagelj & Bren
    - Baulieu I-XV
    - Benini I & II
    - Bennet
    - Bhattacharyya
    - BI-SIM
    - BLEU
    - Block Levenshtein
    - Brainerd-Robinson
    - Braun-Blanquet
    - Canberra
    - Chord
    - Clement
    - Cohen's Kappa
    - Cole
    - Complete Linkage
    - Consonni & Todeschini I-V
    - Cormode's LZ
    - Covington
    - Dennis
    - Dice Asymmetric I & II
    - Digby
    - Dispersion
    - Doolittle
    - Dunning
    - Eyraud
    - Fager & McGowan
    - Faith
    - Fellegi-Sunter
    - Fidelity
    - Fleiss
    - Fleiss-Levin-Paik
    - FlexMetric
    - Forbes I & II
    - Fossum
    - FuzzyWuzzy Partial String
    - FuzzyWuzzy Token Set
    - FuzzyWuzzy Token Sort
    - Generalized Fleiss
    - Gilbert
    - Gilbert & Wells
    - Gini I & II
    - Goodall
    - Goodman & Kruskal's Lambda
    - Goodman & Kruskal's Lambda-r
    - Goodman & Kruskal's Tau A & B
    - Gower & Legendre
    - Guttman's Lambda A & B
    - Gwet's AC
    - Hamann
    - Harris & Lahey
    - Hassanat
    - Hawkins & Dotson
    - Hellinger
    - Higuera & Mico
    - Hurlbert
    - Iterative SubString
    - Jaccard-NM
    - Jensen-Shannon
    - Johnson
    - Kendall's Tau
    - Kent & Foster I & II
    - Koppen I & II
    - Kuder & Richardson
    - Kuhns I-XII
    - Kulczynski I & II
    - Longest Common Prefix
    - Longest Common Suffix
    - Lorentzian
    - Maarel
    - Marking
    - Marking Metric
    - MASI
    - Matusita
    - Maxwell & Pilliner
    - McConnaughey
    - McEwen & Michael
    - MetaLevenshtein
    - Michelet
    - MinHash
    - Mountford
    - Mean Squared Contingency
    - Mutual Information
    - NCD with LZSS
    - NCD with PAQ9a
    - Ozbay
    - Pattern
    - Pearson's Chi-Squared
    - Pearson & Heron II
    - Pearson II & III
    - Pearson's Phi
    - Peirce
    - Positional Q-Gram Dice, Jaccard, & Overlap
    - Q-Gram
    - Quantitative Cosine, Dice, & Jaccard
    - Rees-Levenshtein
    - Roberts
    - Rogers & Tanimoto
    - Rogot & Goldberg
    - Rouge-L, -S, -SU, & -W
    - Russell & Rao
    - SAPS
    - Scott's Pi
    - Shape
    - Shapira & Storer I
    - Sift4 Extended
    - Single Linkage
    - Size
    - Soft Cosine
    - SoftTF-IDF
    - Sokal & Michener
    - Sokal & Sneath I-V
    - Sorgenfrei
    - Steffensen
    - Stiles
    - Stuart's Tau
    - Tarantula
    - Tarwid
    - Tetrachoric
    - TF-IDF
    - Tichy
    - Tulloss's R, S, T, & U
    - Unigram Subtuple
    - Unknown A-M
    - Upholt
    - Warrens I-V
    - Weighted Jaccard
    - Whittaker
    - Yates' Chi-Squared
    - YJHHR
    - Yujian & Bo
    - Yule's Q, Q II, & Y
- Four intersection types are now supported for all distance measure that are
  based on _TokenDistance. In addition to basic crisp intersections, soft,
  fuzzy, and group linkage intersections have been provided.


0.3.6 (2018-11-17) *classy carl*
++++++++++++++++++++++++++++++++

doi:10.5281/zenodo.1490537

Changes:

- Most functions were encapsulated into classes.
- Each class is broken out into its own file, with test files paralleling
  library files.
- Documentation was converted from Sphinx markup to Numpy style.
- A tutorial was written for each subpackage.
- Documentation was cleaned up, with math markup corrections and many
  additional links.


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
   - S stemmer
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
