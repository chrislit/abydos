# -*- coding: utf-8 -*-

# Copyright 2014-2015 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.distance

The distance module implements string edit distance functions including:

    - Levenshtein distance (incl. a [0, 1] normalized variant)
    - Optimal String Alignment distance (incl. a [0, 1] normalized variant)
    - Levenshtein-Damerau distance (incl. a [0, 1] normalized variant)
    - Hamming distance (incl. a [0, 1] normalized variant)
    - Tversky index
    - Sørensen–Dice coefficient & distance
    - Jaccard similarity coefficient & distance
    - overlap similarity & distance
    - Tanimoto coefficient & distance
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
    - Bag distance (incl. a [0, 1] normalized variant)
    - Editex distance (incl. a [0, 1] normalized variant)
    - TF-IDF similarity

Functions beginning with the prefixes 'sim' and 'dist' are guaranteed to be
in the range [0, 1], and sim_X = 1 - dist_X since the two are complements.
If a sim_X function is supplied identical src & tar arguments, it is guaranteed
to return 1; the corresponding dist_X function is guaranteed to return 0.
"""

from __future__ import unicode_literals
from __future__ import division
from ._compat import _range, _unicode
import numpy
import sys
import math
from collections import defaultdict, Counter
from .qgram import QGrams
from .phonetic import mra
import codecs
from .compression import ac_train, ac_encode, rle_encode
import unicodedata
try:
    import lzma
except ImportError:  # pragma: no cover
    # If the system lacks the lzma library, that's fine, but lzma comrpession
    # similarity won't be supported.
    pass


def levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Levenshtein distance

    This is the standard edit distance measure. Cf.
    https://en.wikipedia.org/wiki/Levenshtein_distance

    Two additional variants: optimal string alignment (aka restricted
    Damerau-Levenshtein distance) and the Damerau-Levenshtein distance
    are also supported. Cf.
    https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

    The ordinary Levenshtein & Optimal String Alignment distance both
    employ the Wagner-Fischer dynamic programming algorithm. Cf.
    https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm

    Levenshtein edit distance ordinarily has unit insertion, deletion, and
    substitution costs.

    :param str src, tar: two strings to be compared
    :param str mode: specifies a mode for computing the Levenshtein distance:

        - 'lev' (default) computes the ordinary Levenshtein distance,
          in which edits may include inserts, deletes, and substitutions
        - 'osa' computes the Optimal String Alignment distance, in which
          edits may include inserts, deletes, substitutions, and
          transpositions but substrings may only be edited once
        - 'dam' computes the Damerau-Levenshtein distance, in which
          edits may include inserts, deletes, substitutions, and
          transpositions and substrings may undergo repeated edits

    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits: inserts, deletes, substitutions, and transpositions,
        respectively (by default: (1, 1, 1, 1))
    :returns: the Levenshtein distance between src & tar
    :rtype: int (may return a float if cost has float values)

    >>> levenshtein('cat', 'hat')
    1
    >>> levenshtein('Niall', 'Neil')
    3
    >>> levenshtein('aluminum', 'Catalan')
    7
    >>> levenshtein('ATCG', 'TAGC')
    3

    >>> levenshtein('ATCG', 'TAGC', mode='osa')
    2
    >>> levenshtein('ACTG', 'TAGC', mode='osa')
    4

    >>> levenshtein('ATCG', 'TAGC', mode='dam')
    2
    >>> levenshtein('ACTG', 'TAGC', mode='dam')
    3
    """
    ins_cost, del_cost, sub_cost, trans_cost = cost

    if src == tar:
        return 0
    if len(src) == 0:
        return len(tar) * ins_cost
    if len(tar) == 0:
        return len(src) * del_cost

    if 'dam' in mode:
        return damerau_levenshtein(src, tar, cost)

    # pylint: disable=no-member
    d_mat = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.int)
    # pylint: enable=no-member
    for i in _range(len(src)+1):
        d_mat[i, 0] = i * del_cost
    for j in _range(len(tar)+1):
        d_mat[0, j] = j * ins_cost

    for i in _range(len(src)):
        for j in _range(len(tar)):
            d_mat[i+1, j+1] = min(
                d_mat[i+1, j] + ins_cost,  # ins
                d_mat[i, j+1] + del_cost,  # del
                d_mat[i, j] + (sub_cost if src[i] != tar[j] else 0)  # sub/==
            )

            if mode == 'osa':
                if ((i+1 > 1 and j+1 > 1 and src[i] == tar[j-1] and
                     src[i-1] == tar[j])):
                    d_mat[i+1, j+1] = min(d_mat[i+1, j+1],
                                          d_mat[i-1, j-1] + trans_cost  # trans
                                          )

    return d_mat[len(src), len(tar)]


def dist_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Levenshtein distance normalized to the interval [0, 1]

    The Levenshtein distance is normalized by dividing the Levenshtein distance
    (calculated by any of the three supported methods) by the greater of
    the number of characters in src times the cost of a delete and
    the number of characters in tar times the cost of an insert.
    For the case in which all operations have :math:`cost = 1`, this is
    equivalent to the greater of the length of the two strings src & tar.

    :param str src, tar: two strings to be compared
    :param str mode: specifies a mode for computing the Levenshtein distance:

        - 'lev' (default) computes the ordinary Levenshtein distance,
          in which edits may include inserts, deletes, and substitutions
        - 'osa' computes the Optimal String Alignment distance, in which
          edits may include inserts, deletes, substitutions, and
          transpositions but substrings may only be edited once
        - 'dam' computes the Damerau-Levenshtein distance, in which
          edits may include inserts, deletes, substitutions, and
          transpositions and substrings may undergo repeated edits

    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits: inserts, deletes, substitutions, and transpositions,
        respectively (by default: (1, 1, 1, 1))
    :returns: normalized Levenshtein distance
    :rtype: float

    >>> dist_levenshtein('cat', 'hat')
    0.33333333333333331
    >>> dist_levenshtein('Niall', 'Neil')
    0.59999999999999998
    >>> dist_levenshtein('aluminum', 'Catalan')
    0.875
    >>> dist_levenshtein('ATCG', 'TAGC')
    0.75
    """
    if src == tar:
        return 0
    ins_cost, del_cost = cost[:2]
    return (levenshtein(src, tar, mode, cost) /
            (max(len(src)*del_cost, len(tar)*ins_cost)))


def sim_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Levenshtein similarity normalized to the interval [0, 1]

    Levenshtein similarity the complement of Levenshtein distance:
    :math:`sim_{Levenshtein} = 1 - dist_{Levenshtein}`

    The arguments are identical to those of the levenshtein() function.

    :param str src, tar: two strings to be compared
    :param str mode: specifies a mode for computing the Levenshtein distance:

            - 'lev' (default) computes the ordinary Levenshtein distance,
              in which edits may include inserts, deletes, and substitutions
            - 'osa' computes the Optimal String Alignment distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions but substrings may only be edited once
            - 'dam' computes the Damerau-Levenshtein distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions and substrings may undergo repeated edits

    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits:
        inserts, deletes, substitutions, and transpositions, respectively
        (by default: (1, 1, 1, 1))
    :returns: normalized Levenshtein similarity
    :rtype: float

    >>> sim_levenshtein('cat', 'hat')
    0.66666666666666674
    >>> sim_levenshtein('Niall', 'Neil')
    0.40000000000000002
    >>> sim_levenshtein('aluminum', 'Catalan')
    0.125
    >>> sim_levenshtein('ATCG', 'TAGC')
    0.25
    """
    return 1 - dist_levenshtein(src, tar, mode, cost)


