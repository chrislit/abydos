# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.distance.

The distance module implements string edit distance functions including:

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

Functions beginning with the prefixes 'sim' and 'dist' are guaranteed to be
in the range [0, 1], and sim_X = 1 - dist_X since the two are complements.
If a sim_X function is supplied identical src & tar arguments, it is guaranteed
to return 1; the corresponding dist_X function is guaranteed to return 0.
"""

from __future__ import division, unicode_literals

import codecs
import math
import sys
import types
import unicodedata
from collections import Counter, Iterable, defaultdict

import numpy as np

from six import text_type
from six.moves import range

from .compression import ac_encode, ac_train, rle_encode
from .fingerprint import synoname_toolcode
from .phonetic import eudex, mra
from .qgram import QGrams

try:
    import lzma
except ImportError:  # pragma: no cover
    # If the system lacks the lzma library, that's fine, but lzma comrpession
    # similarity won't be supported.
    pass


def levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein distance between two strings.

    Levenshtein distance

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
    if not src:
        return len(tar) * ins_cost
    if not tar:
        return len(src) * del_cost

    if 'dam' in mode:
        return damerau_levenshtein(src, tar, cost)

    # pylint: disable=no-member
    d_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)
    # pylint: enable=no-member
    for i in range(len(src)+1):
        d_mat[i, 0] = i * del_cost
    for j in range(len(tar)+1):
        d_mat[0, j] = j * ins_cost

    for i in range(len(src)):
        for j in range(len(tar)):
            d_mat[i+1, j+1] = min(
                d_mat[i+1, j] + ins_cost,  # ins
                d_mat[i, j+1] + del_cost,  # del
                d_mat[i, j] + (sub_cost if src[i] != tar[j] else 0)  # sub/==
            )

            if mode == 'osa':
                if ((i+1 > 1 and j+1 > 1 and src[i] == tar[j-1] and
                     src[i-1] == tar[j])):
                    # transposition
                    d_mat[i+1, j+1] = min(d_mat[i+1, j+1],
                                          d_mat[i-1, j-1] + trans_cost)

    return d_mat[len(src), len(tar)]


def dist_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the normalized Levenshtein distance between two strings.

    Levenshtein distance normalized to the interval [0, 1]

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
    """Return the Levenshtein similarity of two strings.

    Levenshtein similarity normalized to the interval [0, 1]

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
    """Return the Damerau-Levenshtein distance between two strings.

    Damerau-Levenshtein distance

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

    >>> damerau_levenshtein('cat', 'hat')
    1
    >>> damerau_levenshtein('Niall', 'Neil')
    3
    >>> damerau_levenshtein('aluminum', 'Catalan')
    7
    >>> damerau_levenshtein('ATCG', 'TAGC')
    2
    """
    ins_cost, del_cost, sub_cost, trans_cost = cost

    if src == tar:
        return 0
    if not src:
        return len(tar) * ins_cost
    if not tar:
        return len(src) * del_cost

    if 2*trans_cost < ins_cost + del_cost:
        raise ValueError('Unsupported cost assignment; the cost of two ' +
                         'transpositions must not be less than the cost of ' +
                         'an insert plus a delete.')

    # pylint: disable=no-member
    d_mat = (np.zeros((len(src))*(len(tar)), dtype=np.int).
             reshape((len(src), len(tar))))
    # pylint: enable=no-member

    if src[0] != tar[0]:
        d_mat[0, 0] = min(sub_cost, ins_cost + del_cost)

    src_index_by_character = {}
    src_index_by_character[src[0]] = 0
    for i in range(1, len(src)):
        del_distance = d_mat[i-1, 0] + del_cost
        ins_distance = (i+1) * del_cost + ins_cost
        match_distance = (i * del_cost +
                          (0 if src[i] == tar[0] else sub_cost))
        d_mat[i, 0] = min(del_distance, ins_distance, match_distance)

    for j in range(1, len(tar)):
        del_distance = (j+1) * ins_cost + del_cost
        ins_distance = d_mat[0, j-1] + ins_cost
        match_distance = (j * ins_cost +
                          (0 if src[0] == tar[j] else sub_cost))
        d_mat[0, j] = min(del_distance, ins_distance, match_distance)

    for i in range(1, len(src)):
        max_src_letter_match_index = (0 if src[i] == tar[0] else -1)
        for j in range(1, len(tar)):
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
    """Return the Damerau-Levenshtein similarity of two strings.

    Damerau-Levenshtein distance normalized to the interval [0, 1]

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

    >>> dist_damerau('cat', 'hat')
    0.33333333333333331
    >>> dist_damerau('Niall', 'Neil')
    0.59999999999999998
    >>> dist_damerau('aluminum', 'Catalan')
    0.875
    >>> dist_damerau('ATCG', 'TAGC')
    0.5
    """
    if src == tar:
        return 0
    ins_cost, del_cost = cost[:2]
    return (damerau_levenshtein(src, tar, cost) /
            (max(len(src)*del_cost, len(tar)*ins_cost)))


def sim_damerau(src, tar, cost=(1, 1, 1, 1)):
    """Return the Damerau-Levenshtein similarity of two strings.

    Damerau-Levenshtein similarity normalized to the interval [0, 1]

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

    >>> sim_damerau('cat', 'hat')
    0.66666666666666674
    >>> sim_damerau('Niall', 'Neil')
    0.40000000000000002
    >>> sim_damerau('aluminum', 'Catalan')
    0.125
    >>> sim_damerau('ATCG', 'TAGC')
    0.5
    """
    return 1 - dist_damerau(src, tar, cost)


