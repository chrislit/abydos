============
  Tutorial
============

There are nine major packages that make up Abydos:

    - :py:mod:`.compression` for string compression classes
    - :py:mod:`.corpus` for document corpus classes
    - :py:mod:`.distance` for string distance measure & metric classes
    - :py:mod:`.fingerprint` for string fingerprint classes
    - :py:mod:`.phones` for functions relating to phones and phonemes
    - :py:mod:`.phonetic` for phonetic algorithm classes
    - :py:mod:`.stats` for statistical functions and a confusion table class
    - :py:mod:`.stemmer` for stemming classes
    - :py:mod:`.tokenizer` for tokenizer classes

Classes with each package have consistent method names, as discussed below.
A tenth package, :py:mod:`.util`, contains functions not intended for end-user
use.


Compression
-----------

The :py:mod:`.compression` package provides the string compression classes:

    - :py:class:`.Arithmetic` for arithmetic coding
    - :py:class:`.BWT` for Burrows-Wheeler Transform
    - :py:class:`.RLE` for Run-Length Encoding

Each class provides ``encode`` and ``decode`` methods for performing and
reversing its encoding. For example, the Burrows-Wheeler Transform can be
performed by creating a :py:class:`.BWT` object and then calling
:py:meth:`.BWT.encode` on a string:

>>> bwt = BWT()
>>> bwt.encode('^BANANA')
'ANNB^AA\x00'


Corpus
------

The :py:mod:`.corpus` package provides :py:class:`.Corpus` and
:py:class:`.NGramCorpus` classes.

As a quick example of :py:class:`.Corpus`:

>>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
>>> tqbf += 'And then it slept.\n And the dog ran off.'
>>> corp = Corpus(tqbf)
>>> corp.docs()
[[['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
'dog.'], ['And', 'then', 'it', 'slept.'], ['And', 'the', 'dog',
'ran', 'off.']]]
>>> round(corp.idf('dog'), 10)
0.4771212547
>>> round(corp.idf('the'), 10)
0.1760912591

Here, each sentence is a separate "document". We can retrieve IDF values from
the :py:class:`.Corpus`. The same :py:class:`.Corpus` can be used to initialize
an :py:class:`.NGramCorpus` and calculate TF values:

>>> ngcorp = NGramCorpus(corp)
>>> ngcorp.get_count('the')
2
>>> ngcorp.get_count('fox')
1
>>> ngcorp.tf('the')
1.3010299956639813
>>> ngcorp.tf('fox')
1.0


Distance
--------

The :py:mod:`.distance` package provides a growing list of string distance
measure and metric classes.

These include traditional Levenshtein edit distance and related algorithms:

    - Levenshtein distance (:py:class:`.Levenshtein`)
    - Optimal String Alignment distance (:py:class:`.Levenshtein` with
      ``mode='osa'``)
    - Damerau-Levenshtein distance (:py:class:`.DamerauLevenshtein`)
    - Indel distance (:py:class:`.Indel`)

Hamming distance (:py:class:`.Hamming`) and the closely related Modified
Language-Independent Product Name Search distance (:py:class:`.MLIPNS`) are
provided.

Distance metrics developed for the US Census are included:

    - Jaro distance (:py:class:`.JaroWinkler` with ``mode='Jaro'``)
    - Jaro-Winkler distance (:py:class:`.JaroWinkler`)
    - Strcmp95 distance (:py:class:`.Strcmp95`)

A large set of multi-set token-based distance metrics are provided, including:

    - Generalized Minkowski distance (:py:class:`.Minkowski`)
    - Manhattan distance (:py:class:`.Manhattan`)
    - Euclidean distance (:py:class:`.Euclidean`)
    - Chebyshev distance (:py:class:`.Chebyshev`)
    - Generalized Tversky distance (:py:class:`.Tversky`)
    - Sørensen–Dice coefficient (:py:class:`.Dice`)
    - Jaccard similarity (:py:class:`.Jaccard`)
    - Tanimoto coefficient (:py:meth:`.Jaccard.tanimoto_coeff`)
    - Overlap distance (:py:class:`.Overlap`)
    - Cosine similarity (:py:class:`.Cosine`)
    - Bag distance (:py:class:`.Bag`)
    - Monge-Elkan distance (:py:class:`.MongeElkan`)