def damerau_levenshtein(src, tar, cost=(1, 1, 1, 1)):
    """Damerau-Levenshtein distance

    This computes the Damerau-Levenshtein distance. Cf.
    https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

    Damerau-Levenshtein code based on Java code by Kevin L. Stern,
    under the MIT license:
    https://github.com/KevinStern/software-and-algorithms/blob/master/src/main/java/blogspot/software_and_algorithms/stern_library/string/DamerauLevenshteinAlgorithm.java

    :param str src, tar: two strings to be compared
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits:
        inserts, deletes, substitutions, and transpositions, respectively
        (by default: (1, 1, 1, 1))
    :returns: the Damerau-Levenshtein distance between src & tar
    :rtype: int (may return a float if cost has float values)
    """
    ins_cost, del_cost, sub_cost, trans_cost = cost

    if src == tar:
        return 0
    if len(src) == 0:
        return len(tar) * ins_cost
    if len(tar) == 0:
        return len(src) * del_cost

    if 2*trans_cost < ins_cost + del_cost:
        raise ValueError('Unsupported cost assignment; the cost of two ' +
                         'transpositions must not be less than the cost of ' +
                         'an insert plus a delete.')

    # pylint: disable=no-member
    d_mat = (numpy.zeros((len(src))*(len(tar)), dtype=numpy.int).
             reshape((len(src), len(tar))))
    # pylint: enable=no-member

    if src[0] != tar[0]:
        d_mat[0, 0] = min(sub_cost, ins_cost + del_cost)

    src_index_by_character = {}
    src_index_by_character[src[0]] = 0
    for i in _range(1, len(src)):
        del_distance = d_mat[i-1, 0] + del_cost
        ins_distance = (i+1) * del_cost + ins_cost
        match_distance = (i * del_cost +
                          (0 if src[i] == tar[0] else sub_cost))
        d_mat[i, 0] = min(del_distance, ins_distance, match_distance)

    for j in _range(1, len(tar)):
        del_distance = (j+1) * ins_cost + del_cost
        ins_distance = d_mat[0, j-1] + ins_cost
        match_distance = (j * ins_cost +
                          (0 if src[0] == tar[j] else sub_cost))
        d_mat[0, j] = min(del_distance, ins_distance, match_distance)

    for i in _range(1, len(src)):
        max_src_letter_match_index = (0 if src[i] == tar[0] else -1)
        for j in _range(1, len(tar)):
            candidate_swap_index = (-1 if tar[j] not in
                                    src_index_by_character else
                                    src_index_by_character[tar[j]])
            j_swap = max_src_letter_match_index
            del_distance = d_mat[i-1, j] + del_cost
            ins_distance = d_mat[i, j-1] + ins_cost
            match_distance = d_mat[i-1, j-1]
            if src[i] != tar[j]:
                match_distance += sub_cost
            else:
                max_src_letter_match_index = j

            if candidate_swap_index != -1 and j_swap != -1:
                i_swap = candidate_swap_index

                if i_swap == 0 and j_swap == 0:
                    pre_swap_cost = 0
                else:
                    pre_swap_cost = d_mat[max(0, i_swap-1), max(0, j_swap-1)]
                swap_distance = (pre_swap_cost + (i - i_swap - 1) *
                                 del_cost + (j - j_swap - 1) * ins_cost +
                                 trans_cost)
            else:
                swap_distance = sys.maxsize

            d_mat[i, j] = min(del_distance, ins_distance,
                              match_distance, swap_distance)
        src_index_by_character[src[i]] = i

    return d_mat[len(src)-1, len(tar)-1]


def dist_damerau(src, tar, cost=(1, 1, 1, 1)):
    """Damerau-Levenshtein distance normalized to the interval [0, 1]

    The Damerau-Levenshtein distance is normalized by dividing the
    Damerau-Levenshtein distance by the greater of
    the number of characters in src times the cost of a delete and
    the number of characters in tar times the cost of an insert.
    For the case in which all operations have :math:`cost = 1`, this is
    equivalent to the greater of the length of the two strings src & tar.

    The arguments are identical to those of the levenshtein() function.

    :param str src, tar: two strings to be compared
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits:
        inserts, deletes, substitutions, and transpositions, respectively
        (by default: (1, 1, 1, 1))
    :returns: normalized Damerau-Levenshtein distance
    :rtype: float
    """
    if src == tar:
        return 0
    ins_cost, del_cost = cost[:2]
    return (damerau_levenshtein(src, tar, cost) /
            (max(len(src)*del_cost, len(tar)*ins_cost)))


def sim_damerau(src, tar, cost=(1, 1, 1, 1)):
    """Levenshtein similarity normalized to the interval [0, 1]

    Damerau-Levenshtein similarity the complement of Damerau-Levenshtein
    distance:
    :math:`sim_{Damerau} = 1 - dist_{Damerau}`

    The arguments are identical to those of the levenshtein() function.

    :param str src, tar: two strings to be compared
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits:
        inserts, deletes, substitutions, and transpositions, respectively
        (by default: (1, 1, 1, 1))
    :returns: normalized Damerau-Levenshtein similarity
    :rtype: float
    """
    return 1 - dist_damerau(src, tar, cost)


def hamming(src, tar, difflens=True):
    """Hamming distance

    Hamming distance equals the number of character positions at which two
    strings differ. For strings of unequal lengths, it is not normally defined.
    By default, this implementation calculates the Hamming distance of the
    first n characters where n is the lesser of the two strings' lengths and
    adds to this the difference in string lengths.

    :param str src, tar: two strings to be compared
    :param bool allow_different_lengths:
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending
        the shorter string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.
    :returns: the Hamming distance between src & tar
    :rtype: int
    """
    if not difflens and len(src) != len(tar):
        raise ValueError('Undefined for sequences of unequal length; set ' +
                         'difflens to True for Hamming distance between ' +
                         'strings of unequal lengths.')

    hdist = 0
    if difflens:
        hdist += abs(len(src)-len(tar))
    hdist += sum(c1 != c2 for c1, c2 in zip(src, tar))

    return hdist


def dist_hamming(src, tar, difflens=True):
    """Hamming distance normalized to the interval [0, 1]

    The Hamming distance is normalized by dividing it
    by the greater of the number of characters in src & tar (unless difflens is
    set to False, in which case an exception is raised).

    The arguments are identical to those of the hamming() function.

    :param str src, tar: two strings to be compared
    :param bool allow_different_lengths:
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending
        the shorter string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.
    :returns: normalized Hamming distance
    :rtype: float
    """
    if src == tar:
        return 0
    return hamming(src, tar, difflens) / max(len(src), len(tar))


def sim_hamming(src, tar, difflens=True):
    """Hamming similarity normalized to the interval [0, 1]

    Hamming similarity is the complement of normalized Hamming distance:
    :math:`sim_{Hamming} = 1 - dist{Hamming}`

    Provided that difflens==True, the Hamming similarity is identical to the
    Language-Independent Product Name Search (LIPNS) similarity score. For
    further information, see the sim_mlipns documentation.

    The arguments are identical to those of the hamming() function.

    :param str src, tar: two strings to be compared
    :param bool allow_different_lengths:
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending
        the shorter string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.
    :returns: normalized Hamming similarity
    :rtype: float
    """
    return 1 - dist_hamming(src, tar, difflens)