def hamming(src, tar, difflens=True):
    """Return the Hamming distance between two strings.

    Hamming distance

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

    >>> hamming('cat', 'hat')
    1
    >>> hamming('Niall', 'Neil')
    3
    >>> hamming('aluminum', 'Catalan')
    8
    >>> hamming('ATCG', 'TAGC')
    4
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
    """Return the normalized Hamming distance between two strings.

    Hamming distance normalized to the interval [0, 1]

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

    >>> dist_hamming('cat', 'hat')
    0.3333333333333333
    >>> dist_hamming('Niall', 'Neil')
    0.6
    >>> dist_hamming('aluminum', 'Catalan')
    1.0
    >>> dist_hamming('ATCG', 'TAGC')
    1.0
    """
    if src == tar:
        return 0
    return hamming(src, tar, difflens) / max(len(src), len(tar))


def sim_hamming(src, tar, difflens=True):
    """Return the normalized Hamming similarity of two strings.

    Hamming similarity normalized to the interval [0, 1]

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

    >>> sim_hamming('cat', 'hat')
    0.6666666666666667
    >>> sim_hamming('Niall', 'Neil')
    0.4
    >>> sim_hamming('aluminum', 'Catalan')
    0.0
    >>> sim_hamming('ATCG', 'TAGC')
    0.0
    """
    return 1 - dist_hamming(src, tar, difflens)


def _get_qgrams(src, tar, qval=None, skip=0):
    """Return the Q-Grams in src & tar.

    :param str src, tar: two strings to be compared
        (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :param int skip: the number of characters to skip (only works when
        src and tar are strings
    :return: Q-Grams
    """
    if isinstance(src, Counter) and isinstance(tar, Counter):
        return src, tar
    if qval and qval > 0:
        return (QGrams(src, qval, '$#', skip),
                QGrams(tar, qval, '$#', skip))
    return Counter(src.strip().split()), Counter(tar.strip().split())


def sim_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    r"""Return the Tversky index of two strings.

    Tversky index

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

    >>> sim_tversky('cat', 'hat')
    0.3333333333333333
    >>> sim_tversky('Niall', 'Neil')
    0.2222222222222222
    >>> sim_tversky('aluminum', 'Catalan')
    0.0625
    >>> sim_tversky('ATCG', 'TAGC')
    0.0
    """
    if alpha < 0 or beta < 0:
        raise ValueError('Unsupported weight assignment; alpha and beta ' +
                         'must be greater than or equal to 0.')

    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0

    q_src, q_tar = _get_qgrams(src, tar, qval)
    q_src_mag = sum(q_src.values())
    q_tar_mag = sum(q_tar.values())
    q_intersection_mag = sum((q_src & q_tar).values())

    if not q_src or not q_tar:
        return 0.0

    if bias is None:
        return q_intersection_mag / (q_intersection_mag + alpha *
                                     (q_src_mag - q_intersection_mag) +
                                     beta * (q_tar_mag - q_intersection_mag))

    a_val = min(q_src_mag - q_intersection_mag,
                q_tar_mag - q_intersection_mag)
    b_val = max(q_src_mag - q_intersection_mag,
                q_tar_mag - q_intersection_mag)
    c_val = q_intersection_mag + bias
    return c_val / (beta * (alpha * a_val + (1 - alpha) * b_val) + c_val)


def dist_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tverssky distance between two strings.

    Tversky distance

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

    >>> dist_tversky('cat', 'hat')
    0.6666666666666667
    >>> dist_tversky('Niall', 'Neil')
    0.7777777777777778
    >>> dist_tversky('aluminum', 'Catalan')
    0.9375
    >>> dist_tversky('ATCG', 'TAGC')
    1.0
    """
    return 1 - sim_tversky(src, tar, qval, alpha, beta, bias)


def sim_dice(src, tar, qval=2):
    r"""Return the Sørensen–Dice coefficient of two strings.

    Sørensen–Dice coefficient

    For two sets X and Y, the Sørensen–Dice coefficient is
    :math:`sim_{dice}(X, Y) = \\frac{2 \\cdot |X \\cap Y|}{|X| + |Y|}`

    This is identical to the Tanimoto similarity coefficient
    and the Tversky index for :math:`\\alpha = \\beta = 0.5`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Sørensen–Dice similarity
    :rtype: float

    >>> sim_dice('cat', 'hat')
    0.5
    >>> sim_dice('Niall', 'Neil')
    0.36363636363636365
    >>> sim_dice('aluminum', 'Catalan')
    0.11764705882352941
    >>> sim_dice('ATCG', 'TAGC')
    0.0
    """
    return sim_tversky(src, tar, qval, 0.5, 0.5)


def dist_dice(src, tar, qval=2):
    """Return the Sørensen–Dice distance between two strings.

    Sørensen–Dice distance

    Sørensen–Dice distance is the complemenjt of the Sørensen–Dice coefficient:
    :math:`dist_{dice} = 1 - sim_{dice}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Sørensen–Dice distance
    :rtype: float

    >>> dist_dice('cat', 'hat')
    0.5
    >>> dist_dice('Niall', 'Neil')
    0.6363636363636364
    >>> dist_dice('aluminum', 'Catalan')
    0.8823529411764706
    >>> dist_dice('ATCG', 'TAGC')
    1.0
    """
    return 1 - sim_dice(src, tar, qval)


def sim_jaccard(src, tar, qval=2):
    r"""Return the Jaccard similarity of two strings.

    Jaccard similarity coefficient

    For two sets X and Y, the Jaccard similarity coefficient is
    :math:`sim_{jaccard}(X, Y) = \\frac{|X \\cap Y|}{|X \\cup Y|}`

    This is identical to the Tanimoto similarity coefficient
    and the Tversky index for :math:`\\alpha = \\beta = 1`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Jaccard similarity
    :rtype: float

    >>> sim_jaccard('cat', 'hat')
    0.3333333333333333
    >>> sim_jaccard('Niall', 'Neil')
    0.2222222222222222
    >>> sim_jaccard('aluminum', 'Catalan')
    0.0625
    >>> sim_jaccard('ATCG', 'TAGC')
    0.0
    """
    return sim_tversky(src, tar, qval, 1, 1)


def dist_jaccard(src, tar, qval=2):
    """Return the Jaccard distance between two strings.

    Jaccard distance

    Jaccard distance is the complement of the Jaccard similarity coefficient:
    :math:`dist_{Jaccard} = 1 - sim_{Jaccard}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Jaccard distance
    :rtype: float

    >>> dist_jaccard('cat', 'hat')
    0.6666666666666667
    >>> dist_jaccard('Niall', 'Neil')
    0.7777777777777778
    >>> dist_jaccard('aluminum', 'Catalan')
    0.9375
    >>> dist_jaccard('ATCG', 'TAGC')
    1.0
    """
    return 1 - sim_jaccard(src, tar, qval)


def sim_overlap(src, tar, qval=2):
    r"""Return the overlap coefficient of two strings.

    Overlap coefficient

    For two sets X and Y, the overlap coefficient is
    :math:`sim_{overlap}(X, Y) = \\frac{|X \\cap Y|}{min(|X|, |Y|)}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: overlap similarity
    :rtype: float

    >>> sim_overlap('cat', 'hat')
    0.5
    >>> sim_overlap('Niall', 'Neil')
    0.4
    >>> sim_overlap('aluminum', 'Catalan')
    0.125
    >>> sim_overlap('ATCG', 'TAGC')
    0.0
    """
    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0

    q_src, q_tar = _get_qgrams(src, tar, qval)
    q_src_mag = sum(q_src.values())
    q_tar_mag = sum(q_tar.values())
    q_intersection_mag = sum((q_src & q_tar).values())

    return q_intersection_mag / min(q_src_mag, q_tar_mag)


def dist_overlap(src, tar, qval=2):
    """Return the overlap distance between two strings.

    Overlap distance

    Overlap distance is the complement of the overlap coefficient:
    :math:`sim_{overlap} = 1 - dist_{overlap}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: overlap distance
    :rtype: float

    >>> dist_overlap('cat', 'hat')
    0.5
    >>> dist_overlap('Niall', 'Neil')
    0.6
    >>> dist_overlap('aluminum', 'Catalan')
    0.875
    >>> dist_overlap('ATCG', 'TAGC')
    1.0
    """
    return 1 - sim_overlap(src, tar, qval)


def sim_tanimoto(src, tar, qval=2):
    r"""Return the Tanimoto similarity of two strings.

    Tanimoto similarity

    For two sets X and Y, the Tanimoto similarity coefficient is
    :math:`sim_{Tanimoto}(X, Y) = \\frac{|X \\cap Y|}{|X \\cup Y|}`
    This is identical to the Jaccard similarity coefficient
    and the Tversky index for :math:`\\alpha = \\beta = 1`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Tanimoto similarity
    :rtype: float

    >>> sim_tanimoto('cat', 'hat')
    0.3333333333333333
    >>> sim_tanimoto('Niall', 'Neil')
    0.2222222222222222
    >>> sim_tanimoto('aluminum', 'Catalan')
    0.0625
    >>> sim_tanimoto('ATCG', 'TAGC')
    0.0
    """
    return sim_jaccard(src, tar, qval)


def tanimoto(src, tar, qval=2):
    """Return the Tanimoto distance between two strings.

    Tanimoto distance

    Tanimoto distance is :math:`-log_{2}sim_{Tanimoto}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: Tanimoto distance
    :rtype: float

    >>> tanimoto('cat', 'hat')
    -1.5849625007211563
    >>> tanimoto('Niall', 'Neil')
    -2.1699250014423126
    >>> tanimoto('aluminum', 'Catalan')
    -4.0
    >>> tanimoto('ATCG', 'TAGC')
    -inf
    """
    coeff = sim_jaccard(src, tar, qval)
    if coeff != 0:
        return math.log(coeff, 2)

    return float('-inf')


def minkowski(src, tar, qval=2, pval=1, normalize=False):
    """Return the Minkowski distance (:math:`L^p-norm`) of two strings.

    :param src:
    :param tar:
    :param qval:
    :param pval:
    :return:
    """
    q_src, q_tar = _get_qgrams(src, tar, qval)
    diffs = ((q_src - q_tar) + (q_tar - q_src)).values()

    normalizer = 1
    if normalize:
        totals = (q_src + q_tar).values()
        if pval == 0:
            normalizer = len(totals)
        else:
            normalizer = sum(_**pval for _ in totals)**(1 / pval)

    if pval == float('inf'):
        # Chebyshev distance
        return max(diffs)/normalizer
    if pval == 0:
        # This is the l_0 "norm" as developed by David Donoho
        return len(diffs)
    return sum(_**pval for _ in diffs)**(1 / pval)/normalizer


def dist_minkowski(src, tar, qval=2, pval=1):
    """Return Minkowski distance of two strings, normalized to [0, 1].

    :param src:
    :param tar:
    :param qval2:
    :param pval:
    :return:
    """
    return minkowski(src, tar, qval, pval, True)


def sim_minkowski(src, tar, qval=2, pval=1):
    """Return Minkowski similarity of two strings, normalized to [0, 1].

    :param src:
    :param tar:
    :param qval2:
    :param pval:
    :return:
    """
    return 1-minkowski(src, tar, qval, pval, True)


def manhattan(src, tar, qval=2, normalize=False):
    """Return the Manhattan distance between two strings.

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return minkowski(src, tar, qval, 1, normalize)


def dist_manhattan(src, tar, qval=2):
    """Return the Manhattan distance between two strings, normalized to [0, 1].

    This is identical to Canberra distance.

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return manhattan(src, tar, qval, 1, True)


def sim_manhattan(src, tar, qval=2):
    """Return the Manhattan similarity of two strings, normalized to [0, 1].

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return 1-manhattan(src, tar, qval, 1, True)


def euclidean(src, tar, qval=2, normalize=False):
    """Return the Euclidean distance between two strings.

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return minkowski(src, tar, qval, 2, normalize)


def dist_euclidean(src, tar, qval=2):
    """Return the Euclidean distance between two strings, normalized to [0, 1].

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return euclidean(src, tar, qval, True)


def sim_euclidean(src, tar, qval=2):
    """Return the Euclidean similarity of two strings, normalized to [0, 1].

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return 1-euclidean(src, tar, qval, True)


def chebyshev(src, tar, qval=2, normalize=False):
    """Return the Chebyshev distance between two strings.

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return minkowski(src, tar, qval, float('inf'), normalize)


def dist_chebyshev(src, tar, qval=2):
    """Return the Chebyshev distance between two strings, normalized to [0, 1].

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return chebyshev(src, tar, qval, True)


def sim_chebyshev(src, tar, qval=2):
    """Return the Chebyshev similarity of two strings, normalized to [0, 1].

    :param src:
    :param tar:
    :param qval:
    :return:
    """
    return 1 - chebyshev(src, tar, qval, True)


def sim_cosine(src, tar, qval=2):
    r"""Return the cosine similarity of two strings.

    Cosine similarity (Ochiai coefficient)

    For two sets X and Y, the cosine similarity (Ochiai coefficient) is:
    :math:`sim_{cosine}(X, Y) = \\frac{|X \\cap Y|}{\\sqrt{|X| \\cdot |Y|}}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: cosine similarity
    :rtype: float

    >>> sim_cosine('cat', 'hat')
    0.5
    >>> sim_cosine('Niall', 'Neil')
    0.3651483716701107
    >>> sim_cosine('aluminum', 'Catalan')
    0.11785113019775793
    >>> sim_cosine('ATCG', 'TAGC')
    0.0
    """
    if src == tar:
        return 1.0
    if not src or not tar:
        return 0.0

    q_src, q_tar = _get_qgrams(src, tar, qval)
    q_src_mag = sum(q_src.values())
    q_tar_mag = sum(q_tar.values())
    q_intersection_mag = sum((q_src & q_tar).values())

    return q_intersection_mag / math.sqrt(q_src_mag * q_tar_mag)


def dist_cosine(src, tar, qval=2):
    """Return the cosine distance between two strings.

    Cosine distance

    Cosine distance is the complement of cosine similarity:
    :math:`dist_{cosine} = 1 - sim_{cosine}`

    :param str src, tar: two strings to be compared (or QGrams/Counter objects)
    :param int qval: the length of each q-gram; 0 or None for non-q-gram
        version
    :returns: cosine distance
    :rtype: float

    >>> dist_cosine('cat', 'hat')
    0.5
    >>> dist_cosine('Niall', 'Neil')
    0.6348516283298893
    >>> dist_cosine('aluminum', 'Catalan')
    0.882148869802242
    >>> dist_cosine('ATCG', 'TAGC')
    1.0
    """
    return 1 - sim_cosine(src, tar, qval)


def sim_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 similarity of two strings.

    strcmp95 similarity

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

    >>> sim_strcmp95('cat', 'hat')
    0.7777777777777777
    >>> sim_strcmp95('Niall', 'Neil')
    0.8454999999999999
    >>> sim_strcmp95('aluminum', 'Catalan')
    0.6547619047619048
    >>> sim_strcmp95('ATCG', 'TAGC')
    0.8333333333333334
    """
    def _inrange(char):
        """Return True if char is in the range (0, 91)."""
        return ord(char) > 0 and ord(char) < 91

    ying = src.strip().upper()
    yang = tar.strip().upper()

    if ying == yang:
        return 1.0
    # If either string is blank - return - added in Version 2
    if not ying or not yang:
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
    for i in range(len(ying)):
        lowlim = (i - search_range) if (i >= search_range) else 0
        hilim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in range(lowlim, hilim+1):
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
    for i in range(len(ying)):
        if ying_flag[i] != 0:
            for j in range(k, len(yang)):
                if yang_flag[j] != 0:
                    k = j + 1
                    break
            if ying[i] != yang[j]:
                n_trans += 1
    n_trans = n_trans // 2

    # Adjust for similarities in unmatched characters
    n_simi = 0
    if minv > num_com:
        for i in range(len(ying)):
            if ying_flag[i] == 0 and _inrange(ying[i]):
                for j in range(len(yang)):
                    if yang_flag[j] == 0 and _inrange(yang[j]):
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
    """Return the strcmp95 distance between two strings.

    strcmp95 distance

    strcmp95 distance is 1 - strcmp95 similarity

    :param str src, tar: two strings to be compared
    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large. It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :returns: strcmp95 distance
    :rtype: float

    >>> dist_strcmp95('cat', 'hat')
    0.22222222222222232
    >>> dist_strcmp95('Niall', 'Neil')
    0.15450000000000008
    >>> dist_strcmp95('aluminum', 'Catalan')
    0.34523809523809523
    >>> dist_strcmp95('ATCG', 'TAGC')
    0.16666666666666663
    """
    return 1 - sim_strcmp95(src, tar, long_strings)


def sim_jaro_winkler(src, tar, qval=1, mode='winkler', long_strings=False,
                     boost_threshold=0.7, scaling_factor=0.1):
    """Return the Jaro or Jaro-Winkler similarity of two strings.

    Jaro(-Winkler) distance

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

    >>> sim_jaro_winkler('cat', 'hat')
    0.7777777777777777
    >>> sim_jaro_winkler('Niall', 'Neil')
    0.8049999999999999
    >>> sim_jaro_winkler('aluminum', 'Catalan')
    0.6011904761904762
    >>> sim_jaro_winkler('ATCG', 'TAGC')
    0.8333333333333334

    >>> sim_jaro_winkler('cat', 'hat', mode='jaro')
    0.7777777777777777
    >>> sim_jaro_winkler('Niall', 'Neil', mode='jaro')
    0.7833333333333333
    >>> sim_jaro_winkler('aluminum', 'Catalan', mode='jaro')
    0.6011904761904762
    >>> sim_jaro_winkler('ATCG', 'TAGC', mode='jaro')
    0.8333333333333334
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
    for i in range(lens):
        lowlim = (i - search_range) if (i >= search_range) else 0
        hilim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in range(lowlim, hilim+1):
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
    for i in range(lens):
        if src_flag[i] != 0:
            for j in range(k, lent):
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
    """Return the Jaro or Jaro-Winkler distance between two strings.

    Jaro(-Winkler) distance

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

    >>> dist_jaro_winkler('cat', 'hat')
    0.22222222222222232
    >>> dist_jaro_winkler('Niall', 'Neil')
    0.19500000000000006
    >>> dist_jaro_winkler('aluminum', 'Catalan')
    0.39880952380952384
    >>> dist_jaro_winkler('ATCG', 'TAGC')
    0.16666666666666663

    >>> dist_jaro_winkler('cat', 'hat', mode='jaro')
    0.22222222222222232
    >>> dist_jaro_winkler('Niall', 'Neil', mode='jaro')
    0.21666666666666667
    >>> dist_jaro_winkler('aluminum', 'Catalan', mode='jaro')
    0.39880952380952384
    >>> dist_jaro_winkler('ATCG', 'TAGC', mode='jaro')
    0.16666666666666663
    """
    return 1 - sim_jaro_winkler(src, tar, qval, mode, long_strings,
                                boost_threshold, scaling_factor)


def lcsseq(src, tar):
    """Return the longest common subsequence of two strings.

    Longest common subsequence (LCSseq)

    Based on the dynamic programming algorithm from
    http://rosettacode.org/wiki/Longest_common_subsequence#Dynamic_Programming_6
    This is licensed GFDL 1.2

    Modifications include:
        conversion to a numpy array in place of a list of lists

    :param str src, tar: two strings to be compared
    :returns: the longes common subsequence
    :rtype: str

    >>> lcsseq('cat', 'hat')
    'at'
    >>> lcsseq('Niall', 'Neil')
    'Nil'
    >>> lcsseq('aluminum', 'Catalan')
    'aln'
    >>> lcsseq('ATCG', 'TAGC')
    'AC'
    """
    # pylint: disable=no-member
    lengths = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)
    # pylint: enable=no-member

    # row 0 and column 0 are initialized to 0 already
    for i, src_char in enumerate(src):
        for j, tar_char in enumerate(tar):
            if src_char == tar_char:
                lengths[i+1, j+1] = lengths[i, j] + 1
            else:
                lengths[i+1, j+1] = max(lengths[i+1, j], lengths[i, j+1])

    # read the substring out from the matrix
    result = ''
    i, j = len(src), len(tar)
    while i != 0 and j != 0:
        if lengths[i, j] == lengths[i-1, j]:
            i -= 1
        elif lengths[i, j] == lengths[i, j-1]:
            j -= 1
        else:
            result = src[i-1] + result
            i -= 1
            j -= 1
    return result


def sim_lcsseq(src, tar):
    r"""Return the longest common subsequence similarity of two strings.

    Longest common subsequence similarity (:math:`sim_{LCSseq}`)

    This employs the LCSseq function to derive a similarity metric:
    :math:`sim_{LCSseq}(s,t) = \\frac{|LCSseq(s,t)|}{max(|s|, |t|)}`

    :param str src, tar: two strings to be compared
    :returns: LCSseq similarity
    :rtype: float

    >>> sim_lcsseq('cat', 'hat')
    0.6666666666666666
    >>> sim_lcsseq('Niall', 'Neil')
    0.6
    >>> sim_lcsseq('aluminum', 'Catalan')
    0.375
    >>> sim_lcsseq('ATCG', 'TAGC')
    0.5
    """
    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0
    return len(lcsseq(src, tar)) / max(len(src), len(tar))


def dist_lcsseq(src, tar):
    """Return the longest common subsequence distance between two strings.

    Longest common subsequence distance (:math:`dist_{LCSseq}`)

    This employs the LCSseq function to derive a similarity metric:
    :math:`dist_{LCSseq}(s,t) = 1 - sim_{LCSseq}(s,t)`

    :param str src, tar: two strings to be compared
    :returns: LCSseq distance
    :rtype: float

    >>> dist_lcsseq('cat', 'hat')
    0.33333333333333337
    >>> dist_lcsseq('Niall', 'Neil')
    0.4
    >>> dist_lcsseq('aluminum', 'Catalan')
    0.625
    >>> dist_lcsseq('ATCG', 'TAGC')
    0.5
    """
    return 1 - sim_lcsseq(src, tar)


def lcsstr(src, tar):
    """Return the longest common substring of two strings.

    Longest common substring (LCSstr)

    Based on the code from
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python
    This is licensed Creative Commons: Attribution-ShareAlike 3.0

    Modifications include:

        - conversion to a numpy array in place of a list of lists
        - conversion to Python 2/3-safe range from xrange via six

    :param str src, tar: two strings to be compared
    :returns: the longes common substring
    :rtype: float

    >>> lcsstr('cat', 'hat')
    'at'
    >>> lcsstr('Niall', 'Neil')
    'N'
    >>> lcsstr('aluminum', 'Catalan')
    'al'
    >>> lcsstr('ATCG', 'TAGC')
    'A'
    """
    # pylint: disable=no-member
    lengths = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)
    # pylint: enable=no-member
    longest, i_longest = 0, 0
    for i in range(1, len(src)+1):
        for j in range(1, len(tar)+1):
            if src[i-1] == tar[j-1]:
                lengths[i, j] = lengths[i-1, j-1] + 1
                if lengths[i, j] > longest:
                    longest = lengths[i, j]
                    i_longest = i
            else:
                lengths[i, j] = 0
    return src[i_longest - longest:i_longest]