Three popular sequence alignment algorithms are provided:

    - Needleman-Wunsch score (:py:class:`.NeedlemanWunsch`)
    - Smith-Waterman score (:py:class:`.SmithWaterman`)
    - Gotoh score (:py:class:`.Gotoh`)

Classes relating to substring and subsequence distances include:

    - Longest common subsequence (:py:class:`.LCSseq`)
    - Longest common substring (:py:class:`.LCSstr`)
    - Ratcliff-Obserhelp distance (:py:class:`.RatcliffObershelp`)

A number of simple distance classes provided in the package include:

    - Identity distance (:py:class:`.Ident`)
    - Length distance (:py:class:`.Length`)
    - Prefix distance (:py:class:`.Prefix`)
    - Suffix distance (:py:class:`.Suffix`)

Normalized compression distance classes for a variety of compression algorithms
are provided:

    - zlib (:py:class:`.NCDzlib`)
    - bzip2 (:py:class:`.NCDbz2`)
    - lzma (:py:class:`.NCDlzma`)
    - arithmetic coding (:py:class:`.NCDarith`)
    - BWT plus RLE (:py:class:`.NCDbwtrle`)
    - RLE (:py:class:`.NCDrle`)

The remaining distance measures & metrics include:

    - Western Airlines' Match Rating Algorithm comparison
      (:py:class:`.distance.MRA`)
    - Editex (:py:class:`.Editex`)
    - Bavarian Landesamt für Statistik distance (:py:class:`.Baystat`)
    - Eudex distance (:py:class:`.distance.Eudex`)
    - Sift4 distance (:py:class:`.Sift4` and :py:class:`.Sift4Simplest`)
    - Typo distance (:py:class:`.Typo`)
    - Synoname (:py:class:`.Synoname`)


Most of the distance and similarity measures have ``sim`` and ``dist`` methods,
which return a measure that is normalized to the range :math:`[0, 1]`. The
normalized distance and similarity are always complements, so the normalized
distance will always equal 1 - the similarity for a particular measure supplied
with the same input. Some measures have an absolute distance method
``dist_abs`` that is not limited to any range.

All three methods can be demonstrated using the :py:class:`.DamerauLevenshtein`
class:

>>> dl = DamerauLevenshtein()
>>> dl.dist_abs('orange', 'strange')
2
>>> dl.dist('orange', 'strange')
0.2857142857142857
>>> dl.sim('orange', 'strange')
0.7142857142857143


Fingerprint
-----------

The :py:mod:`.fingerprint` package provides numerous string fingerprint
algorithms, including:

    - Basic fingerprinters originating in `OpenRefine <http://openrefine.org>`:

        - String (:py:class:`.String`)
        - Phonetic, which applies a phonetic algorithm and returns the string
          fingerprint of the result (:py:class:`.Phonetic`)
        - QGram, which applies Q-gram tokenization and returns the string
          fingerprint of the result (:py:class:`.QGram`)

    - Fingerprints developed by Pollock & Zomora:

        - Skeleton key (:py:class:`.SkeletonKey`)
        - Omission key (:py:class:`.OmissionKey`)

    - Fingerprints developed by Cisłak & Grabowski:

        - Occurrence (:py:class:`.Occurrence`)
        - Occurrence halved (:py:class:`.OccurrenceHalved`)
        - Count (:py:class:`.Count`)
        - Position (:py:class:`.Position`)

    - The Synoname toolcode (:py:class:`.SynonameToolcode`)


Each fingerprint class has a ``fingerprint`` method that takes a string and
returns the string's fingerprint:

>>> sk = SkeletonKey()
>>> sk.fingerprint('orange')
'ORNGAE'
>>> sk.fingerprint('strange')
'STRNGAE'


Phones
------