def sim_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Tversky index

    The Tversky index is defined as:
    For two sets X and Y:
    :math:`sim_{Tversky}(X, Y) = \\frac{|X \\cap Y|}
    {|X \\cap Y| + \\alpha|X - Y| + \\beta|Y - X|}`

    Cf. https://en.wikipedia.org/wiki/Tversky_index

    :math:`\\alpha = \\beta = 1` is equivalent to the Jaccard & Tanimoto
    similarity coefficients.

    :math:`\\alpha = \\beta = 0.5` is equivalent to the Sørensen-Dice
    similarity coefficient.

    Unequal α and β will tend to emphasize one or the other set's
    contributions:

        - :math:`\\alpha > \\beta` emphasizes the contributions of X over Y
        - :math:`\\alpha < \\beta` emphasizes the contributions of Y over X)

    Parameter values' relation to 1 emphasizes different types of
    contributions:

        - :math:`\\alpha and \\beta > 1` emphsize unique contributions over the
          intersection
        - :math:`\\alpha and \\beta < 1` emphsize the intersection over unique
          contributions

    The symmetric variant is defined in Jiminez, Sergio, Claudio Becerra, and
    Alexander Gelbukh. 2013. SOFTCARDINALITY-CORE: Improving Text Overlap with
    Distributional Measures for Semantic Textual Similarity. This is activated
    by specifying a bias parameter.
    Cf. http://aclweb.org/anthology/S/S13/S13-1028.pdf

    :param str src, tar: two strings to be compared
        (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :param float alpha, beta: two Tversky index parameters as indicated in the
        description below
    :returns: Tversky similarity
    :rtype: float
    """
    if alpha < 0 or beta < 0:
        raise ValueError('Unsupported weight assignment; alpha and beta ' +
                         'must be greater than or equal to 0.')

    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0

    if isinstance(src, Counter) and isinstance(tar, Counter):
        q_src = src
        q_tar = tar
    elif qval and qval > 0:
        q_src = QGrams(src, qval)
        q_tar = QGrams(tar, qval)
    else:
        q_src = Counter(src.strip().split())
        q_tar = Counter(tar.strip().split())
    q_src_mag = sum(q_src.values())
    q_tar_mag = sum(q_tar.values())
    q_intersection_mag = sum((q_src & q_tar).values())

    if len(q_src) == 0 or len(q_tar) == 0:
        return 0.0

    if bias is None:
        return q_intersection_mag / (q_intersection_mag + alpha *
                                     (q_src_mag - q_intersection_mag) +
                                     beta * (q_tar_mag - q_intersection_mag))
    else:
        a_val = min(q_src_mag - q_intersection_mag,
                    q_tar_mag - q_intersection_mag)
        b_val = max(q_src_mag - q_intersection_mag,
                    q_tar_mag - q_intersection_mag)
        c_val = q_intersection_mag + bias
        return c_val / (beta * (alpha * a_val + (1 - alpha) * b_val) + c_val)


def dist_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Tversky distance

    Tversky distance is the complement of the Tvesrsky index (similarity):
    :math:`dist_{Tversky} = 1-sim_{Tversky}`

    The symmetric variant is defined in Jiminez, Sergio, Claudio Becerra, and
    Alexander Gelbukh. 2013. SOFTCARDINALITY-CORE: Improving Text Overlap with
    Distributional Measures for Semantic Textual Similarity. This is activated
    by specifying a bias parameter.
    Cf. http://aclweb.org/anthology/S/S13/S13-1028.pdf

    :param str src, tar: two strings to be compared
        (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :param float alpha, beta: two Tversky index parameters as indicated in the
        description below
    :returns: Tversky distance
    :rtype: float
    """
    return 1 - sim_tversky(src, tar, qval, alpha, beta, bias)


def sim_dice(src, tar, qval=2):
    """Sørensen–Dice coefficient

    For two sets X and Y, the Sørensen–Dice coefficient is
    :math:`sim_{dice}(X, Y) = \\frac{2 \\cdot |X \\cap Y|}{|X| + |Y|}`

    This is identical to the Tanimoto similarity coefficient
    and the Tversky index for :math:`\\alpha = \\beta = 0.5`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Sørensen–Dice similarity
    :rtype: float
    """
    return sim_tversky(src, tar, qval, 0.5, 0.5)


def dist_dice(src, tar, qval=2):
    """Sørensen–Dice distance

    Sørensen–Dice distance is the complemenjt of the Sørensen–Dice coefficient:
    :math:`dist_{dice} = 1 - sim_{dice}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Sørensen–Dice distance
    :rtype: float
    """
    return 1 - sim_dice(src, tar, qval)


def sim_jaccard(src, tar, qval=2):
    """Jaccard similarity coefficient

    For two sets X and Y, the Jaccard similarity coefficient is
    :math:`sim_{jaccard}(X, Y) = \\frac{|X \\cap Y|}{|X \\cup Y|}`

    This is identical to the Tanimoto similarity coefficient
    and the Tversky index for :math:`\\alpha = \\beta = 1`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Jaccard similarity
    :rtype: float
    """
    return sim_tversky(src, tar, qval, 1, 1)


def dist_jaccard(src, tar, qval=2):
    """Jaccard distance

    Jaccard distance is the complement of the Jaccard similarity coefficient:
    :math:`dist_{Jaccard} = 1 - sim_{Jaccard}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Jaccard distance
    :rtype: float
    """
    return 1 - sim_jaccard(src, tar, qval)


def sim_overlap(src, tar, qval=2):
    """overlap coefficient

    For two sets X and Y, the overlap coefficient is
    :math:`sim_{overlap}(X, Y) = \\frac{|X \\cap Y|}{min(|X|, |Y|)}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: overlap similarity
    :rtype: float
    """
    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0

    if isinstance(src, Counter) and isinstance(tar, Counter):
        q_src = src
        q_tar = tar
    elif qval and qval > 0:
        q_src = QGrams(src, qval)
        q_tar = QGrams(tar, qval)
    else:
        q_src = Counter(src.strip().split())
        q_tar = Counter(tar.strip().split())
    q_src_mag = sum(q_src.values())
    q_tar_mag = sum(q_tar.values())
    q_intersection_mag = sum((q_src & q_tar).values())

    return q_intersection_mag / min(q_src_mag, q_tar_mag)


def dist_overlap(src, tar, qval=2):
    """overlap distance

    Overlap distance is the complement of the overlap coefficient:
    :math:`sim_{overlap} = 1 - dist_{overlap}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: overlap distance
    :rtype: float
    """
    return 1 - sim_overlap(src, tar, qval)


def sim_tanimoto(src, tar, qval=2):
    """Tanimoto similarity

    For two sets X and Y, the Tanimoto similarity coefficient is
    :math:`sim_{Tanimoto}(X, Y) = \\frac{|X \\cap Y|}{|X \\cup Y|}`
    This is identical to the Jaccard similarity coefficient
    and the Tversky index for :math:`\\alpha = \\beta = 1`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Tanimoto similarity
    :rtype: float
    """
    return sim_jaccard(src, tar, qval)


def tanimoto(src, tar, qval=2):
    """Tanimoto distance

    Tanimoto distance is :math:`-log_{2}sim_{Tanimoto}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Tanimoto distance
    :rtype: float
    """
    coeff = sim_jaccard(src, tar, qval)
    if coeff != 0:
        return math.log(coeff, 2)
    else:
        return float('-inf')


def sim_cosine(src, tar, qval=2):
    """cosine similarity (Ochiai coefficient)

    For two sets X and Y, the cosine similarity (Ochiai coefficient) is:
    :math:`sim_{cosine}(X, Y) = \\frac{|X \\cap Y|}{\\sqrt{|X| \\cdot |Y|}}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: cosine similarity
    :rtype: float
    """
    if src == tar:
        return 1.0
    if not src or not tar:
        return 0.0

    if isinstance(src, Counter) and isinstance(tar, Counter):
        q_src = src
        q_tar = tar
    elif qval and qval > 0:
        q_src = QGrams(src, qval)
        q_tar = QGrams(tar, qval)
    else:
        q_src = Counter(src.strip().split())
        q_tar = Counter(tar.strip().split())
    q_src_mag = sum(q_src.values())
    q_tar_mag = sum(q_tar.values())
    q_intersection_mag = sum((q_src & q_tar).values())

    return q_intersection_mag / math.sqrt(q_src_mag * q_tar_mag)


def dist_cosine(src, tar, qval=2):
    """cosine distance

    Cosine distance is the complement of cosine similarity:
    :math:`dist_{cosine} = 1 - sim_{cosine}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: cosine distance
    :rtype: float
    """
    return 1 - sim_cosine(src, tar, qval)


def sim_strcmp95(src, tar, long_strings=False):
    """strcmp95 similarity

    This is a Python translation of the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    The above file is a US Government publication and, accordingly,
    in the public domain.

    This is based on the Jaro-Winkler distance, but also attempts to correct
    for some common typos and frequently confused characters. It is also
    limited to uppercase ASCII characters, so it is appropriate to American
    names, but not much else.

    :param str src, tar: two strings to be compared
    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large. It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :returns: strcmp95 similarity
    :rtype: float
    """
    def _in_range(char):
        """Return True if char is in the range (0, 91)
        """
        return ord(char) > 0 and ord(char) < 91

    ying = src.strip().upper()
    yang = tar.strip().upper()

    if ying == yang:
        return 1.0
    # If either string is blank - return - added in Version 2
    if len(ying) == 0 or len(yang) == 0:
        return 0.0

    adjwt = defaultdict(int)
    sp_mx = (
        ('A', 'E'), ('A', 'I'), ('A', 'O'), ('A', 'U'), ('B', 'V'), ('E', 'I'),
        ('E', 'O'), ('E', 'U'), ('I', 'O'), ('I', 'U'), ('O', 'U'), ('I', 'Y'),
        ('E', 'Y'), ('C', 'G'), ('E', 'F'), ('W', 'U'), ('W', 'V'), ('X', 'K'),
        ('S', 'Z'), ('X', 'S'), ('Q', 'C'), ('U', 'V'), ('M', 'N'), ('L', 'I'),
        ('Q', 'O'), ('P', 'R'), ('I', 'J'), ('2', 'Z'), ('5', 'S'), ('8', 'B'),
        ('1', 'I'), ('1', 'L'), ('0', 'O'), ('0', 'Q'), ('C', 'K'), ('G', 'J')
    )

    # Initialize the adjwt array on the first call to the function only.
    # The adjwt array is used to give partial credit for characters that
    # may be errors due to known phonetic or character recognition errors.
    # A typical example is to match the letter "O" with the number "0"
    for i in sp_mx:
        adjwt[(i[0], i[1])] = 3
        adjwt[(i[1], i[0])] = 3

    if len(ying) > len(yang):
        search_range = len(ying)
        minv = len(yang)
    else:
        search_range = len(yang)
        minv = len(ying)

    # Blank out the flags
    ying_flag = [0] * search_range
    yang_flag = [0] * search_range
    search_range = max(0, search_range // 2 - 1)

    # Looking only within the search range, count and flag the matched pairs.
    num_com = 0
    yl1 = len(yang) - 1
    for i in _range(len(ying)):
        lowlim = (i - search_range) if (i >= search_range) else 0
        hilim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in _range(lowlim, hilim+1):
            if (yang_flag[j] == 0) and (yang[j] == ying[i]):
                yang_flag[j] = 1
                ying_flag[i] = 1
                num_com += 1
                break

    # If no characters in common - return
    if num_com == 0:
        return 0.0

    # Count the number of transpositions
    k = n_trans = 0
    for i in _range(len(ying)):
        if ying_flag[i] != 0:
            for j in _range(k, len(yang)):
                if yang_flag[j] != 0:
                    k = j + 1
                    break
            if ying[i] != yang[j]:
                n_trans += 1
    n_trans = n_trans // 2

    # Adjust for similarities in unmatched characters
    n_simi = 0
    if minv > num_com:
        for i in _range(len(ying)):
            if ying_flag[i] == 0 and _in_range(ying[i]):
                for j in _range(len(yang)):
                    if yang_flag[j] == 0 and _in_range(yang[j]):
                        if (ying[i], yang[j]) in adjwt:
                            n_simi += adjwt[(ying[i], yang[j])]
                            yang_flag[j] = 2
                            break
    num_sim = n_simi/10.0 + num_com

    # Main weight computation
    weight = num_sim / len(ying) + num_sim / len(yang) + \
        (num_com - n_trans) / num_com
    weight = weight / 3.0

    # Continue to boost the weight if the strings are similar
    if weight > 0.7:

        # Adjust for having up to the first 4 characters in common
        j = 4 if (minv >= 4) else minv
        i = 0
        while (i < j) and (ying[i] == yang[i]) and (not ying[i].isdigit()):
            i += 1
        if i:
            weight += i * 0.1 * (1.0 - weight)

        # Optionally adjust for long strings.

        # After agreeing beginning chars, at least two more must agree and
        # the agreeing characters must be > .5 of remaining characters.
        if (((long_strings) and (minv > 4) and (num_com > i+1) and
             (2*num_com >= minv+i))):
            if not ying[0].isdigit():
                weight += (1.0-weight) * ((num_com-i-1) /
                                          (len(ying)+len(yang)-i*2+2))

    return weight


def dist_strcmp95(src, tar, long_strings=False):
    """strcmp95 distance

    strcmp95 distance is 1 - strcmp95 similarity

    :param str src, tar: two strings to be compared
    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large. It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :returns: strcmp95 distance
    :rtype: float
    """
    return 1 - sim_strcmp95(src, tar, long_strings)


def sim_jaro_winkler(src, tar, qval=1, mode='winkler', long_strings=False,
                     boost_threshold=0.7, scaling_factor=0.1):
    """Jaro(-Winkler) distance

    This is Python based on the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    The above file is a US Government publication and, accordingly,
    in the public domain.

    :param str src, tar: two strings to be compared
    :param int qval: the length of each q-gram (defaults to 1: character-wise
        matching)
    :param str mode: indicates which variant of this distance metric to
        compute:

            - 'winkler' -- computes the Jaro-Winkler distance (default) which
              increases the score for matches near the start of the word
            - 'jaro' -- computes the Jaro distance

    The following arguments apply only when mode is 'winkler':

    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large.  It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :param float boost_threshold: a value between 0 and 1, below which the
        Winkler boost is not applied (defaults to 0.7)
    :param float scaling_factor: a value between 0 and 0.25, indicating by how
        much to boost scores for matching prefixes (defaults to 0.1)

    :returns: Jaro or Jaro-Winkler similarity
    :rtype: float
    """
    if mode == 'winkler':
        if boost_threshold > 1 or boost_threshold < 0:
            raise ValueError('Unsupported boost_threshold assignment; ' +
                             'boost_threshold must be between 0 and 1.')
        if scaling_factor > 0.25 or scaling_factor < 0:
            raise ValueError('Unsupported scaling_factor assignment; ' +
                             'scaling_factor must be between 0 and 0.25.')

    if src == tar:
        return 1.0

    src = QGrams(src.strip(), qval).ordered_list
    tar = QGrams(tar.strip(), qval).ordered_list

    lens = len(src)
    lent = len(tar)

    # If either string is blank - return - added in Version 2
    if lens == 0 or lent == 0:
        return 0.0

    if lens > lent:
        search_range = lens
        minv = lent
    else:
        search_range = lent
        minv = lens

    # Zero out the flags
    src_flag = [0] * search_range
    tar_flag = [0] * search_range
    search_range = max(0, search_range//2 - 1)

    # Looking only within the search range, count and flag the matched pairs.
    num_com = 0
    yl1 = lent - 1
    for i in _range(lens):
        lowlim = (i - search_range) if (i >= search_range) else 0
        hilim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in _range(lowlim, hilim+1):
            if (tar_flag[j] == 0) and (tar[j] == src[i]):
                tar_flag[j] = 1
                src_flag[i] = 1
                num_com += 1
                break

    # If no characters in common - return
    if num_com == 0:
        return 0.0

    # Count the number of transpositions
    k = n_trans = 0
    for i in _range(lens):
        if src_flag[i] != 0:
            for j in _range(k, lent):
                if tar_flag[j] != 0:
                    k = j + 1
                    break
            if src[i] != tar[j]:
                n_trans += 1
    n_trans = n_trans // 2

    # Main weight computation for Jaro distance
    weight = num_com / lens + num_com / lent + (num_com - n_trans) / num_com
    weight = weight / 3.0

    # Continue to boost the weight if the strings are similar
    # This is the Winkler portion of Jaro-Winkler distance
    if mode == 'winkler' and weight > boost_threshold:

        # Adjust for having up to the first 4 characters in common
        j = 4 if (minv >= 4) else minv
        i = 0
        while (i < j) and (src[i] == tar[i]):
            i += 1
        if i:
            weight += i * scaling_factor * (1.0 - weight)

        # Optionally adjust for long strings.

        # After agreeing beginning chars, at least two more must agree and
        # the agreeing characters must be > .5 of remaining characters.
        if (((long_strings) and (minv > 4) and (num_com > i+1) and
             (2*num_com >= minv+i))):
            weight += (1.0-weight) * ((num_com-i-1) / (lens+lent-i*2+2))

    return weight


def dist_jaro_winkler(src, tar, qval=1, mode='winkler', long_strings=False,
                      boost_threshold=0.7, scaling_factor=0.1):
    """Jaro(-Winkler) distance

    Jaro-Winkler distance is 1 - the Jaro-Winkler similarity

    :param str src, tar: two strings to be compared
    :param int qval: the length of each q-gram (defaults to 1: character-wise
        matching)
    :param str mode: indicates which variant of this distance metric to
        compute:

            - 'winkler' -- computes the Jaro-Winkler distance (default) which
              increases the score for matches near the start of the word
            - 'jaro' -- computes the Jaro distance

    The following arguments apply only when mode is 'winkler':

    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large.  It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :param float boost_threshold: a value between 0 and 1, below which the
        Winkler boost is not applied (defaults to 0.7)
    :param float scaling_factor: a value between 0 and 0.25, indicating by how
        much to boost scores for matching prefixes (defaults to 0.1)

    :returns: Jaro or Jaro-Winkler distance
    :rtype: float
    """
    return 1 - sim_jaro_winkler(src, tar, qval, mode, long_strings,
                                boost_threshold, scaling_factor)


def lcsseq(src, tar):
    """longest common subsequence (LCSseq)

    Based on the dynamic programming algorithm from
    http://rosettacode.org/wiki/Longest_common_subsequence#Dynamic_Programming_6
    This is licensed GFDL 1.2

    Modifications include:
        conversion to a numpy array in place of a list of lists

    :param str src, tar: two strings to be compared
    :returns: the longes common subsequence
    :rtype: str
    """
    # pylint: disable=no-member
    lengths = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.int)
    # pylint: enable=no-member

    # row 0 and column 0 are initialized to 0 already
    for i, src_char in enumerate(src):
        for j, tar_char in enumerate(tar):
            if src_char == tar_char:
                lengths[i+1, j+1] = lengths[i, j] + 1
            else:
                lengths[i+1, j+1] = max(lengths[i+1, j], lengths[i, j+1])

    # read the substring out from the matrix
    result = ""
    i, j = len(src), len(tar)
    while i != 0 and j != 0:
        if lengths[i, j] == lengths[i-1, j]:
            i -= 1
        elif lengths[i, j] == lengths[i, j-1]:
            j -= 1
        else:
            assert src[i-1] == tar[j-1]
            result = src[i-1] + result
            i -= 1
            j -= 1
    return result


def sim_lcsseq(src, tar):
    """longest common subsequence similarity (:math:`sim_{LCSseq}`)

    This employs the LCSseq function to derive a similarity metric:
    :math:`sim_{LCSseq}(s,t) = \\frac{|LCSseq(s,t)|}{max(|s|, |t|)}`

    :param str src, tar: two strings to be compared
    :returns: LCSseq similarity
    :rtype: float
    """
    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0
    return len(lcsseq(src, tar)) / max(len(src), len(tar))


def dist_lcsseq(src, tar):
    """longest common subsequence distance (:math:`dist_{LCSseq}`)

    This employs the LCSseq function to derive a similarity metric:
    :math:`dist_{LCSseq}(s,t) = 1 - sim_{LCSseq}(s,t)`

    :param str src, tar: two strings to be compared
    :returns: LCSseq distance
    :rtype: float
    """
    return 1 - sim_lcsseq(src, tar)


def lcsstr(src, tar):
    """longest common substring (LCSstr)

    Based on the code from
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python
    This is licensed Creative Commons: Attribution-ShareAlike 3.0

    Modifications include:

        - conversion to a numpy array in place of a list of lists
        - conversion to Python 2/3-safe _range from xrange

    :param str src, tar: two strings to be compared
    :returns: the longes common substring
    :rtype: float
    """
    # pylint: disable=no-member
    lengths = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.int)
    # pylint: enable=no-member
    longest, i_longest = 0, 0
    for i in _range(1, len(src)+1):
        for j in _range(1, len(tar)+1):
            if src[i-1] == tar[j-1]:
                lengths[i, j] = lengths[i-1, j-1] + 1
                if lengths[i, j] > longest:
                    longest = lengths[i, j]
                    i_longest = i
            else:
                lengths[i, j] = 0
    return src[i_longest - longest:i_longest]


def sim_lcsstr(src, tar):
    """longest common substring similarity (:math:`sim_{LCSstr}`)

    This employs the LCS function to derive a similarity metric:
    :math:`sim_{LCSstr}(s,t) = \\frac{|LCSstr(s,t)|}{max(|s|, |t|)}`

    :param str src, tar: two strings to be compared
    :returns: LCSstr similarity
    :rtype: float
    """
    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0
    return len(lcsstr(src, tar)) / max(len(src), len(tar))


def dist_lcsstr(src, tar):
    """longest common substring distance (:math:`dist_{LCSstr}`)

    This employs the LCS function to derive a similarity metric:
    :math:`dist_{LCSstr}(s,t) = 1 - sim_{LCSstr}(s,t)`

    :param str src, tar: two strings to be compared
    :returns: LCSstr distance
    :rtype: float
    """
    return 1 - sim_lcsstr(src, tar)


def sim_ratcliff_obershelp(src, tar):
    """Ratcliff-Obershelp similarity

    This follows the Ratcliff-Obershelp algorithm to derive a similarity
    measure:

        1. Find the length of the longest common substring in src & tar.
        2. Recurse on the strings to the left & right of each this substring
           in src & tar. The base case is a 0 length common substring, in which
           case, return 0. Otherwise, return the sum of the current longest
           common substring and the left & right recursed sums.
        3. Multiply this length by 2 and divide by the sum of the lengths of
           src & tar.

    Cf.
    http://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970

    :param str src, tar: two strings to be compared
    :returns: Ratcliff-Obserhelp similarity
    :rtype: float
    """
    def _lcsstr_stl(src, tar):
        """Return the start position in the source string, start position in
        the target string, and length of the longest common substring of
        strings src and tar
        """
        # pylint: disable=no-member
        lengths = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.int)
        # pylint: enable=no-member
        longest, src_longest, tar_longest = 0, 0, 0
        for i in _range(1, len(src)+1):
            for j in _range(1, len(tar)+1):
                if src[i-1] == tar[j-1]:
                    lengths[i, j] = lengths[i-1, j-1] + 1
                    if lengths[i, j] > longest:
                        longest = lengths[i, j]
                        src_longest = i
                        tar_longest = j
                else:
                    lengths[i, j] = 0
        return (src_longest-longest, tar_longest-longest, longest)

    def _sstr_matches(src, tar):
        """Return the sum of substring match lengths by following the
        Ratcliff-Obershelp algorithm:

             1. Find the length of the longest common substring in src & tar.
             2. Recurse on the strings to the left & right of each this
                 substring in src & tar.
             3. Base case is a 0 length common substring, in which case,
                 return 0.
             4. Return the sum.
        """
        src_start, tar_start, length = _lcsstr_stl(src, tar)
        if length == 0:
            return 0
        return (_sstr_matches(src[:src_start], tar[:tar_start]) +
                length +
                _sstr_matches(src[src_start+length:], tar[tar_start+length:]))

    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0
    return 2*_sstr_matches(src, tar)/(len(src)+len(tar))