def sim_lcsstr(src, tar):
    r"""Return the longest common substring similarity of two strings.

    Longest common substring similarity (:math:`sim_{LCSstr}`)

    This employs the LCS function to derive a similarity metric:
    :math:`sim_{LCSstr}(s,t) = \\frac{|LCSstr(s,t)|}{max(|s|, |t|)}`

    :param str src, tar: two strings to be compared
    :returns: LCSstr similarity
    :rtype: float

    >>> sim_lcsstr('cat', 'hat')
    0.6666666666666666
    >>> sim_lcsstr('Niall', 'Neil')
    0.2
    >>> sim_lcsstr('aluminum', 'Catalan')
    0.25
    >>> sim_lcsstr('ATCG', 'TAGC')
    0.25
    """
    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0
    return len(lcsstr(src, tar)) / max(len(src), len(tar))


def dist_lcsstr(src, tar):
    """Return the longest common substring distance between two strings.

    Longest common substring distance (:math:`dist_{LCSstr}`)

    This employs the LCS function to derive a similarity metric:
    :math:`dist_{LCSstr}(s,t) = 1 - sim_{LCSstr}(s,t)`

    :param str src, tar: two strings to be compared
    :returns: LCSstr distance
    :rtype: float

    >>> dist_lcsstr('cat', 'hat')
    0.33333333333333337
    >>> dist_lcsstr('Niall', 'Neil')
    0.8
    >>> dist_lcsstr('aluminum', 'Catalan')
    0.75
    >>> dist_lcsstr('ATCG', 'TAGC')
    0.75
    """
    return 1 - sim_lcsstr(src, tar)