The `phones` package has three functions:

    - :py:func:`.ipa_to_features` takes a string of IPA symbols and returns
      list of integers that represent the phonetic features bundled in the
      phone that the symbols represents.
    - :py:func:`.get_feature` takes a list of feature bundles produced by
      :py:func:`.ipa_to_features` and a feature name and returns a list
      representing whether that feature is present in each component of the
      list.
    - :py:func:`.cmp_features` takes two phonetic feature bundles, such as the
      components of the lists returned by :py:func:`.ipa_to_features`, and
      returns a measure of their similarity.


An example using these functions on two different pronunciations of the word
'international':

>>> int1 = 'ɪntənæʃənəɫ'
>>> int2 = 'ɪnɾənæʃɨnəɫ'
>>> feat1 = ipa_to_features(int1)
>>> feat1
[1826957413067434410,
 2711173160463936106,
 2783230754502126250,
 1828083331160779178,
 2711173160463936106,
 1826957425885227434,
 2783231556184615322,
 1828083331160779178,
 2711173160463936106,
 1828083331160779178,
 2693158721554917798]
>>> feat2 = ipa_to_features(int2)
>>> feat2
[1826957413067434410,
 2711173160463936106,
 2711173160463935914,
 1828083331160779178,
 2711173160463936106,
 1826957425885227434,
 2783231556184615322,
 1826957414069873066,
 2711173160463936106,
 1828083331160779178,
 2693158721554917798]