def dist_ratcliff_obershelp(src, tar):
    """Ratcliff-Obershelp distance

    Ratcliff-Obsershelp distance the complement of Ratcliff-Obershelp
    similarity:
    :math:`dist_{Ratcliff-Obershelp} = 1 - sim_{Ratcliff-Obershelp}`

    :param str src, tar: two strings to be compared
    :returns: Ratcliffe-Obershelp distance
    :rtype: float
    """
    return 1 - sim_ratcliff_obershelp(src, tar)


def mra_compare(src, tar):
    """Western Airlines Surname Match Rating Algorithm comparison rating

    A description of the algorithm can be found on page 18 of
    https://archive.org/details/accessingindivid00moor

    :param str src, tar: two strings to be compared
    :returns: MRA comparison rating
    :rtype: int
    """
    if src == tar:
        return 6
    if src == '' or tar == '':
        return 0
    src = list(mra(src))
    tar = list(mra(tar))

    if abs(len(src)-len(tar)) > 2:
        return 0

    length_sum = len(src) + len(tar)
    if length_sum < 5:
        min_rating = 5
    elif length_sum < 8:
        min_rating = 4
    elif length_sum < 12:
        min_rating = 3
    else:
        min_rating = 2

    for _ in _range(2):
        new_src = []
        new_tar = []
        minlen = min(len(src), len(tar))
        for i in _range(minlen):
            if src[i] != tar[i]:
                new_src.append(src[i])
                new_tar.append(tar[i])
        src = new_src+src[minlen:]
        tar = new_tar+tar[minlen:]
        src.reverse()
        tar.reverse()

    similarity = 6 - max(len(src), len(tar))

    if similarity >= min_rating:
        return similarity
    return 0