def sim_ratcliff_obershelp(src, tar):
    """Return the Ratcliff-Obershelp similarity of two strings.

    Ratcliff-Obershelp similarity

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

    >>> sim_ratcliff_obershelp('cat', 'hat')
    0.66666666666666663
    >>> sim_ratcliff_obershelp('Niall', 'Neil')
    0.66666666666666663
    >>> sim_ratcliff_obershelp('aluminum', 'Catalan')
    0.40000000000000002
    >>> sim_ratcliff_obershelp('ATCG', 'TAGC')
    0.5
    """
    def _lcsstr_stl(src, tar):
        """Return start positions & length for Ratcliff-Obershelp.

        Return the start position in the source string, start position in
        the target string, and length of the longest common substring of
        strings src and tar.
        """
        # pylint: disable=no-member
        lengths = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)
        # pylint: enable=no-member
        longest, src_longest, tar_longest = 0, 0, 0
        for i in range(1, len(src)+1):
            for j in range(1, len(tar)+1):
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
        """Return the sum of substring match lengths.

        This follows the Ratcliff-Obershelp algorithm:
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
    elif not src or not tar:
        return 0.0
    return 2*_sstr_matches(src, tar)/(len(src)+len(tar))


def dist_ratcliff_obershelp(src, tar):
    """Return the Ratcliff-Obershelp distance between two strings.

    Ratcliff-Obershelp distance

    Ratcliff-Obsershelp distance the complement of Ratcliff-Obershelp
    similarity:
    :math:`dist_{Ratcliff-Obershelp} = 1 - sim_{Ratcliff-Obershelp}`

    :param str src, tar: two strings to be compared
    :returns: Ratcliffe-Obershelp distance
    :rtype: float

    >>> dist_ratcliff_obershelp('cat', 'hat')
    0.33333333333333337
    >>> dist_ratcliff_obershelp('Niall', 'Neil')
    0.33333333333333337
    >>> dist_ratcliff_obershelp('aluminum', 'Catalan')
    0.59999999999999998
    >>> dist_ratcliff_obershelp('ATCG', 'TAGC')
    0.5
    """
    return 1 - sim_ratcliff_obershelp(src, tar)


def mra_compare(src, tar):
    """Return the MRA comparison rating of two strings.

    Western Airlines Surname Match Rating Algorithm comparison rating

    A description of the algorithm can be found on page 18 of
    https://archive.org/details/accessingindivid00moor

    :param str src, tar: two strings to be compared
    :returns: MRA comparison rating
    :rtype: int

    >>> mra_compare('cat', 'hat')
    5
    >>> mra_compare('Niall', 'Neil')
    6
    >>> mra_compare('aluminum', 'Catalan')
    0
    >>> mra_compare('ATCG', 'TAGC')
    5
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

    for _ in range(2):
        new_src = []
        new_tar = []
        minlen = min(len(src), len(tar))
        for i in range(minlen):
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
    """Return the normalized MRA similarity of two strings.

    Normalized Match Rating Algorithm similarity

    This is the MRA normalized to :math:`[0, 1]`, given that MRA itself is
    constrained to the range :math:`[0, 6]`.

    :param str src, tar: two strings to be compared
    :returns: normalized MRA similarity
    :rtype: float

    >>> sim_mra('cat', 'hat')
    0.8333333333333334
    >>> sim_mra('Niall', 'Neil')
    1.0
    >>> sim_mra('aluminum', 'Catalan')
    0.0
    >>> sim_mra('ATCG', 'TAGC')
    0.8333333333333334
    """
    return mra_compare(src, tar)/6


def dist_mra(src, tar):
    """Return the normalized MRA distance between two strings.

    Normalized Match Rating Algorithm distance

    MRA distance is the complement of MRA similarity:
    :math:`dist_{MRA} = 1 - sim_{MRA}`

    :param str src, tar: two strings to be compared
    :returns: normalized MRA distance
    :rtype: float

    >>> dist_mra('cat', 'hat')
    0.16666666666666663
    >>> dist_mra('Niall', 'Neil')
    0.0
    >>> dist_mra('aluminum', 'Catalan')
    1.0
    >>> dist_mra('ATCG', 'TAGC')
    0.16666666666666663
    """
    return 1 - sim_mra(src, tar)


def dist_compression(src, tar, compressor='bz2', probs=None):
    """Return the normalized compression distance between two strings.

    Normalized compression distance (NCD)

    Cf.
    https://en.wikipedia.org/wiki/Normalized_compression_distance#Normalized_compression_distance

    :param str src, tar: two strings to be compared
    :param str compressor: a compression scheme to use for the similarity
        calculation, from the following:

            - `zlib` -- standard zlib/gzip
            - `bz2` -- bzip2 (default)
            - `lzma` -- Lempel–Ziv–Markov chain algorithm
            - `arith` -- arithmetic coding
            - `rle` -- run-length encoding
            - `bwtrle` -- Burrows-Wheeler transform followed by run-length
              encoding

    :param doct probs: a dictionary trained with ac_train (for the arith
        compressor only)
    :returns: compression distance
    :rtype: float

    >>> dist_compression('cat', 'hat')
    0.08
    >>> dist_compression('Niall', 'Neil')
    0.037037037037037035
    >>> dist_compression('aluminum', 'Catalan')
    0.20689655172413793
    >>> dist_compression('ATCG', 'TAGC')
    0.037037037037037035

    >>> dist_compression('Niall', 'Neil', compressor='zlib')
    0.45454545454545453
    >>> dist_compression('Niall', 'Neil', compressor='bz2')
    0.037037037037037035
    >>> dist_compression('Niall', 'Neil', compressor='lzma')
    0.16
    >>> dist_compression('Niall', 'Neil', compressor='arith')
    0.6875
    >>> dist_compression('Niall', 'Neil', compressor='rle')
    1.0
    >>> dist_compression('Niall', 'Neil', compressor='bwtrle')
    0.8333333333333334
    """
    if src == tar:
        return 0.0

    if compressor not in {'arith', 'rle', 'bwtrle'}:
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
    elif compressor in {'rle', 'bwtrle'}:
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
    """Return the normalized compression similarity of two strings.

    Normalized compression similarity (NCS)

    Normalized compression similarity is the complement of normalized
    compression distance:
    :math:`sim_{NCS} = 1 - dist_{NCD}`

    :param str src, tar: two strings to be compared
    :param str compressor: a compression scheme to use for the similarity
        calculation:

            - `zlib` -- standard zlib/gzip
            - `bz2` -- bzip2 (default)
            - `lzma` -- Lempel–Ziv–Markov chain algorithm
            - `arith` -- arithmetic coding
            - `rle` -- run-length encoding
            - `bwtrle` -- Burrows-Wheeler transform followed by run-length
              encoding

    :param dict probs: a dictionary trained with ac_train (for the arith
        compressor only)
    :returns: compression similarity
    :rtype: float

    >>> sim_compression('cat', 'hat')
    0.92
    >>> sim_compression('Niall', 'Neil')
    0.962962962962963
    >>> sim_compression('aluminum', 'Catalan')
    0.7931034482758621
    >>> sim_compression('ATCG', 'TAGC')
    0.962962962962963

    >>> sim_compression('Niall', 'Neil', compressor='zlib')
    0.5454545454545454
    >>> sim_compression('Niall', 'Neil', compressor='bz2')
    0.962962962962963
    >>> sim_compression('Niall', 'Neil', compressor='lzma')
    0.84
    >>> sim_compression('Niall', 'Neil', compressor='arith')
    0.3125
    >>> sim_compression('Niall', 'Neil', compressor='rle')
    0.0
    >>> sim_compression('Niall', 'Neil', compressor='bwtrle')
    0.16666666666666663
    """
    return 1 - dist_compression(src, tar, compressor, probs)


def sim_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan similarity of two strings.

    Monge-Elkan similarity

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

    >>> sim_monge_elkan('cat', 'hat')
    0.75
    >>> sim_monge_elkan('Niall', 'Neil')
    0.66666666666666663
    >>> sim_monge_elkan('aluminum', 'Catalan')
    0.3888888888888889
    >>> sim_monge_elkan('ATCG', 'TAGC')
    0.5
    """
    if src == tar:
        return 1.0

    q_src = sorted(QGrams(src).elements())
    q_tar = sorted(QGrams(tar).elements())

    if not q_src or not q_tar:
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
    """Return the Monge-Elkan distance between two strings.

    Monge-Elkan distance

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

    >>> dist_monge_elkan('cat', 'hat')
    0.25
    >>> dist_monge_elkan('Niall', 'Neil')
    0.33333333333333337
    >>> dist_monge_elkan('aluminum', 'Catalan')
    0.61111111111111116
    >>> dist_monge_elkan('ATCG', 'TAGC')
    0.5
    """
    return 1 - sim_monge_elkan(src, tar, sim_func, symmetric)


def sim_ident(src, tar):
    """Return the identity similarity of two strings.

    Identity similarity

    This is 1 if the two strings are identical, otherwise 0.

    :param str src, tar: two strings to be compared
    :returns: identity similarity
    :rtype: int

    >>> sim_ident('cat', 'hat')
    0
    >>> sim_ident('cat', 'cat')
    1
    """
    return int(src == tar)


def dist_ident(src, tar):
    """Return the identity distance between two strings.

    Identity distance

    This is 0 if the two strings are identical, otherwise 1, i.e.
    :math:`dist_{identity} = 1 - sim_{identity}`

    :param str src, tar: two strings to be compared
    :returns: indentity distance
    :rtype: int

    >>> dist_ident('cat', 'hat')
    1
    >>> dist_ident('cat', 'cat')
    0
    """
    return 1 - sim_ident(src, tar)


def sim_matrix(src, tar, mat=None, mismatch_cost=0, match_cost=1,
               symmetric=True, alphabet=None):
    """Return the matrix similarity of two strings.

    Matrix similarity

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

    >>> sim_matrix('cat', 'hat')
    0
    >>> sim_matrix('hat', 'hat')
    1
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
        return match_cost
    if mat and (src, tar) in mat:
        return mat[(src, tar)]
    elif symmetric and mat and (tar, src) in mat:
        return mat[(tar, src)]
    return mismatch_cost