>>> get_feature(feat1, 'consonantal')
[-1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
>>> get_feature(feat1, 'nasal')
[-1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1]
>>> [cmp_features(f1, f2) for f1, f2 in zip(feat1, feat2)]
[1.0,
 1.0,
 0.9032258064516129,
 1.0,
 1.0,
 1.0,
 1.0,
 0.9193548387096774,
 1.0,
 1.0,
 1.0]
>>> sum(cmp_features(f1, f2) for f1, f2 in zip(feat1, feat2))/len(feat1)
0.9838709677419355


Phonetic
--------

The :py:mod:`.phonetic` package includes classes for phonetic algorithms,
including:

    - Robert C. Russell's Index (:py:class:`.RussellIndex`)
    - American Soundex (:py:class:`.Soundex`)
    - Refined Soundex (:py:class:`.RefinedSoundex`)
    - Daitch-Mokotoff Soundex (:py:class:`.DaitchMokotoff`)
    - NYSIIS (:py:class:`.NYSIIS`)
    - Match Rating Algorithm (:py:class:`.phonetic.MRA`)
    - Metaphone (:py:class:`.Metaphone`)
    - Double Metaphone (:py:class:`.DoubleMetaphone`)
    - Caverphone (:py:class:`.Caverphone`)
    - Alpha Search Inquiry System (:py:class:`.AlphaSIS`)
    - Fuzzy Soundex (:py:class:`.FuzzySoundex`)
    - Phonex (:py:class:`.Phonex`)
    - Phonem (:py:class:`.Phonem`)
    - Phonix (:py:class:`.Phonix`)
    - Standardized Phonetic Frequency Code (:py:class:`.SPFC`)
    - Statistics Canada (:py:class:`.StatisticsCanada`)
    - Lein (:py:class:`.Lein`)
    - Roger Root (:py:class:`.RogerRoot`)
    - Eudex phonetic hash (:py:class:`.phonetic.Eudex`)
    - Parmar-Kumbharana (:py:class:`.ParmarKumbharana`)
    - Davidson's Consonant Code (:py:class:`.Davidson`)
    - SoundD (:py:class:`.SoundD`)
    - PSHP Soundex/Viewex Coding (:py:class:`.PSHPSoundexFirst` and
      :py:class:`.PSHPSoundexLast`)
    - Dolby Code (:py:class:`.Dolby`)
    - NRL English-to-phoneme (:py:class:`.NRL`)
    - Beider-Morse Phonetic Matching (:py:class:`.BeiderMorse`)

There are also language-specific phonetic algorithms for German:

    - Kölner Phonetik (:py:class:`.Koelner`)
    - phonet (:py:class:`.Phonet`)
    - Haase Phonetik (:py:class:`.Haase`)
    - Reth-Schek Phonetik (:py:class:`.RethSchek`)

For French:

    - FONEM (:py:class:`.FONEM`)
    - an early version of Henry Code (:py:class:`.HenryEarly`)

For Spanish:

    - Phonetic Spanish (:py:class:`.PhoneticSpanish`)
    - Spanish Metaphone (:py:class:`.SpanishMetaphone`)

For Swedish:

    - SfinxBis (:py:class:`.SfinxBis`)

For Norwegian:

    - Norphone (:py:class:`.Norphone`)

For Brazilian Portuguese:

    - SoundexBR (:py:class:`.SoundexBR`)

And there are some hybrid phonetic algorithms that employ multiple underlying
phonetic algorithms:

    - Oxford Name Compression Algorithm (ONCA) (:py:class:`.ONCA`)
    - MetaSoundex (:py:class:`.MetaSoundex`)


Each class has an ``encode`` method to return the phonetically encoded string.
Classes for which ``encode`` returns a numeric value generally have an
``encode_alpha`` method that returns an alphabetic version of the phonetic
encoding, as demonstrated below:

>>> rus = RussellIndex()
>>> rus.encode('Abramson')
128637
>>> rus.encode_alpha('Abramson')
'ABRMCN'


Stats
-----

The :py:mod:`.stats` package includes numerous statistical functions and a
confusion table class:

The basic statistical functions include:

    - arithmetic mean (:py:func:`.amean`)
    - geometric mean (:py:func:`.gmean`)
    - harmonic mean (:py:func:`.hmean`)
    - quadratic mean (:py:func:`.qmean`)
    - contraharmonic mean (:py:func:`.cmean`)
    - logarithmic mean (:py:func:`.lmean`)
    - identric (exponential) mean (:py:func:`.imean`)
    - Seiffert's mean (:py:func:`.seiffert_mean`)
    - Lehmer mean (:py:func:`.lehmer_mean`)
    - Heronian mean (:py:func:`.heronian_mean`)
    - Hölder (power/generalized) mean (:py:func:`.hoelder_mean`)
    - arithmetic-geometric mean (:py:func:`.agmean`)
    - geometric-harmonic mean (:py:func:`.ghmean`)
    - arithmetic-geometric-harmonic mean (:py:func:`.aghmean`)
    - midrange (:py:func:`.midrange`)
    - median (:py:func:`.median`)
    - mode (:py:func:`.mode`)
    - variance (:py:func:`.var`)
    - standard deviation (:py:func:`.std`)

Some examples of the basic functions:

>>> nums = [16, 49, 55, 49, 6, 40, 23, 47, 29, 85, 76, 20]
>>> amean(nums)
41.25
>>> aghmean(nums)
32.42167170892585
>>> heronian_mean(nums)
37.931508950381925
>>> mode(nums)
49
>>> std(nums)
22.876935255113754


Two pairwise functions are provided:

    - mean pairwise similarity (:py:func:`.mean_pairwise_similarity`), which
      returns the mean similarity (using a supplied similarity function) among
      each item in a collection
    - pairwise similarity statistics
      (:py:func:`.pairwise_similarity_statistics`), which returns the max, min,
      mean, and standard deviation of pairwise similarities between two
      collections

The confusion table class (:py:class:`.ConfusionTable`) can be constructed in
a number of ways:

    - four values, representing true positives, true negatives,
      false positives, and false negatives, can be passed to the constructor
    - a list or tuple with four values, representing true positives,
      true negatives, false positives, and false negatives, can be passed to
      the constructor
    - a dict with keys 'tp', 'tn', 'fp', 'fn', each assigned to the values for
      true positives, true negatives, false positives, and false negatives
      can be passed to the constructor

The :py:class:`.ConfusionTable` class has methods:

    - :py:meth:`.to_tuple` extracts the :py:class:`.ConfusionTable` values as a
      tuple: (:math:`w`, :math:`x`, :math:`y`, :math:`z`)
    - :py:meth:`.to_dict` extracts the :py:class:`.ConfusionTable` values as a
      dict: {'tp'::math:`w`, 'tn'::math:`x`, 'fp'::math:`y`, 'fn'::math:`z`}
    - :py:meth:`.true_pos` returns the number of true positives
    - :py:meth:`.true_neg` returns the number of true negatives
    - :py:meth:`.false_pos` returns the number of false positives
    - :py:meth:`.false_neg` returns the number of false negatives
    - :py:meth:`.correct_pop` returns the correct population
    - :py:meth:`.error_pop` returns the error population
    - :py:meth:`.test_pos_pop` returns the test positive population
    - :py:meth:`.test_neg_pop` returns the test negative population
    - :py:meth:`.cond_pos_pop` returns the condition positive population
    - :py:meth:`.cond_neg_pop` returns the condition negative population
    - :py:meth:`.population` returns the total population
    - :py:meth:`.precision` returns the precision
    - :py:meth:`.precision_gain` returns the precision gain
    - :py:meth:`.recall` returns the recall
    - :py:meth:`.specificity` returns the specificity
    - :py:meth:`.npv` returns the negative predictive value
    - :py:meth:`.fallout` returns the fallout
    - :py:meth:`.fdr` returns the false discovery rate
    - :py:meth:`.accuracy` returns the accuracy
    - :py:meth:`.accuracy_gain` returns the accuracy gain
    - :py:meth:`.balanced_accuracy` returns the balanced accuracy
    - :py:meth:`.informedness` returns the informedness
    - :py:meth:`.markedness` returns the markedness
    - :py:meth:`.pr_amean` returns the arithmetic mean of precision & recall
    - :py:meth:`.pr_gmean` returns the geometric mean of precision & recall
    - :py:meth:`.pr_hmean` returns the harmonic mean of precision & recall
    - :py:meth:`.pr_qmean` returns the quadratic mean of precision & recall
    - :py:meth:`.pr_cmean` returns the contraharmonic mean of precision &
      recall
    - :py:meth:`.pr_lmean` returns the logarithmic mean of precision & recall
    - :py:meth:`.pr_imean` returns the identric mean of precision & recall
    - :py:meth:`.pr_seiffert_mean` returns Seiffert's mean of precision &
      recall
    - :py:meth:`.pr_lehmer_mean` returns the Lehmer mean of precision & recall
    - :py:meth:`.pr_heronian_mean` returns the Heronian mean of precision &
      recall
    - :py:meth:`.pr_hoelder_mean` returns the Hölder mean of precision & recall
    - :py:meth:`.pr_agmean` returns the arithmetic-geometric mean of precision
      & recall
    - :py:meth:`.pr_ghmean` returns the geometric-harmonic mean of precision &
      recall
    - :py:meth:`.pr_aghmean` returns the arithmetic-geometric-harmonic mean of
      precision & recall
    - :py:meth:`.fbeta_score` returns the :math:`F_{beta}` score
    - :py:meth:`.f2_score` returns the :math:`F_2` score
    - :py:meth:`.fhalf_score` returns the :math:`F_{\frac{1}{2}}` score
    - :py:meth:`.e_score` returns the :math:`E` score
    - :py:meth:`.f1_score` returns the :math:`F_1` score
    - :py:meth:`.f_measure` returns the F measure
    - :py:meth:`.g_measure` returns the G measure
    - :py:meth:`.mcc` returns Matthews correlation coefficient
    - :py:meth:`.significance` returns the significance
    - :py:meth:`.kappa_statistic` returns the Kappa statistic

>>> ct = ConfusionTable(120, 60, 20, 30)
>>> ct.f1_score()
0.8275862068965516
>>> ct.mcc()
0.5367450401216932
>>> ct.specificity()
0.75
>>> ct.significance()
66.26190476190476


The :py:class:`.ConfusionTable` class also supports checking for equality with
another :py:class:`.ConfusionTable` and casting to string with ``str()``:

>>> ConfusionTable({'tp':120, 'tn':60, 'fp':20, 'fn':30}) ==
... ConfusionTable(120, 60, 20, 30)
True
>>> str(ConfusionTable(120, 60, 20, 30))
'tp:120, tn:60, fp:20, fn:30'


Stemmer
-------

The :py:mod:`stemmer` package collects stemmer classes for a number of
languages including:

    - English stemmers:

        - Lovins' (:py:class:`.Lovins`)
        - Porter (:py:class:`.Porter`)
        - Porter2 (i.e. Snowball English) (:py:class:`.Porter2`)
        - UEA-Lite (:py:class:`.UEALite`)
        - Paice-Husk (:py:class:`.PaiceHusk`)
        - S-stemmer (:py:class:`.SStemmer`)

    - German stemmers:

        - Caumanns' (:py:class:`.Caumanns`)
        - CLEF German (:py:class:`.CLEFGerman`)
        - CLEF German Plus (:py:class:`.CLEFGermanPlus`)
        - Snowball German (:py:class:`.SnowballGerman`)

    - Swedish stemmers:

        - CLEF Swedish (:py:class:`.CLEFSwedish`)
        - Snowball Swedish (:py:class:`.SnowballSwedish`)

    - Latin stemmer:

        - Schinke (:py:class:`.Schinke`)

    - Danish stemmer:

        - Snowball Danish (:py:class:`.SnowballDanish`)

    - Dutch stemmer:

        - Snowball Dutch (:py:class:`.SnowballDutch`)

    - Norwegian stemmer:

        - Snowball Norwegian (:py:class:`.SnowballNorwegian`)


Each stemmer has a ``stem`` method, which takes a word and returns its stemmed
form:

>>> stmr = Porter()
>>> stmr.stem('democracy')
'democraci'
>>> stmr.stem('trusted')
'trust'



Tokenizer
---------

The :py:mod:`tokenizer` package collects classes whose purpose is to tokenize
text. Currently, this is limited to the :py:class:`.QGrams` class, which
tokenizes a string into q-grams. The class supports different values of
q, the addition of start and stop symbols, and skip values. It even supports
multiple values for q and skip, using lists or ranges.

>>> QGrams('interning', qval=2, start_stop='$#')
QGrams({'$i': 1,
        'in': 2,
        'nt': 1,
        'te': 1,
        'er': 1,
        'rn': 1,
        'ni': 1,
        'ng': 1,
        'g#': 1})

>>> QGrams('AACTAGAAC', start_stop='', skip=1)
QGrams({'AC': 2, 'AT': 1, 'CA': 1, 'TG': 1, 'AA': 1, 'GA': 1, 'A': 1})

>>> QGrams('AACTAGAAC', start_stop='', skip=[0, 1])
QGrams({'AA': 3,
        'AC': 4,
        'CT': 1,
        'TA': 1,
        'AG': 1,
        'GA': 2,
        'AT': 1,
        'CA': 1,
        'TG': 1,
        'A': 1})

>>> QGrams('interdisciplinarian', qval=range(3), skip=[0, 1])
QGrams({'i': 10,
        'n': 7,
        't': 2,
        'e': 2,
        'r': 4,
        'd': 2,
        's': 2,
        'c': 2,
        'p': 2,
        'l': 2,
        'a': 4,
        '$i': 1,
        'in': 3,
        'nt': 1,
        'te': 1,
        'er': 1,
        'rd': 1,
        'di': 1,
        'is': 1,
        'sc': 1,
        'ci': 1,
        'ip': 1,
        'pl': 1,
        'li': 1,
        'na': 1,
        'ar': 1,
        'ri': 2,
        'ia': 2,
        'an': 1,
        'n#': 1,
        '$n': 1,
        'it': 1,
        'ne': 1,
        'tr': 1,
        'ed': 1,
        'ds': 1,
        'ic': 1,
        'si': 1,
        'cp': 1,
        'il': 1,
        'pi': 1,
        'ln': 1,
        'nr': 1,
        'ai': 1,
        'ra': 1,
        'a#': 1})