def sim_mra(src, tar):
    """normalized Match Rating Algorithm similarity

    This is the MRA normalized to :math:`[0, 1]`, given that MRA itself is
    constrained to the range :math:`[0, 6]`.

    :param str src, tar: two strings to be compared
    :returns: normalized MRA similarity
    :rtype: float
    """
    return mra_compare(src, tar)/6


def dist_mra(src, tar):
    """normalized Match Rating Algorithm distance

    MRA distance is the complement of MRA similarity:
    :math:`dist_{MRA} = 1 - sim_{MRA}`

    :param str src, tar: two strings to be compared
    :returns: normalized MRA distance
    :rtype: float
    """
    return 1 - sim_mra(src, tar)


def dist_compression(src, tar, compressor='bz2', probs=None):
    """normalized compression distance (NCD)

    Cf.
    https://en.wikipedia.org/wiki/Normalized_compression_distance#Normalized_compression_distance

    :param str src, tar: two strings to be compared
    :param str compressor: a compression scheme to use for the similarity
        calculation, from the following:

            - `zlib` -- standard zlib/gzip
            - `bz2` -- bzip2
            - `lzma` -- Lempel–Ziv–Markov chain algorithm
            - `arith` -- arithmetic coding
            - `rle` -- run-length encoding
            - `bwtrle` -- Burrows-Wheeler transform followed by run-length
              encoding

    :param doct probs: a dictionary trained with ac_train (for the arith
        compressor only)
    :returns: compression distance
    :rtype: float
    """
    if src == tar:
        return 0.0

    if compressor not in frozenset(['arith', 'rle', 'bwtrle']):
        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

    if compressor == 'bz2':
        src_comp = codecs.encode(src, 'bz2_codec')[15:]
        tar_comp = codecs.encode(tar, 'bz2_codec')[15:]
        concat_comp = codecs.encode(src+tar, 'bz2_codec')[15:]
        concat_comp2 = codecs.encode(tar+src, 'bz2_codec')[15:]
    elif compressor == 'lzma':
        if 'lzma' in sys.modules:
            src_comp = lzma.compress(src)[14:]
            tar_comp = lzma.compress(tar)[14:]
            concat_comp = lzma.compress(src+tar)[14:]
            concat_comp2 = lzma.compress(tar+src)[14:]
        else:  # pragma: no cover
            raise ValueError('Install the PylibLZMA module in order to use ' +
                             'lzma compression similarity')
    elif compressor == 'arith':
        if probs is None:
            # lacking a reasonable dictionary, train on the strings themselves
            probs = ac_train(src+tar)
        src_comp = ac_encode(src, probs)[1]
        tar_comp = ac_encode(tar, probs)[1]
        concat_comp = ac_encode(src+tar, probs)[1]
        concat_comp2 = ac_encode(tar+src, probs)[1]
        return ((min(concat_comp, concat_comp2) - min(src_comp, tar_comp)) /
                max(src_comp, tar_comp))
    elif compressor in frozenset(['rle', 'bwtrle']):
        src_comp = rle_encode(src, (compressor == 'bwtrle'))
        tar_comp = rle_encode(tar, (compressor == 'bwtrle'))
        concat_comp = rle_encode(src+tar, (compressor == 'bwtrle'))
        concat_comp2 = rle_encode(tar+src, (compressor == 'bwtrle'))
    else:  # zlib
        src_comp = codecs.encode(src, 'zlib_codec')[2:]
        tar_comp = codecs.encode(tar, 'zlib_codec')[2:]
        concat_comp = codecs.encode(src+tar, 'zlib_codec')[2:]
        concat_comp2 = codecs.encode(tar+src, 'zlib_codec')[2:]
    return ((min(len(concat_comp), len(concat_comp2)) -
             min(len(src_comp), len(tar_comp))) /
            max(len(src_comp), len(tar_comp)))