def needleman_wunsch(src, tar, gap_cost=1, sim_func=sim_ident):
    """Return the Needleman-Wunsch score of two strings.

    Needleman-Wunsch score

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

    >>> needleman_wunsch('cat', 'hat')
    2.0
    >>> needleman_wunsch('Niall', 'Neil')
    1.0
    >>> needleman_wunsch('aluminum', 'Catalan')
    -1.0
    >>> needleman_wunsch('ATCG', 'TAGC')
    0.0
    """
    # pylint: disable=no-member
    d_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.float)
    # pylint: enable=no-member

    for i in range(len(src)+1):
        d_mat[i, 0] = -(i * gap_cost)
    for j in range(len(tar)+1):
        d_mat[0, j] = -(j * gap_cost)
    for i in range(1, len(src)+1):
        for j in range(1, len(tar)+1):
            match = d_mat[i-1, j-1] + sim_func(src[i-1], tar[j-1])
            delete = d_mat[i-1, j] - gap_cost
            insert = d_mat[i, j-1] - gap_cost
            d_mat[i, j] = max(match, delete, insert)
    return d_mat[d_mat.shape[0]-1, d_mat.shape[1]-1]


def smith_waterman(src, tar, gap_cost=1, sim_func=sim_ident):
    """Return the Smith-Waterman score of two strings.

    Smith-Waterman score

    This is the standard edit distance measure.

    Cf. https://en.wikipedia.org/wiki/Smith–Waterman_algorithm

    :param str src, tar: two strings to be compared
    :param float gap_cost: the cost of an alignment gap (1 by default)
    :param function sim_func: a function that returns the similarity of two
        characters (identity similarity by default)
    :returns: Smith-Waterman score
    :rtype: int (in fact dependent on the gap_cost & return value of sim_func)

    >>> smith_waterman('cat', 'hat')
    2.0
    >>> smith_waterman('Niall', 'Neil')
    1.0
    >>> smith_waterman('aluminum', 'Catalan')
    0.0
    >>> smith_waterman('ATCG', 'TAGC')
    1.0
    """
    # pylint: disable=no-member
    d_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.float)
    # pylint: enable=no-member

    for i in range(len(src)+1):
        d_mat[i, 0] = 0
    for j in range(len(tar)+1):
        d_mat[0, j] = 0
    for i in range(1, len(src)+1):
        for j in range(1, len(tar)+1):
            match = d_mat[i-1, j-1] + sim_func(src[i-1], tar[j-1])
            delete = d_mat[i-1, j] - gap_cost
            insert = d_mat[i, j-1] - gap_cost
            d_mat[i, j] = max(0, match, delete, insert)
    return d_mat[d_mat.shape[0]-1, d_mat.shape[1]-1]


def gotoh(src, tar, gap_open=1, gap_ext=0.4, sim_func=sim_ident):
    """Return the Gotoh score of two strings.

    Gotoh score

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

    >>> gotoh('cat', 'hat')
    2.0
    >>> gotoh('Niall', 'Neil')
    1.0
    >>> gotoh('aluminum', 'Catalan')
    -0.40000000000000002
    >>> gotoh('cat', 'hat')
    2.0
    """
    # pylint: disable=no-member
    d_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.float)
    p_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.float)
    q_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.float)
    # pylint: enable=no-member

    d_mat[0, 0] = 0
    p_mat[0, 0] = float('-inf')
    q_mat[0, 0] = float('-inf')
    for i in range(1, len(src)+1):
        d_mat[i, 0] = float('-inf')
        p_mat[i, 0] = -gap_open - gap_ext*(i-1)
        q_mat[i, 0] = float('-inf')
        q_mat[i, 1] = -gap_open
    for j in range(1, len(tar)+1):
        d_mat[0, j] = float('-inf')
        p_mat[0, j] = float('-inf')
        p_mat[1, j] = -gap_open
        q_mat[0, j] = -gap_open - gap_ext*(j-1)

    for i in range(1, len(src)+1):
        for j in range(1, len(tar)+1):
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
    """Return the length similarty of two strings.

    Length similarity

    This is the ratio of the length of the shorter string to the longer.

    :param str src, tar: two strings to be compared
    :returns: length similarity
    :rtype: float

    >>> sim_length('cat', 'hat')
    1.0
    >>> sim_length('Niall', 'Neil')
    0.8
    >>> sim_length('aluminum', 'Catalan')
    0.875
    >>> sim_length('ATCG', 'TAGC')
    1.0
    """
    if src == tar:
        return 1.0
    if not src or not tar:
        return 0.0
    return len(src)/len(tar) if len(src) < len(tar) else len(tar)/len(src)


def dist_length(src, tar):
    """Return the length distance between two strings.

    Length distance

    Length distance is the complement of length similarity:
    :math:`dist_{length} = 1 - sim_{length}`

    :param str src, tar: two strings to be compared
    :returns: length distance
    :rtype: float

    >>> dist_length('cat', 'hat')
    0.0
    >>> dist_length('Niall', 'Neil')
    0.19999999999999996
    >>> dist_length('aluminum', 'Catalan')
    0.125
    >>> dist_length('ATCG', 'TAGC')
    0.0
    """
    return 1 - sim_length(src, tar)


def sim_prefix(src, tar):
    """Return the prefix similarty of two strings.

    Prefix similarity

    Prefix similarity is the ratio of the length of the shorter term that
    exactly matches the longer term to the length of the shorter term,
    beginning at the start of both terms.

    :param str src, tar: two strings to be compared
    :returns: prefix similarity
    :rtype: float

    >>> sim_prefix('cat', 'hat')
    0.0
    >>> sim_prefix('Niall', 'Neil')
    0.25
    >>> sim_prefix('aluminum', 'Catalan')
    0.0
    >>> sim_prefix('ATCG', 'TAGC')
    0.0
    """
    if src == tar:
        return 1.0
    if not src or not tar:
        return 0.0
    min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
    min_len = len(min_word)
    for i in range(min_len, 0, -1):
        if min_word[:i] == max_word[:i]:
            return i/min_len
    return 0.0


def dist_prefix(src, tar):
    """Return the prefix distance between two strings.

    Prefix distance

    Prefix distance is the complement of prefix similarity:
    :math:`dist_{prefix} = 1 - sim_{prefix}`

    :param str src, tar: two strings to be compared
    :returns: prefix distance
    :rtype: float

    >>> dist_prefix('cat', 'hat')
    1.0
    >>> dist_prefix('Niall', 'Neil')
    0.75
    >>> dist_prefix('aluminum', 'Catalan')
    1.0
    >>> dist_prefix('ATCG', 'TAGC')
    1.0
    """
    return 1 - sim_prefix(src, tar)


def sim_suffix(src, tar):
    """Return the suffix similarity of two strings.

    Suffix similarity

    Suffix similarity is the ratio of the length of the shorter term that
    exactly matches the longer term to the length of the shorter term,
    beginning at the end of both terms.

    :param str src, tar: two strings to be compared
    :returns: suffix similarity
    :rtype: float

    >>> sim_suffix('cat', 'hat')
    0.6666666666666666
    >>> sim_suffix('Niall', 'Neil')
    0.25
    >>> sim_suffix('aluminum', 'Catalan')
    0.0
    >>> sim_suffix('ATCG', 'TAGC')
    0.0
    """
    if src == tar:
        return 1.0
    if not src or not tar:
        return 0.0
    min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
    min_len = len(min_word)
    for i in range(min_len, 0, -1):
        if min_word[-i:] == max_word[-i:]:
            return i/min_len
    return 0.0


def dist_suffix(src, tar):
    """Return the suffix distance between two strings.

    Suffix distance

    Suffix distance is the complement of suffix similarity:
    :math:`dist_{suffix} = 1 - sim_{suffix}`

    :param str src, tar: two strings to be compared
    :returns: suffix distance
    :rtype: float

    >>> dist_suffix('cat', 'hat')
    0.33333333333333337
    >>> dist_suffix('Niall', 'Neil')
    0.75
    >>> dist_suffix('aluminum', 'Catalan')
    1.0
    >>> dist_suffix('ATCG', 'TAGC')
    1.0
    """
    return 1 - sim_suffix(src, tar)


def sim_mlipns(src, tar, threshold=0.25, maxmismatches=2):
    """Return the MLIPNS similarity of two strings.

    Modified Language-Independent Product Name Search (MLIPNS)

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

    >>> sim_mlipns('cat', 'hat')
    1.0
    >>> sim_mlipns('Niall', 'Neil')
    0.0
    >>> sim_mlipns('aluminum', 'Catalan')
    0.0
    >>> sim_mlipns('ATCG', 'TAGC')
    0.0
    """
    if tar == src:
        return 1.0
    if not src or not tar:
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
    """Return the MLIPNS distance between two strings.

    Modified Language-Independent Product Name Search (MLIPNS)

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

    >>> dist_mlipns('cat', 'hat')
    0.0
    >>> dist_mlipns('Niall', 'Neil')
    1.0
    >>> dist_mlipns('aluminum', 'Catalan')
    1.0
    >>> dist_mlipns('ATCG', 'TAGC')
    1.0
    """
    return 1.0 - sim_mlipns(src, tar, threshold, maxmismatches)


def bag(src, tar):
    """Return the bag distance between two strings.

    Bag distance

    Bag distance is proposed in Bartolini, Illaria, Paolo Ciaccia, and Marco
    Patella. 2002. "String Matching with Metric Trees Using and Approximate
    Distance." Proceedings of the 9th International Symposium on String
    Processing and Information Retrieval, Lisbon, Portugal, September 2002.
    271-283.
    http://www-db.disi.unibo.it/research/papers/SPIRE02.pdf

    It is defined as:
    :math:`max( |multiset(src)-multiset(tar)|, |multiset(tar)-multiset(src)| )`

    :param str src, tar: two strings to be compared
    :returns: bag distance
    :rtype: int

    >>> bag('cat', 'hat')
    1
    >>> bag('Niall', 'Neil')
    2
    >>> bag('aluminum', 'Catalan')
    5
    >>> bag('ATCG', 'TAGC')
    0
    >>> bag('abcdefg', 'hijklm')
    7
    >>> bag('abcdefg', 'hijklmno')
    8
    """
    if tar == src:
        return 0
    elif not src:
        return len(tar)
    elif not tar:
        return len(src)

    src_bag = Counter(src)
    tar_bag = Counter(tar)
    return max(sum((src_bag-tar_bag).values()),
               sum((tar_bag-src_bag).values()))


def dist_bag(src, tar):
    """Return the normalized bag distance between two strings.

    Normalized bag distance

    Bag distance is normalized by dividing by :math:`max( |src|, |tar| )`.

    :param str src, tar: two strings to be compared
    :returns: normalized bag distance
    :rtype: float

    >>> dist_bag('cat', 'hat')
    0.3333333333333333
    >>> dist_bag('Niall', 'Neil')
    0.4
    >>> dist_bag('aluminum', 'Catalan')
    0.375
    >>> dist_bag('ATCG', 'TAGC')
    0.0
    """
    if tar == src:
        return 0.0
    if not src or not tar:
        return 1.0

    maxlen = max(len(src), len(tar))

    return bag(src, tar)/maxlen


def sim_bag(src, tar):
    """Return the normalized bag similarity of two strings.

    Normalized bag similarity

    Normalized bag similarity is the complement of normalized bag distance:
    :math:`sim_{bag} = 1 - dist_{bag}`

    :param str src, tar: two strings to be compared
    :returns: normalized bag similarity
    :rtype: float

    >>> sim_bag('cat', 'hat')
    0.6666666666666667
    >>> sim_bag('Niall', 'Neil')
    0.6
    >>> sim_bag('aluminum', 'Catalan')
    0.625
    >>> sim_bag('ATCG', 'TAGC')
    1.0
    """
    return 1-dist_bag(src, tar)


def editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the Editex distance between two strings.

    Editex distance

    As described on pages 3 & 4 of
    Zobel, Justin and Philip Dart. 1996. Phonetic string matching: Lessons from
    information retrieval. In: Proceedings of the ACM-SIGIR Conference on
    Research and Development in Information Retrieval, Zurich, Switzerland.
    166–173. https://doi.org/10.1145/243199.243258

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

    >>> editex('cat', 'hat')
    2
    >>> editex('Niall', 'Neil')
    2
    >>> editex('aluminum', 'Catalan')
    12
    >>> editex('ATCG', 'TAGC')
    6
    """
    match_cost, group_cost, mismatch_cost = cost
    letter_groups = ({'A', 'E', 'I', 'O', 'U', 'Y'},
                     {'B', 'P'},
                     {'C', 'K', 'Q'},
                     {'D', 'T'},
                     {'L', 'R'},
                     {'M', 'N'},
                     {'G', 'J'},
                     {'F', 'P', 'V'},
                     {'S', 'X', 'Z'},
                     {'C', 'S', 'Z'})
    all_letters = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z'}

    def r_cost(ch1, ch2):
        """Return r(a,b) according to Zobel & Dart's definition."""
        if ch1 == ch2:
            return match_cost
        if ch1 in all_letters and ch2 in all_letters:
            for group in letter_groups:
                if ch1 in group and ch2 in group:
                    return group_cost
        return mismatch_cost

    def d_cost(ch1, ch2):
        """Return d(a,b) according to Zobel & Dart's definition."""
        if ch1 != ch2 and (ch1 == 'H' or ch1 == 'W'):
            return group_cost
        return r_cost(ch1, ch2)

    # convert both src & tar to NFKD normalized unicode
    src = unicodedata.normalize('NFKD', text_type(src.upper()))
    tar = unicodedata.normalize('NFKD', text_type(tar.upper()))
    # convert ß to SS (for Python2)
    src = src.replace('ß', 'SS')
    tar = tar.replace('ß', 'SS')

    if src == tar:
        return 0
    if not src:
        return len(tar) * mismatch_cost
    if not tar:
        return len(src) * mismatch_cost

    # pylint: disable=no-member
    d_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)
    # pylint: enable=no-member
    lens = len(src)
    lent = len(tar)
    src = ' '+src
    tar = ' '+tar

    if not local:
        for i in range(1, lens+1):
            d_mat[i, 0] = d_mat[i-1, 0] + d_cost(src[i-1], src[i])
    for j in range(1, lent+1):
        d_mat[0, j] = d_mat[0, j-1] + d_cost(tar[j-1], tar[j])

    for i in range(1, lens+1):
        for j in range(1, lent+1):
            d_mat[i, j] = min(d_mat[i-1, j] + d_cost(src[i-1], src[i]),
                              d_mat[i, j-1] + d_cost(tar[j-1], tar[j]),
                              d_mat[i-1, j-1] + r_cost(src[i], tar[j]))

    return d_mat[lens, lent]


def dist_editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the normalized Editex distance between two strings.

    Editex distance normalized to the interval [0, 1]

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

    >>> dist_editex('cat', 'hat')
    0.33333333333333331
    >>> dist_editex('Niall', 'Neil')
    0.20000000000000001
    >>> dist_editex('aluminum', 'Catalan')
    0.75
    >>> dist_editex('ATCG', 'TAGC')
    0.75
    """
    if src == tar:
        return 0
    mismatch_cost = cost[2]
    return (editex(src, tar, cost, local) /
            (max(len(src)*mismatch_cost, len(tar)*mismatch_cost)))


def sim_editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the normalized Editex similarity of two strings.

    Editex similarity normalized to the interval [0, 1]

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

    >>> sim_editex('cat', 'hat')
    0.66666666666666674
    >>> sim_editex('Niall', 'Neil')
    0.80000000000000004
    >>> sim_editex('aluminum', 'Catalan')
    0.25
    >>> sim_editex('ATCG', 'TAGC')
    0.25
    """
    return 1 - dist_editex(src, tar, cost, local)


def eudex_hamming(src, tar, weights='exponential', maxlength=8,
                  normalized=False):
    """Calculate the Hamming distance between the Eudex hashes of two terms.

    - If weights is set to None, a simple Hamming distance is calculated.
    - If weights is set to 'exponential', weight decays by powers of 2, as
      proposed in the eudex specification: https://github.com/ticki/eudex.
    - If weights is set to 'fibonacci', weight decays through the Fibonacci
      series, as in the eudex reference implementation.
    - If weights is set to a callable function, this assumes it creates a
      generator and the generator is used to populate a series of weights.
    - If weights is set to an iterable, the iterable's values should be
      integers and will be used as the weights.

    :param str src, tar: two strings to be compared
    :param iterable or generator function weights:
    :param maxlength: the number of characters to encode as a eudex hash
    :return:
    """
    def _gen_fibonacci():
        """Yield the next Fibonacci number.

        Based on https://www.python-course.eu/generators.php
        Starts at Fibonacci number 3 (the second 1)
        """
        num_a, num_b = 1, 2
        while True:
            yield num_a
            num_a, num_b = num_b, num_a + num_b

    def _gen_exponential(base=2):
        """Yield the next value in an exponential series of the base.

        Based on https://www.python-course.eu/generators.php
        Starts at base**0
        """
        exp = 0
        while True:
            yield base ** exp
            exp += 1

    # Calculate the eudex hashes and XOR them
    xored = eudex(src, maxlength=maxlength) ^ eudex(tar, maxlength=maxlength)

    # Simple hamming distance (all bits are equal)
    if not weights:
        return bin(xored).count('1')

    # If weights is a function, it should create a generator,
    # which we now use to populate a list
    if callable(weights):
        weights = weights()
    elif weights == 'exponential':
        weights = _gen_exponential()
    elif weights == 'fibonacci':
        weights = _gen_fibonacci()
    if isinstance(weights, types.GeneratorType):
        weights = [next(weights) for _ in range(maxlength)][::-1]

    # Sum the weighted hamming distance
    dist = 0
    maxdist = 0
    while (xored or normalized) and weights:
        maxdist += 8*weights[-1]
        dist += bin(xored & 0xFF).count('1') * weights.pop()
        xored >>= 8

    if normalized:
        dist /= maxdist

    return dist


def dist_eudex(src, tar, weights='exponential', maxlength=8):
    """Return normalized Hamming distance between Eudex hashes of two terms.

    - If weights is set to None, a simple Hamming distance is calculated.
    - If weights is set to 'exponential', weight decays by powers of 2, as
      proposed in the eudex specification: https://github.com/ticki/eudex.
    - If weights is set to 'fibonacci', weight decays through the Fibonacci
      series, as in the eudex reference implementation.
    - If weights is set to a callable function, this assumes it creates a
      generator and the generator is used to populate a series of weights.
    - If weights is set to an iterable, the iterable's values should be
      integers and will be used as the weights.

    :param str src, tar: two strings to be compared
    :param iterable or generator function weights:
    :param maxlength: the number of characters to encode as a eudex hash
    :return:
    """
    return eudex_hamming(src, tar, weights, maxlength, True)