def sim_compression(src, tar, compressor='bz2', probs=None):
    """normalized compression similarity (NCS)

    Normalized compression similarity is the complement of normalized
    compression distance:
    :math:`sim_{NCS} = 1 - dist_{NCD}`

    :param str src, tar: two strings to be compared
    :param str compressor: a compression scheme to use for the similarity
        calculation:

            - `zlib` -- standard zlib/gzip
            - `bz2` -- bzip2
            - `lzma` -- Lempel–Ziv–Markov chain algorithm
            - `arith` -- arithmetic coding
            - `rle` -- run-length encoding
            - `bwtrle` -- Burrows-Wheeler transform followed by run-length
              encoding

    :param dict probs: a dictionary trained with ac_train (for the arith
        compressor only)
    :returns: compression similarity
    :rtype: float
    """
    return 1 - dist_compression(src, tar, compressor, probs)


def sim_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Monge-Elkan similarity

    Monge-Elkan is defined in:
    Monge, Alvaro E. and Charles P. Elkan. 1996. "The field matching problem:
    Algorithms and applications." KDD-9 Proceedings.
    http://www.aaai.org/Papers/KDD/1996/KDD96-044.pdf

    Note: Monge-Elkan is NOT a symmetric similarity algoritm. Thus, the
    similarity of src to tar is not necessarily equal to the similarity of
    tar to src. If the sym argument is True, a symmetric value is calculated,
    at the cost of doubling the computation time (since the
    :math:`sim_{Monge-Elkan}(src, tar)` and
    :math:`sim_{Monge-Elkan}(tar, src)` are both calculated and then averaged).

    :param str src, tar: two strings to be compared
    :param function sim_func: the internal similarity metric to emply
    :param bool symmetric: return a symmetric similarity measure
    :returns: Monge-Elkan similarity
    :rtype: float
    """
    if src == tar:
        return 1.0

    q_src = sorted(QGrams(src).elements())
    q_tar = sorted(QGrams(tar).elements())

    if len(q_src) == 0 or len(q_tar) == 0:
        return 0.0

    sum_of_maxes = 0
    for q_s in q_src:
        max_sim = float('-inf')
        for q_t in q_tar:
            max_sim = max(max_sim, sim_func(q_s, q_t))
        sum_of_maxes += max_sim
    sim_em = sum_of_maxes / len(q_src)

    if symmetric:
        sim_em = (sim_em + sim_monge_elkan(tar, src, sim, False))/2

    return sim_em


def dist_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Monge-Elkan distance

    Monge-Elkan is defined in:
    Monge, Alvaro E. and Charles P. Elkan. 1996. "The field matching problem:
    Algorithms and applications." KDD-9 Proceedings.
    http://www.aaai.org/Papers/KDD/1996/KDD96-044.pdf

    Note: Monge-Elkan is NOT a symmetric similarity algoritm. Thus, the
    distance between src and tar is not necessarily equal to the distance
    between tar and src. If the sym argument is True, a symmetric value is
    calculated, at the cost of doubling the computation time (since the
    :math:`sim_{Monge-Elkan}(src, tar)` and :math:`sim_{Monge-Elkan}(tar, src)`
    are both calculated and then averaged).

    :param str src, tar: two strings to be compared
    :param function sim_func: the internal similarity metric to emply
    :param bool symmetric: return a symmetric similarity measure
    :returns: Monge-Elkan distance
    :rtype: float
    """
    return 1 - sim_monge_elkan(src, tar, sim_func, symmetric)


def sim_ident(src, tar):
    """identity similarity

    This is 1 if the two strings are identical, otherwise 0.

    :param str src, tar: two strings to be compared
    :returns: identity similarity
    :rtype: int
    """
    return int(src == tar)


def dist_ident(src, tar):
    """identity distance

    This is 0 if the two strings are identical, otherwise 1, i.e.
    :math:`dist_{identity} = 1 - sim_{identity}`

    :param str src, tar: two strings to be compared
    :returns: indentity distance
    :rtype: int
    """
    return 1 - sim_ident(src, tar)


def sim_matrix(src, tar, mat=None, mismatch_cost=0, match_cost=1,
               symmetric=True, alphabet=None):
    """matrix similarity

    With the default parameters, this is identical to sim_ident.
    It is possible for sim_matrix to return values outside of the range
    :math:`[0, 1]`, if values outside that range are present in mat,
    mismatch_cost, or match_cost.

    :param str src, tar: two strings to be compared
    :param dict mat: a dict mapping tuples to costs; the tuples are (src, tar)
        pairs of symbols from the alphabet parameter
    :param float mismatch_cost: the value returned if (src, tar) is absent from
        mat when src does not equal tar
    :param float match_cost: the value returned if (src, tar) is absent from
        mat when src equals tar
    :param bool symmetric: True if the cost of src not matching tar is
        identical to the cost of tar not matching src; in this case, the values
        in mat need only contain (src, tar) or (tar, src), not both
    :param str alphabet: a collection of tokens from which src and tar are
        drawn; if this is defined a ValueError is raised if either tar or src
        is not found in alphabet
    :returns: matrix similarity
    :rtype: float
    """
    if alphabet:
        alphabet = tuple(alphabet)
        for i in src:
            if i not in alphabet:
                raise ValueError('src value not in alphabet')
        for i in tar:
            if i not in alphabet:
                raise ValueError('tar value not in alphabet')

    if src == tar:
        if mat and (src, src) in mat:
            return mat[(src, src)]
        else:
            return match_cost
    else:
        if mat and (src, tar) in mat:
            return mat[(src, tar)]
        elif symmetric and mat and (tar, src) in mat:
            return mat[(tar, src)]
        else:
            return mismatch_cost


def needleman_wunsch(src, tar, gap_cost=1, sim_func=sim_ident):
    """Needleman-Wunsch score

    This is the standard edit distance measure.

    Cf. https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm

    Cf.
    http://csb.stanford.edu/class/public/readings/Bioinformatics_I_Lecture6/Needleman_Wunsch_JMB_70_Global_alignment.pdf

    :param str src, tar: two strings to be compared
    :param float gap_cost: the cost of an alignment gap (1 by default)
    :param function sim_func: a function that returns the similarity of two
        characters (identity similarity by default)
    :returns: Needleman-Wunsch score
    :rtype: int (in fact dependent on the gap_cost & return value of sim_func)
    """
    # pylint: disable=no-member
    d_mat = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.float)
    # pylint: enable=no-member

    for i in _range(len(src)+1):
        d_mat[i, 0] = -(i * gap_cost)
    for j in _range(len(tar)+1):
        d_mat[0, j] = -(j * gap_cost)
    for i in _range(1, len(src)+1):
        for j in _range(1, len(tar)+1):
            match = d_mat[i-1, j-1] + sim_func(src[i-1], tar[j-1])
            delete = d_mat[i-1, j] - gap_cost
            insert = d_mat[i, j-1] - gap_cost
            d_mat[i, j] = max(match, delete, insert)
    return d_mat[d_mat.shape[0]-1, d_mat.shape[1]-1]