def sim_eudex(src, tar, weights='exponential', maxlength=8):
    """Return normalized Hamming similarity between Eudex hashes of two terms.

    - If weights is set to None, a simple Hamming distance is calculated.
    - If weights is set to 'exponential', weight decays by powers of 2, as
      proposed in the eudex specification: https://github.com/ticki/eudex.
    - If weights is set to 'fibonacci', weight decays through the Fibonacci
      series, as in the eudex reference implementation.
    - If weights is set to a callable function, this assumes it creates a
      generator and the generator is used to populate a series of weights.
    - If weights is set to an iterable, the iterable's values should be
      integers and will be used as the weights.

    :param str src, tar: two strings to be compared
    :param iterable or generator function weights:
    :param maxlength: the number of characters to encode as a eudex hash
    :return:
    """
    return 1-dist_eudex(src, tar, weights, maxlength)


def sift4_simplest(src, tar, max_offset=0):
    """Return the "simplest" Sift4 distance between two terms.

    This is an approximation of edit distance, described in:
    Zackwehdex, Siderite. 2014. "Super Fast and Accurate string distance
    algorithm: Sift4."
    https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html

    :param str src, tar: two strings to be compared
    :param max_offset: the number of characters to search for matching letters
    :return:
    """
    if not src:
        return len(tar)

    if not tar:
        return len(src)

    src_len = len(src)
    tar_len = len(tar)

    src_cur = 0
    tar_cur = 0
    lcss = 0
    local_cs = 0

    while (src_cur < src_len) and (tar_cur < tar_len):
        if src[src_cur] == tar[tar_cur]:
            local_cs += 1
        else:
            lcss += local_cs
            local_cs = 0
            if src_cur != tar_cur:
                src_cur = tar_cur = max(src_cur, tar_cur)
            for i in range(max_offset):
                if not ((src_cur+i < src_len) or (tar_cur+i < tar_len)):
                    break
                if (src_cur+i < src_len) and (src[src_cur+i] == tar[tar_cur]):
                    src_cur += i
                    local_cs += 1
                    break
                if (tar_cur+i < tar_len) and (src[src_cur] == tar[tar_cur+i]):
                    tar_cur += i
                    local_cs += 1
                    break

        src_cur += 1
        tar_cur += 1

    lcss += local_cs
    return round(max(src_len, tar_len) - lcss)


def sift4_common(src, tar, max_offset=0, max_distance=0):
    """Return the "common" Sift4 distance between two terms.

    This is an approximation of edit distance, described in:
    Zackwehdex, Siderite. 2014. "Super Fast and Accurate string distance
    algorithm: Sift4."
    https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html

    :param str src, tar: two strings to be compared
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :return:
    """
    if not src:
        return len(tar)

    if not tar:
        return len(src)

    src_len = len(src)
    tar_len = len(tar)

    src_cur = 0
    tar_cur = 0
    lcss = 0
    local_cs = 0
    trans = 0
    offset_arr = []

    while (src_cur < src_len) and (tar_cur < tar_len):
        if src[src_cur] == tar[tar_cur]:
            local_cs += 1
            is_trans = False
            i = 0
            while i < len(offset_arr):
                ofs = offset_arr[i]
                if src_cur <= ofs['src_cur'] or tar_cur <= ofs['tar_cur']:
                    is_trans = (abs(tar_cur-src_cur) >=
                                abs(ofs['tar_cur']-ofs['src_cur']))
                    if is_trans:
                        trans += 1
                    elif not ofs['trans']:
                        ofs['trans'] = True
                        trans += 1
                    break
                elif src_cur > ofs['tar_cur'] and tar_cur > ofs['src_cur']:
                    del offset_arr[i]
                else:
                    i += 1

            offset_arr.append({'src_cur': src_cur, 'tar_cur': tar_cur,
                               'trans': is_trans})
        else:
            lcss += local_cs
            local_cs = 0
            if src_cur != tar_cur:
                src_cur = tar_cur = min(src_cur, tar_cur)
            for i in range(max_offset):
                if not ((src_cur+i < src_len) or (tar_cur+i < tar_len)):
                    break
                if (src_cur+i < src_len) and (src[src_cur+i] == tar[tar_cur]):
                    src_cur += i-1
                    tar_cur -= 1
                    break
                if (tar_cur+i < tar_len) and (src[src_cur] == tar[tar_cur+i]):
                    src_cur -= 1
                    tar_cur += i-1
                    break

        src_cur += 1
        tar_cur += 1

        if max_distance:
            temporary_distance = max(src_cur, tar_cur) - lcss + trans
            if temporary_distance >= max_distance:
                return round(temporary_distance)

        if (src_cur >= src_len) or (tar_cur >= tar_len):
            lcss += local_cs
            local_cs = 0
            src_cur = tar_cur = min(src_cur, tar_cur)

    lcss += local_cs
    return round(max(src_len, tar_len) - lcss + trans)


def dist_sift4(src, tar, max_offset=0, max_distance=0):
    """Return the normalized "common" Sift4 distance between two terms.

    This is an approximation of edit distance, described in:
    Zackwehdex, Siderite. 2014. "Super Fast and Accurate string distance
    algorithm: Sift4."
    https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html

    :param str src, tar: two strings to be compared
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :return:
    """
    return (sift4_common(src, tar, max_offset, max_distance) /
            (max(len(src), len(tar))))


def sim_sift4(src, tar, max_offset=0, max_distance=0):
    """Return the normalized "common" Sift4 similarity of two terms.

    This is an approximation of edit distance, described in:
    Zackwehdex, Siderite. 2014. "Super Fast and Accurate string distance
    algorithm: Sift4."
    https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html

    :param str src, tar: two strings to be compared
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :return:
    """
    return 1-dist_sift4(src, tar, max_offset, max_distance)


def sim_baystat(src, tar, min_ss_len=None, left_ext=None, right_ext=None):
    """Return the Baystat similarity.

    Good results for shorter words are reported when setting min_ss_len to 1
    and either left_ext OR right_ext to 1.

    The Baystat similarity is defined in:
    Fürnrohr, Michael, Birgit Rimmelspacher, and Tilman von Roncador. 2002.
    "Zusammenführung von Datenbeständen ohne numerische Identifikatoren: ein
    Verfahren im Rahmen der Testuntersuchungen zu einem registergestützten
    Zensus." Bayern in Zahlen, 2002(7). 308--321.
    https://www.statistik.bayern.de/medien/statistik/zensus/zusammenf__hrung_von_datenbest__nden_ohne_numerische_identifikatoren.pdf

    This is ostensibly a port of the R module PPRL's implementation:
    https://github.com/cran/PPRL/blob/master/src/MTB_Baystat.cpp
    As such, this could be made more pythonic.

    :param str src, tar: two strings to be compared
    :param int min_ss_len: minimum substring length to be considered
    :param int left_ext: left-side extension length
    :param int right_ext: right-side extension length
    :rtype: float
    :return: the Baystat similarity
    """
    if src == tar:
        return 1
    if not src or not tar:
        return 0

    max_len = max(len(src), len(tar))

    if not (min_ss_len and left_ext and right_ext):
        # These can be set via arguments to the function. Otherwise they are
        # set automatically based on values from the article.
        if max_len >= 7:
            min_ss_len = 2
            left_ext = 2
            right_ext = 2
        else:
            # The paper suggests that for short names, (exclusively) one or the
            # other of left_ext and right_ext can be 1, with good results.
            # I use 0 & 0 as the default in this case.
            min_ss_len = 1
            left_ext = 0
            right_ext = 0

    pos = 0
    match_len = 0

    while (True):
        if pos + min_ss_len > len(src):
            return match_len/max_len

        hit_len = 0
        ix = 1

        substring = src[pos:pos + min_ss_len]
        search_begin = pos - left_ext

        if search_begin < 0:
            search_begin = 0
            left_ext_len = pos
        else:
            left_ext_len = left_ext

        if pos + min_ss_len + right_ext >= len(tar):
            right_ext_len = len(tar) - pos - min_ss_len
        else:
            right_ext_len = right_ext

        if (search_begin + left_ext_len + min_ss_len + right_ext_len >
                search_begin):
            search_val = tar[search_begin:(search_begin + left_ext_len +
                                           min_ss_len + right_ext_len)]
        else:
            search_val = ''

        flagged_tar = ''
        while substring in search_val and pos + ix <= len(src):
            hit_len = len(substring)
            flagged_tar = tar.replace(substring, '#'*hit_len)

            if pos + min_ss_len + ix <= len(src):
                substring = src[pos:pos + min_ss_len + ix]

            if pos+min_ss_len + right_ext_len + 1 <= len(tar):
                right_ext_len += 1

            if (search_begin + left_ext_len + min_ss_len + right_ext_len <=
                    len(tar)):
                search_val = tar[search_begin:(search_begin + left_ext_len +
                                               min_ss_len + right_ext_len)]

            ix += 1

        if hit_len > 0:
            tar = flagged_tar

        match_len += hit_len
        pos += ix


def dist_baystat(src, tar, min_ss_len=None, left_ext=None, right_ext=None):
    """Return the Baystat distance.

    :param str src, tar: two strings to be compared
    :param int min_ss_len: minimum substring length to be considered
    :param int left_ext: left-side extension length
    :param int right_ext: right-side extension length
    :rtype: float
    :return: the Baystat distance
    """
    return 1-sim_baystat(src, tar, min_ss_len, left_ext, right_ext)


def typo(src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5)):
    """Return the typo distance between two strings.

    This is inspired by Wayne Song's Typo-Distance
    (https://github.com/wsong/Typo-Distance), and a fair bit of this was
    copied from his module. Compared to the original, this has supports
    different metrics for substitution.

    :param str src, tar: two strings to be compared
    :param str metric: supported values include: 'euclidean', 'manhattan',
          'log-euclidean', and 'log-manhattan'
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits: inserts, deletes, substitutions, and shift, respectively (by
        default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless
        a log metric is used.
    :return:
    """
    ins_cost, del_cost, sub_cost, shift_cost = cost

    if src == tar:
        return 0.0
    if not src:
        return len(tar) * ins_cost
    if not tar:
        return len(src) * del_cost

    layout = {'QWERTY': (
        (('`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='),
         ('', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
          '\\'),
         ('', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\''),
         ('', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'),
         ('', '', ' ', ' ', ' ', ' ', ' ', ' ', ' ')),
        (('~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'),
         ('', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'),
         ('', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'),
         ('', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?'),
         ('', '', ' ', ' ', ' ', ' ', ' ', ' ', ' '))
    )}

    keyboard = layout['QWERTY']
    lowercase = {item for sublist in keyboard[0] for item in sublist}
    uppercase = {item for sublist in keyboard[1] for item in sublist}

    def _kb_array_for_char(char):
        """Return the keyboard layout that contains ch."""
        if char in lowercase:
            return keyboard[0]
        elif char in uppercase:
            return keyboard[1]
        else:
            raise ValueError(char + ' not found in any keyboard layouts')

    def _get_char_coord(char, keyboard):
        """Return the row & column of char in the keyboard."""
        for row in keyboard:
            if char in row:
                return keyboard.index(row), row.index(char)
        raise ValueError(char + ' not found in given keyboard layout')

    def _euclidean_keyboard_distance(char1, char2):
        row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
        row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
        return ((row1 - row2) ** 2 + (col1 - col2) ** 2) ** 0.5

    def _manhattan_keyboard_distance(char1, char2):
        row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
        row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
        return abs(row1 - row2) + abs(col1 - col2)

    def _log_euclidean_keyboard_distance(char1, char2):
        return math.log(1 + _euclidean_keyboard_distance(char1, char2))

    def _log_manhattan_keyboard_distance(char1, char2):
        return math.log(1 + _manhattan_keyboard_distance(char1, char2))

    metric_dict = {'euclidean': _euclidean_keyboard_distance,
                   'manhattan': _manhattan_keyboard_distance,
                   'log-euclidean': _log_euclidean_keyboard_distance,
                   'log-manhattan': _log_manhattan_keyboard_distance}

    def substitution_cost(char1, char2):
        cost = sub_cost
        cost *= (metric_dict[metric](char1, char2) +
                 shift_cost * (_kb_array_for_char(char1) !=
                               _kb_array_for_char(char2)))
        return cost

    d_mat = np.zeros((len(src) + 1, len(tar) + 1), dtype=np.float32)
    for i in range(len(src) + 1):
        d_mat[i, 0] = i * del_cost
    for j in range(len(tar) + 1):
        d_mat[0, j] = j * ins_cost

    for i in range(len(src)):
        for j in range(len(tar)):
            d_mat[i + 1, j + 1] = min(
                d_mat[i + 1, j] + ins_cost,  # ins
                d_mat[i, j + 1] + del_cost,  # del
                d_mat[i, j] + (substitution_cost(src[i], tar[j])
                               if src[i] != tar[j] else 0)  # sub/==
            )

    return d_mat[len(src), len(tar)]


def dist_typo(src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5)):
    """Return the normalized typo distance between two strings.

    This is inspired by Wayne Song's Typo-Distance
    (https://github.com/wsong/Typo-Distance), and a fair bit of this was
    copied from his module. Compared to the original, this has supports
    different metrics for substitution.

    :param str src, tar: two strings to be compared
    :param str metric: supported values include: 'euclidean', 'manhattan',
          'log-euclidean', and 'log-manhattan'
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits: inserts, deletes, substitutions, and shift, respectively (by
        default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless
        a log metric is used.
    :return:
    """
    if src == tar:
        return 0
    ins_cost, del_cost = cost[:2]
    return (typo(src, tar, metric, cost) /
            (max(len(src)*del_cost, len(tar)*ins_cost)))


def sim_typo(src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5)):
    """Return the normalized typo similarity between two strings.

    This is inspired by Wayne Song's Typo-Distance
    (https://github.com/wsong/Typo-Distance), and a fair bit of this was
    copied from his module. Compared to the original, this has supports
    different metrics for substitution.

    :param str src, tar: two strings to be compared
    :param str metric: supported values include: 'euclidean', 'manhattan',
          'log-euclidean', and 'log-manhattan'
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits: inserts, deletes, substitutions, and shift, respectively (by
        default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless
        a log metric is used.
    :return:
    """
    return 1 - dist_typo(src, tar, metric, cost)


def synoname(src, tar, word_approx_min=0.3, char_approx_min=0.73,
             tests=2**11-1):
    """Return the Synoname similarity type of two words.

    :param src:
    :param tar:
    :return:
    """
    punct = {'=', "'", '-', '|', '.', ' '}
    test_dict = {val: n**2 for n, val in enumerate([
        'exact', 'omission', 'substitution', 'transposition', 'punctuation',
        'initials', 'extended', 'inclusion', 'no_first', 'word_approx',
        'confusions', 'char_approx'])}
    match_type_dict = {val: n for n, val in enumerate([
        'exact', 'omission', 'substitution', 'transposition', 'punctuation',
        'initials', 'extended', 'inclusion', 'no_first', 'word_approx',
        'confusions', 'char_approx'], 1)}

    if isinstance(tests, Iterable):
        new_tests = 0
        for term in tests:
            if term in test_dict:
                new_tests += test_dict[term]
        tests = new_tests

    if isinstance(src, tuple):
        src_ln, src_fn, src_qual = src
    else:
        src_ln, src_fn, src_qual = src.split('#')[1:4]
    if isinstance(tar, tuple):
        tar_ln, tar_fn, tar_qual = tar
    else:
        tar_ln, tar_fn, tar_qual = tar.split('#')[1:4]

    # 1. Preprocessing

    # Lowercasing
    src_fn = src_fn.strip().lower()
    src_ln = src_ln.strip().lower()
    src_qual = src_qual.strip().lower()

    tar_fn = tar_fn.strip().lower()
    tar_ln = tar_ln.strip().lower()
    tar_qual = tar_qual.strip().lower()

    # Create toolcodes
    src_fn, src_ln, src_tc = synoname_toolcode(src_fn, src_ln, src_qual)
    tar_fn, tar_ln, tar_tc = synoname_toolcode(tar_fn, tar_ln, tar_qual)

    src_qualcode = int(src_tc[0])
    src_punctcode = int(src_tc[1])
    src_generation = int(src_tc[2])
    src_romancode = int(src_tc[3:6])
    src_len_first = int(src_tc[6:8])
    src_len_last = int(src_tc[8:10])
    src_tc = src_tc.split('#')
    src_specials = src_tc[1]
    src_search_range = src_tc[2]
    src_len_specials = len(src_specials)

    tar_qualcode = int(tar_tc[0])
    tar_punctcode = int(tar_tc[1])
    tar_generation = int(tar_tc[2])
    tar_romancode = int(tar_tc[3:6])
    tar_len_first = int(tar_tc[6:8])
    tar_len_last = int(tar_tc[8:10])
    tar_tc = tar_tc.split('#')
    tar_specials = tar_tc[1]
    tar_search_range = tar_tc[2]
    tar_len_specials = len(tar_specials)

    qual_conflict = src_qual != tar_qual
    gen_conflict = (src_generation != tar_generation and
                    (src_generation or tar_generation))
    roman_conflict = (src_romancode != tar_romancode and
                      (src_romancode or tar_romancode))

    # approx_c
    def approx_c():
        if gen_conflict or roman_conflict:
            return False, 0.0
        full_name = ' '.join((tar_ln, tar_fn))
        if full_name.startswith('master '):
            full_name = full_name[len('master '):]
            for intro in ['of the ', 'of ', 'known as the ', 'with the ',
                          'with ']:
                if full_name.startswith(intro):
                    full_name = full_name[len(intro):]

        # ca_ratio = simil(cap_full_name, full_name)
        return ca_ratio >= char_approx_min, ca_ratio

    def simil(src, tar):
        return 100*sim_ratcliff_obershelp(src, tar)

    approx_c_result, ca_ratio = approx_c()

    if ca_ratio >= char_approx_min and ca_ratio >= 70:
        if tests & test_dict['exact'] and src == tar:
            return 1


def sim_tfidf(src, tar, qval=2, docs_src=None, docs_tar=None):
    """Return the TF-IDF similarity of two strings.

    TF-IDF similarity

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
    elif not src or not tar:
        return 0.0

    q_src, q_tar = _get_qgrams(src, tar, qval)

    if isinstance(docs_src, Counter):
        q_docs = docs_src
    elif qval and qval > 0:
        q_docs = QGrams(docs_src, qval)
    else:
        q_docs = Counter(docs_src.strip().split())

    if not q_src or not q_tar:
        return 0.0

    # TODO: finish implementation
    return 0.5  # hardcoded to half

###############################################################################


def sim(src, tar, method=sim_levenshtein):
    """Return a similarity of two strings.

    This is a generalized function for calling other similarity functions.

    :param str src, tar: two strings to be compared
    :param function method: specifies the similarity metric (Levenshtein by
        default)
    :returns: similarity according to the specified function
    :rtype: float

    >>> sim('cat', 'hat')
    0.66666666666666674
    >>> sim('Niall', 'Neil')
    0.40000000000000002
    >>> sim('aluminum', 'Catalan')
    0.125
    >>> sim('ATCG', 'TAGC')
    0.25
    """
    if callable(method):
        return method(src, tar)
    else:
        raise AttributeError('Unknown similarity function: ' + str(method))


def dist(src, tar, method=sim_levenshtein):
    """Return a distance between two strings.

    This is a generalized function for calling other distance functions.

    :param str src, tar: two strings to be compared
    :param function method: specifies the similarity metric (Levenshtein by
        default) -- Note that this takes a similarity metric function, not
        a distance metric function.
    :returns: distance according to the specified function
    :rtype: float

    >>> dist('cat', 'hat')
    0.33333333333333326
    >>> dist('Niall', 'Neil')
    0.59999999999999998
    >>> dist('aluminum', 'Catalan')
    0.875
    >>> dist('ATCG', 'TAGC')
    0.75
    """
    if callable(method):
        return 1 - method(src, tar)
    else:
        raise AttributeError('Unknown distance function: ' + str(method))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