def smith_waterman(src, tar, gap_cost=1, sim_func=sim_ident):
    """Smith-Waterman score

    This is the standard edit distance measure.

    Cf. https://en.wikipedia.org/wiki/Smith–Waterman_algorithm

    :param str src, tar: two strings to be compared
    :param float gap_cost: the cost of an alignment gap (1 by default)
    :param function sim_func: a function that returns the similarity of two
        characters (identity similarity by default)
    :returns: Smith-Waterman score
    :rtype: int (in fact dependent on the gap_cost & return value of sim_func)
    """
    # pylint: disable=no-member
    d_mat = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.float)
    # pylint: enable=no-member

    for i in _range(len(src)+1):
        d_mat[i, 0] = 0
    for j in _range(len(tar)+1):
        d_mat[0, j] = 0
    for i in _range(1, len(src)+1):
        for j in _range(1, len(tar)+1):
            match = d_mat[i-1, j-1] + sim_func(src[i-1], tar[j-1])
            delete = d_mat[i-1, j] - gap_cost
            insert = d_mat[i, j-1] - gap_cost
            d_mat[i, j] = max(0, match, delete, insert)
    return d_mat[d_mat.shape[0]-1, d_mat.shape[1]-1]


def gotoh(src, tar, gap_open=1, gap_ext=0.4, sim_func=sim_ident):
    """Gotoh score

    Gotoh's algorithm is essentially Needleman-Wunsch with affine gap
    penalties:
    https://www.cs.umd.edu/class/spring2003/cmsc838t/papers/gotoh1982.pdf

    :param str src, tar: two strings to be compared
    :param float gap_open: the cost of an open alignment gap (1 by default)
    :param float gap_ext: the cost of an alignment gap extension (0.4 by
        default)
    :param function sim_func: a function that returns the similarity of two
        characters (identity similarity by default)
    :returns: Gotoh score
    :rtype: float (in fact dependent on the gap_cost & return value of
        sim_func)
    """
    # pylint: disable=no-member
    d_mat = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.float)
    p_mat = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.float)
    q_mat = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.float)
    # pylint: enable=no-member

    d_mat[0, 0] = 0
    p_mat[0, 0] = float('-inf')
    q_mat[0, 0] = float('-inf')
    for i in _range(1, len(src)+1):
        d_mat[i, 0] = float('-inf')
        p_mat[i, 0] = -gap_open - gap_ext*(i-1)
        q_mat[i, 0] = float('-inf')
        q_mat[i, 1] = -gap_open
    for j in _range(1, len(tar)+1):
        d_mat[0, j] = float('-inf')
        p_mat[0, j] = float('-inf')
        p_mat[1, j] = -gap_open
        q_mat[0, j] = -gap_open - gap_ext*(j-1)

    for i in _range(1, len(src)+1):
        for j in _range(1, len(tar)+1):
            sim_val = sim_func(src[i-1], tar[j-1])
            d_mat[i, j] = max(d_mat[i-1, j-1] + sim_val,
                              p_mat[i-1, j-1] + sim_val,
                              q_mat[i-1, j-1] + sim_val)

            p_mat[i, j] = max(d_mat[i-1, j] - gap_open,
                              p_mat[i-1, j] - gap_ext)

            q_mat[i, j] = max(d_mat[i, j-1] - gap_open,
                              q_mat[i, j-1] - gap_ext)

    i, j = (n - 1 for n in d_mat.shape)
    return max(d_mat[i, j], p_mat[i, j], q_mat[i, j])


def sim_length(src, tar):
    """length similarity

    This is the ratio of the length of the shorter string to the longer.

    :param str src, tar: two strings to be compared
    :returns: length similarity
    :rtype: float
    """
    if src == tar:
        return 1.0
    if len(src) == 0 or len(tar) == 0:
        return 0.0
    return len(src)/len(tar) if len(src) < len(tar) else len(tar)/len(src)


def dist_length(src, tar):
    """length distance

    Length distance is the complement of length similarity:
    :math:`dist_{length} = 1 - sim_{length}`

    :param str src, tar: two strings to be compared
    :returns: length distance
    :rtype: float
    """
    return 1 - sim_length(src, tar)


def sim_prefix(src, tar):
    """prefix similarity

    Prefix similarity is the ratio of the length of the shorter term that
    exactly matches the longer term to the length of the shorter term,
    beginning at the start of both terms.

    :param str src, tar: two strings to be compared
    :returns: prefix similarity
    :rtype: float
    """
    if src == tar:
        return 1.0
    if len(src) == 0 or len(tar) == 0:
        return 0.0
    min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
    min_len = len(min_word)
    for i in _range(min_len, 0, -1):
        if min_word[:i] == max_word[:i]:
            return i/min_len
    return 0.0


def dist_prefix(src, tar):
    """prefix distance

    Prefix distance is the complement of prefix similarity:
    :math:`dist_{prefix} = 1 - sim_{prefix}`

    :param str src, tar: two strings to be compared
    :returns: prefix distance
    :rtype: float
    """
    return 1 - sim_prefix(src, tar)


def sim_suffix(src, tar):
    """suffix similarity

    Suffix similarity is the ratio of the length of the shorter term that
    exactly matches the longer term to the length of the shorter term,
    beginning at the end of both terms.

    :param str src, tar: two strings to be compared
    :returns: suffix similarity
    :rtype: float
    """
    if src == tar:
        return 1.0
    if len(src) == 0 or len(tar) == 0:
        return 0.0
    min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
    min_len = len(min_word)
    for i in _range(min_len, 0, -1):
        if min_word[-i:] == max_word[-i:]:
            return i/min_len
    return 0.0


def dist_suffix(src, tar):
    """suffix distance

    Suffix distance is the complement of suffix similarity:
    :math:`dist_{suffix} = 1 - sim_{suffix}`

    :param str src, tar: two strings to be compared
    :returns: suffix distance
    :rtype: float
    """
    return 1 - sim_suffix(src, tar)


def sim_mlipns(src, tar, threshold=0.25, maxmismatches=2):
    """Modified Language-Independent Product Name Search (MLIPNS)

    The MLIPNS algorithm is described in Shannaq, Boumedyen A. N. and Victor V.
    Alexandrov. 2010. "Using Product Similarity for Adding Business." Global
    Journal of Computer Science and Technology. 10(12). 2-8.
    http://www.sial.iias.spb.su/files/386-386-1-PB.pdf

    This function returns only 1.0 (similar) or 0.0 (not similar).

    LIPNS similarity is identical to normalized Hamming similarity.

    :param str src, tar: two strings to be compared
    :param float threshold: a number [0, 1] indicating the maximum similarity
        score, below which the strings are considered 'similar' (0.25 by
        default)
    :param int maxmismatches: a number indicating the allowable number of
        mismatches to remove before declaring two strings not similar (2 by
        default)
    :returns: MLIPNS similarity
    :rtype: float
    """
    if tar == src:
        return 1.0
    if len(src) == 0 or len(tar) == 0:
        return 0.0

    mismatches = 0
    ham = hamming(src, tar, difflens=True)
    maxlen = max(len(src), len(tar))
    while src and tar and mismatches <= maxmismatches:
        if maxlen < 1 or (1-(maxlen-ham)/maxlen) <= threshold:
            return 1.0
        else:
            mismatches += 1
            ham -= 1
            maxlen -= 1

    if maxlen < 1:
        return 1.0
    return 0.0


def dist_mlipns(src, tar, threshold=0.25, maxmismatches=2):
    """Modified Language-Independent Product Name Search (MLIPNS)

    MLIPNS distance is the complement of MLIPNS similarity:
    :math:`dist_{MLIPNS} = 1 - sim_{MLIPNS}`

    This function returns only 0.0 (distant) or 1.0 (not distant)

    :param str src, tar: two strings to be compared
    :param float threshold: a number [0, 1] indicating the maximum similarity
        score, below which the strings are considered 'similar' (0.25 by
        default)
    :param int maxmismatches: a number indicating the allowable number of
        mismatches to remove before declaring two strings not similar (2 by
        default)
    :returns: MLIPNS distance
    :rtype: float
    """
    return 1.0 - sim_mlipns(src, tar, threshold, maxmismatches)


def bag(src, tar):
    """bag distance

    Bag distance is:
    :math:`max( |multiset(src)-multiset(tar)|, |multiset(tar)-multiset(src)| )`

    :param str src, tar: two strings to be compared
    :returns: bag distance
    :rtype: int
    """
    if tar == src:
        return 0
    elif len(src) == 0:
        return len(tar)
    elif len(tar) == 0:
        return len(src)

    src_bag = Counter(src)
    tar_bag = Counter(tar)
    return max(len(src_bag-tar_bag), len(tar_bag-src_bag))


def dist_bag(src, tar):
    """Return the normalized bag distance of two strings.

    Bag distance is normalized by dividing by :math:`max( |src|, |tar| )`.

    :param str src, tar: two strings to be compared
    :returns: normalized bag distance
    :rtype: float
    """
    if tar == src:
        return 0.0
    if len(src) == 0 or len(tar) == 0:
        return 1.0

    maxlen = max(len(src), len(tar))

    return bag(src, tar)/maxlen


def sim_bag(src, tar):
    """normalized bag similarity


    Normalized bag similarity is the complement of normalized bag distance:
    :math:`sim_{bag} = 1 - dist_{bag}`

    :param str src, tar: two strings to be compared
    :returns: normalized bag similarity
    :rtype: float
    """
    return 1-dist_bag(src, tar)


def editex(src, tar, cost=(0, 1, 2), local=False):
    """Editex distance

    As described on pages 3 & 4 of
    Zobel, Justin and Philip Dart. 1996. Phonetic string matching: Lessons from
    information retrieval. In: Proceedings of the ACM-SIGIR Conference on
    Research and Development in Information Retrieval, Zurich, Switzerland.
    166–173. http://goanna.cs.rmit.edu.au/~jz/fulltext/sigir96.pdf

    The local variant is based on
    Ring, Nicholas and Alexandra L. Uitdenbogerd. 2009. Finding ‘Lucy in
    Disguise’: The Misheard Lyric Matching Problem. In: Proceedings of the 5th
    Asia Information Retrieval Symposium, Sapporo, Japan. 157-167.
    http://www.seg.rmit.edu.au/research/download.php?manuscript=404

    :param str src, tar: two strings to be compared
    :param tuple cost: a 3-tuple representing the cost of the four possible
        edits:
        match, same-group, and mismatch respectively (by default: (0, 1, 2))
    :param bool local: if True, the local variant of Editex is used
    :returns: Editex distance
    :rtype: int
    """
    match_cost, group_cost, mismatch_cost = cost
    letter_groups = (frozenset('AEIOUY'), frozenset('BP'), frozenset('CKQ'),
                     frozenset('DT'), frozenset('LR'), frozenset('MN'),
                     frozenset('GJ'), frozenset('FPV'), frozenset('SXZ'),
                     frozenset('CSZ'))
    all_letters = frozenset('AEIOUYBPCKQDTLRMNGJFVSXZ')

    def r_cost(ch1, ch2):
        """Return r(a,b) according to Zobel & Dart's definition
        """
        if ch1 == ch2:
            return match_cost
        if ch1 in all_letters and ch2 in all_letters:
            for group in letter_groups:
                if ch1 in group and ch2 in group:
                    return group_cost
        return mismatch_cost

    def d_cost(ch1, ch2):
        """Return d(a,b) according to Zobel & Dart's definition
        """
        if ch1 != ch2 and (ch1 == 'H' or ch1 == 'W'):
            return group_cost
        return r_cost(ch1, ch2)

    # convert both src & tar to NFKD normalized unicode
    src = unicodedata.normalize('NFKD', _unicode(src.upper()))
    tar = unicodedata.normalize('NFKD', _unicode(tar.upper()))
    # convert ß to SS (for Python2)
    src = src.replace('ß', 'SS')
    tar = tar.replace('ß', 'SS')

    if src == tar:
        return 0
    if len(src) == 0:
        return len(tar) * mismatch_cost
    if len(tar) == 0:
        return len(src) * mismatch_cost

    # pylint: disable=no-member
    d_mat = numpy.zeros((len(src)+1, len(tar)+1), dtype=numpy.int)
    # pylint: enable=no-member
    lens = len(src)
    lent = len(tar)
    src = ' '+src
    tar = ' '+tar

    if not local:
        for i in _range(1, lens+1):
            d_mat[i, 0] = d_mat[i-1, 0] + d_cost(src[i-1], src[i])
    for j in _range(1, lent+1):
        d_mat[0, j] = d_mat[0, j-1] + d_cost(tar[j-1], tar[j])

    for i in _range(1, lens+1):
        for j in _range(1, lent+1):
            d_mat[i, j] = min(d_mat[i-1, j] + d_cost(src[i-1], src[i]),
                              d_mat[i, j-1] + d_cost(tar[j-1], tar[j]),
                              d_mat[i-1, j-1] + r_cost(src[i], tar[j]))

    return d_mat[lens, lent]


def dist_editex(src, tar, cost=(0, 1, 2), local=False):
    """Editex distance normalized to the interval [0, 1]

    The Editex distance is normalized by dividing the Editex distance
    (calculated by any of the three supported methods) by the greater of
    the number of characters in src times the cost of a delete and
    the number of characters in tar times the cost of an insert.
    For the case in which all operations have :math:`cost = 1`, this is
    equivalent to the greater of the length of the two strings src & tar.

    :param str src, tar: two strings to be compared
    :param tuple cost: a 3-tuple representing the cost of the four possible
        edits:
        match, same-group, and mismatch respectively (by default: (0, 1, 2))
    :param bool local: if True, the local variant of Editex is used
    :returns: normalized Editex distance
    :rtype: float
    """
    if src == tar:
        return 0
    mismatch_cost = cost[2]
    return (editex(src, tar, cost, local) /
            (max(len(src)*mismatch_cost, len(tar)*mismatch_cost)))


def sim_editex(src, tar, cost=(0, 1, 2), local=False):
    """Editex similarity normalized to the interval [0, 1]

    The Editex similarity is the complement of Editex distance
    :math:`sim_{Editex} = 1 - dist_{Editex}`

    The arguments are identical to those of the editex() function.

    :param str src, tar: two strings to be compared
    :param tuple cost: a 3-tuple representing the cost of the four possible
        edits:
        match, same-group, and mismatch respectively (by default: (0, 1, 2))
    :param bool local: if True, the local variant of Editex is used
    :returns: normalized Editex similarity
    :rtype: float
    """
    return 1 - dist_editex(src, tar, cost, local)


def sim_tfidf(src, tar, qval=2, docs_src=None, docs_tar=None):
    """TF-IDF similarity

    This is chiefly based on the "Formal Definition of TF/IDF Distance" at:
    http://alias-i.com/lingpipe/docs/api/com/aliasi/spell/TfIdfDistance.html

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :param Counter docs_src: a Counter object or string representing the
        document corpus for the src string
    :param Counter docs_tar: a Counter object or string representing the
        document corpus for the tar string (or set to None to use the docs_src
        for both)
    :returns: TF-IDF similarity
    :rtype: float
    """
    if src == tar:
        return 1.0  # TODO: confirm correctness of this when docs are different
    elif len(src) == 0 or len(tar) == 0:
        return 0.0

    if isinstance(src, Counter) and isinstance(tar, Counter):
        q_src = src
        q_tar = tar
    elif qval and qval > 0:
        q_src = QGrams(src, qval)
        q_tar = QGrams(tar, qval)
    else:
        q_src = Counter(src.strip().split())
        q_tar = Counter(tar.strip().split())

    if isinstance(docs_src, Counter):
        q_docs = docs_src
    elif qval and qval > 0:
        q_docs = QGrams(docs_src, qval)
    else:
        q_docs = Counter(docs_src.strip().split())

    if len(q_src) == 0 or len(q_tar) == 0:
        return 0.0

    # TODO: finish implementation

###############################################################################


def sim(src, tar, method=sim_levenshtein):
    """generalized similarity

    This is a generalized function for calling other similarity functions.

    :param str src, tar: two strings to be compared
    :param function method: specifies the similarity metric (Levenshtein by
        default)
    :returns: similarity according to the specified function
    :rtype: float
    """
    if hasattr(method, '__call__'):
        return method(src, tar)
    else:
        raise AttributeError('Unknown similarity function: ' + str(method))


def dist(src, tar, method=sim_levenshtein):
    """generalized distance

    This is a generalized function for calling other distance functions.

    :param str src, tar: two strings to be compared
    :param function method: specifies the similarity metric (Levenshtein by
        default) -- Note that this takes a similarity metric function, not
        a distance metric function.
    :returns: distance according to the specified function
    :rtype: float
    """
    if hasattr(method, '__call__'):
        return 1 - method(src, tar)
    else:
        raise AttributeError('Unknown distance function: ' + str(method))
