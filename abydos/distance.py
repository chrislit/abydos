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
    - Smith-Waterman score
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

Functions beginning with the prefixes 'sim' and 'dist' are guaranteed to be
in the range [0, 1], and sim_X = 1 - dist_X since the two are complements.
If a sim_X function is supplied identical src & tar arguments, it is guaranteed
to return 1; the corresponding dist_X function is guaranteed to return 0.
"""

from __future__ import division, unicode_literals

from codecs import encode
from collections import Counter, Iterable, defaultdict
from math import log, sqrt
from numbers import Number
from sys import maxsize, modules
from types import GeneratorType
from unicodedata import normalize as unicode_normalize

from numpy import float32 as np_float32
from numpy import int as np_int
from numpy import zeros as np_zeros

from six import text_type
from six.moves import range

from .compression import ac_encode, ac_train, rle_encode
# noinspection PyProtectedMember
from .fingerprint import _synoname_special_table, synoname_toolcode
from .phonetic import eudex, mra
from .qgram import QGrams

try:
    import lzma
except ImportError:  # pragma: no cover
    # If the system lacks the lzma library, that's fine, but lzma compression
    # similarity won't be supported.
    lzma = None

__all__ = ['bag', 'chebyshev', 'damerau_levenshtein', 'dist', 'dist_bag',
           'dist_baystat', 'dist_compression', 'dist_cosine', 'dist_damerau',
           'dist_dice', 'dist_editex', 'dist_euclidean', 'dist_eudex',
           'dist_hamming', 'dist_ident', 'dist_indel', 'dist_jaccard',
           'dist_jaro_winkler', 'dist_lcsseq', 'dist_lcsstr', 'dist_length',
           'dist_levenshtein', 'dist_manhattan', 'dist_minkowski',
           'dist_mlipns', 'dist_monge_elkan', 'dist_mra',
           'dist_overlap', 'dist_prefix', 'dist_ratcliff_obershelp',
           'dist_sift4', 'dist_strcmp95', 'dist_suffix', 'dist_tversky',
           'dist_typo', 'editex', 'euclidean', 'eudex', 'eudex_hamming',
           'gotoh', 'hamming', 'lcsseq', 'lcsstr', 'levenshtein', 'manhattan',
           'minkowski', 'mra_compare', 'needleman_wunsch', 'sift4_common',
           'sift4_simplest', 'sim', 'sim_bag', 'sim_baystat',
           'sim_compression', 'sim_cosine', 'sim_damerau', 'sim_dice',
           'sim_editex', 'sim_euclidean', 'sim_eudex', 'sim_hamming',
           'sim_ident', 'sim_indel', 'sim_jaccard', 'sim_jaro_winkler',
           'sim_lcsseq', 'sim_lcsstr', 'sim_length', 'sim_levenshtein',
           'sim_manhattan', 'sim_matrix', 'sim_minkowski', 'sim_mlipns',
           'sim_monge_elkan', 'sim_mra', 'sim_overlap', 'sim_prefix',
           'sim_ratcliff_obershelp', 'sim_sift4', 'sim_strcmp95', 'sim_suffix',
           'sim_tanimoto', 'sim_tversky', 'sim_typo', 'smith_waterman',
           'synoname', '_synoname_word_approximation', 'tanimoto', 'typo']


def levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein distance between two strings.

    This is the standard edit distance measure. Cf.
    :cite:`Levenshtein:1965,Levenshtein:1966`.

    Two additional variants: optimal string alignment (aka restricted
    Damerau-Levenshtein distance) :cite:`Boytsov:2011` and the
    Damerau-Levenshtein :cite:`Damerau:1964` distance are also supported.

    The ordinary Levenshtein & Optimal String Alignment distance both
    employ the Wagner-Fischer dynamic programming algorithm
    :cite:`Wagner:1974`.

    Levenshtein edit distance ordinarily has unit insertion, deletion, and
    substitution costs.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    d_mat = np_zeros((len(src)+1, len(tar)+1), dtype=np_int)
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

    The Levenshtein distance is normalized by dividing the Levenshtein distance
    (calculated by any of the three supported methods) by the greater of
    the number of characters in src times the cost of a delete and
    the number of characters in tar times the cost of an insert.
    For the case in which all operations have :math:`cost = 1`, this is
    equivalent to the greater of the length of the two strings src & tar.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    >>> round(dist_levenshtein('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_levenshtein('Niall', 'Neil'), 12)
    0.6
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

    Normalized Levenshtein similarity is the complement of normalized
    Levenshtein distance:
    :math:`sim_{Levenshtein} = 1 - dist_{Levenshtein}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    >>> round(sim_levenshtein('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_levenshtein('Niall', 'Neil'), 12)
    0.4
    >>> sim_levenshtein('aluminum', 'Catalan')
    0.125
    >>> sim_levenshtein('ATCG', 'TAGC')
    0.25
    """
    return 1 - dist_levenshtein(src, tar, mode, cost)


def damerau_levenshtein(src, tar, cost=(1, 1, 1, 1)):
    """Return the Damerau-Levenshtein distance between two strings.

    This computes the Damerau-Levenshtein distance :cite:`Damerau:1964`.
    Damerau-Levenshtein code is based on Java code by Kevin L. Stern
    :cite:`Stern:2014`, under the MIT license:
    https://github.com/KevinStern/software-and-algorithms/blob/master/src/main/java/blogspot/software_and_algorithms/stern_library/string/DamerauLevenshteinAlgorithm.java

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    d_mat = (np_zeros((len(src))*(len(tar)), dtype=np_int).
             reshape((len(src), len(tar))))

    if src[0] != tar[0]:
        d_mat[0, 0] = min(sub_cost, ins_cost + del_cost)

    src_index_by_character = {src[0]: 0}
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
                swap_distance = maxsize

            d_mat[i, j] = min(del_distance, ins_distance,
                              match_distance, swap_distance)
        src_index_by_character[src[i]] = i

    return d_mat[len(src)-1, len(tar)-1]


def dist_damerau(src, tar, cost=(1, 1, 1, 1)):
    """Return the Damerau-Levenshtein similarity of two strings.

    Damerau-Levenshtein distance normalized to the interval [0, 1].

    The Damerau-Levenshtein distance is normalized by dividing the
    Damerau-Levenshtein distance by the greater of
    the number of characters in src times the cost of a delete and
    the number of characters in tar times the cost of an insert.
    For the case in which all operations have :math:`cost = 1`, this is
    equivalent to the greater of the length of the two strings src & tar.

    The arguments are identical to those of the levenshtein() function.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits:
        inserts, deletes, substitutions, and transpositions, respectively
        (by default: (1, 1, 1, 1))
    :returns: normalized Damerau-Levenshtein distance
    :rtype: float

    >>> round(dist_damerau('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_damerau('Niall', 'Neil'), 12)
    0.6
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

    Normalized Damerau-Levenshtein similarity the complement of normalized
    Damerau-Levenshtein distance:
    :math:`sim_{Damerau} = 1 - dist_{Damerau}`.

    The arguments are identical to those of the levenshtein() function.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits:
        inserts, deletes, substitutions, and transpositions, respectively
        (by default: (1, 1, 1, 1))
    :returns: normalized Damerau-Levenshtein similarity
    :rtype: float

    >>> round(sim_damerau('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_damerau('Niall', 'Neil'), 12)
    0.4
    >>> sim_damerau('aluminum', 'Catalan')
    0.125
    >>> sim_damerau('ATCG', 'TAGC')
    0.5
    """
    return 1 - dist_damerau(src, tar, cost)


def hamming(src, tar, diff_lens=True):
    """Return the Hamming distance between two strings.

    Hamming distance :cite:`Hamming:1950` equals the number of character
    positions at which two strings differ. For strings of unequal lengths,
    it is not normally defined. By default, this implementation calculates the
    Hamming distance of the first n characters where n is the lesser of the two
    strings' lengths and adds to this the difference in string lengths.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool diff_lens:
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
    if not diff_lens and len(src) != len(tar):
        raise ValueError('Undefined for sequences of unequal length; set ' +
                         'diff_lens to True for Hamming distance between ' +
                         'strings of unequal lengths.')

    hdist = 0
    if diff_lens:
        hdist += abs(len(src)-len(tar))
    hdist += sum(c1 != c2 for c1, c2 in zip(src, tar))

    return hdist


def dist_hamming(src, tar, diff_lens=True):
    """Return the normalized Hamming distance between two strings.

    Hamming distance normalized to the interval [0, 1].

    The Hamming distance is normalized by dividing it
    by the greater of the number of characters in src & tar (unless diff_lens
    is set to False, in which case an exception is raised).

    The arguments are identical to those of the hamming() function.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool diff_lens:
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending
        the shorter string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.
    :returns: normalized Hamming distance
    :rtype: float

    >>> round(dist_hamming('cat', 'hat'), 12)
    0.333333333333
    >>> dist_hamming('Niall', 'Neil')
    0.6
    >>> dist_hamming('aluminum', 'Catalan')
    1.0
    >>> dist_hamming('ATCG', 'TAGC')
    1.0
    """
    if src == tar:
        return 0
    return hamming(src, tar, diff_lens) / max(len(src), len(tar))


def sim_hamming(src, tar, diff_lens=True):
    """Return the normalized Hamming similarity of two strings.

    Hamming similarity normalized to the interval [0, 1].

    Hamming similarity is the complement of normalized Hamming distance:
    :math:`sim_{Hamming} = 1 - dist{Hamming}`.

    Provided that diff_lens==True, the Hamming similarity is identical to the
    Language-Independent Product Name Search (LIPNS) similarity score. For
    further information, see the sim_mlipns documentation.

    The arguments are identical to those of the hamming() function.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool diff_lens:
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending
        the shorter string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.
    :returns: normalized Hamming similarity
    :rtype: float

    >>> round(sim_hamming('cat', 'hat'), 12)
    0.666666666667
    >>> sim_hamming('Niall', 'Neil')
    0.4
    >>> sim_hamming('aluminum', 'Catalan')
    0.0
    >>> sim_hamming('ATCG', 'TAGC')
    0.0
    """
    return 1 - dist_hamming(src, tar, diff_lens)


def _get_qgrams(src, tar, qval=0, skip=0):
    """Return the Q-Grams in src & tar.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param int skip: the number of characters to skip (only works when
        src and tar are strings
    :returns: Q-Grams
    :rtype: tuple of Counters

    >>> _get_qgrams('AT', 'TT', qval=2)
    (QGrams({'$A': 1, 'AT': 1, 'T#': 1}), QGrams({'$T': 1, 'TT': 1, 'T#': 1}))
    """
    if isinstance(src, Counter) and isinstance(tar, Counter):
        return src, tar
    if qval > 0:
        return (QGrams(src, qval, '$#', skip),
                QGrams(tar, qval, '$#', skip))
    return Counter(src.strip().split()), Counter(tar.strip().split())


def sim_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    r"""Return the Tversky index of two strings.

    The Tversky index :cite:`Tversky:1977` is defined as:
    For two sets X and Y:
    :math:`sim_{Tversky}(X, Y) = \\frac{|X \\cap Y|}
    {|X \\cap Y| + \\alpha|X - Y| + \\beta|Y - X|}`.

    :math:`\\alpha = \\beta = 1` is equivalent to the Jaccard & Tanimoto
    similarity coefficients.

    :math:`\\alpha = \\beta = 0.5` is equivalent to the Sørensen-Dice
    similarity coefficient :cite:`Dice:1945,Sorensen:1948`.

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

    The symmetric variant is defined in :cite:`Jiminez:2013`. This is activated
    by specifying a bias parameter.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param float alpha: Tversky index parameter as described above
    :param float beta: Tversky index parameter as described above
    :param float bias: The symmetric Tversky index bias parameter
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
    """Return the Tversky distance between two strings.

    Tversky distance is the complement of the Tvesrsky index (similarity):
    :math:`dist_{Tversky} = 1-sim_{Tversky}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram
        version
    :param float alpha: the Tversky index's alpha parameter
    :param float beta: the Tversky index's beta parameter
    :param float bias: The symmetric Tversky index bias parameter
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

    For two sets X and Y, the Sørensen–Dice coefficient
    :cite:`Dice:1945,Sorensen:1948` is
    :math:`sim_{dice}(X, Y) = \\frac{2 \\cdot |X \\cap Y|}{|X| + |Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958` and the Tversky index :cite:`Tversky:1977` for
    :math:`\\alpha = \\beta = 0.5`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram
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

    Sørensen–Dice distance is the complemenjt of the Sørensen–Dice coefficient:
    :math:`dist_{dice} = 1 - sim_{dice}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram
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

    For two sets X and Y, the Jaccard similarity coefficient
    :cite:`Jaccard:1901` is :math:`sim_{jaccard}(X, Y) =
    \\frac{|X \\cap Y|}{|X \\cup Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958`
    and the Tversky index :cite:`Tversky:1977` for
    :math:`\\alpha = \\beta = 1`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram
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

    Jaccard distance is the complement of the Jaccard similarity coefficient:
    :math:`dist_{Jaccard} = 1 - sim_{Jaccard}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
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

    For two sets X and Y, the overlap coefficient
    :cite:`Szymkiewicz:1934,Simpson:1949`, also called the
    Szymkiewicz-Simpson coefficient, is
    :math:`sim_{overlap}(X, Y) = \\frac{|X \\cap Y|}{min(|X|, |Y|)}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
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

    Overlap distance is the complement of the overlap coefficient:
    :math:`sim_{overlap} = 1 - dist_{overlap}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
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

    For two sets X and Y, the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958` is
    :math:`sim_{Tanimoto}(X, Y) = \\frac{|X \\cap Y|}{|X \\cup Y|}`.

    This is identical to the Jaccard similarity coefficient
    :cite:`Jaccard:1901` and the Tversky index :cite:`Tversky:1977` for
    :math:`\\alpha = \\beta = 1`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
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

    Tanimoto distance is :math:`-log_{2}sim_{Tanimoto}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
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
        return log(coeff, 2)

    return float('-inf')


def minkowski(src, tar, qval=2, pval=1, normalized=False, alphabet=None):
    """Return the Minkowski distance (:math:`L^p-norm`) of two strings.

    The Minkowski distance :cite:`Minkowski:1910` is a distance metric in
    :math:`L^p-space`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param int or float pval: the :math:`p`-value of the :math:`L^p`-space.
    :param bool normalized: normalizes to [0, 1] if True
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the Minkowski distance
    :rtype: float

    >>> minkowski('cat', 'hat')
    4.0
    >>> minkowski('Niall', 'Neil')
    7.0
    >>> minkowski('Colin', 'Cuilen')
    9.0
    >>> minkowski('ATCG', 'TAGC')
    10.0
    """
    q_src, q_tar = _get_qgrams(src, tar, qval)
    diffs = ((q_src - q_tar) + (q_tar - q_src)).values()

    normalizer = 1
    if normalized:
        totals = (q_src + q_tar).values()
        if alphabet is not None:
            # noinspection PyTypeChecker
            normalizer = (alphabet if isinstance(alphabet, Number) else
                          len(alphabet))
        elif pval == 0:
            normalizer = len(totals)
        else:
            normalizer = sum(_**pval for _ in totals)**(1 / pval)

    if len(diffs) == 0:
        return 0.0
    if pval == float('inf'):
        # Chebyshev distance
        return max(diffs)/normalizer
    if pval == 0:
        # This is the l_0 "norm" as developed by David Donoho
        return len(diffs)/normalizer
    return sum(_**pval for _ in diffs)**(1 / pval)/normalizer


def dist_minkowski(src, tar, qval=2, pval=1, alphabet=None):
    """Return normalized Minkowski distance of two strings.

    The normalized Minkowski distance :cite:`Minkowski:1910` is a distance
    metric in :math:`L^p-space`, normalized to [0, 1].

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param int or float pval: the :math:`p`-value of the :math:`L^p`-space.
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Minkowski distance
    :rtype: float

    >>> dist_minkowski('cat', 'hat')
    0.5
    >>> round(dist_minkowski('Niall', 'Neil'), 12)
    0.636363636364
    >>> round(dist_minkowski('Colin', 'Cuilen'), 12)
    0.692307692308
    >>> dist_minkowski('ATCG', 'TAGC')
    1.0
    """
    return minkowski(src, tar, qval, pval, True, alphabet)


def sim_minkowski(src, tar, qval=2, pval=1, alphabet=None):
    """Return normalized Minkowski similarity of two strings.

    Minkowski similarity is the complement of Minkowski distance:
    :math:`sim_{Minkowski} = 1 - dist_{Minkowski}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param int or float pval: the :math:`p`-value of the :math:`L^p`-space.
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Minkowski similarity
    :rtype: float

    >>> sim_minkowski('cat', 'hat')
    0.5
    >>> round(sim_minkowski('Niall', 'Neil'), 12)
    0.363636363636
    >>> round(sim_minkowski('Colin', 'Cuilen'), 12)
    0.307692307692
    >>> sim_minkowski('ATCG', 'TAGC')
    0.0
    """
    return 1-minkowski(src, tar, qval, pval, True, alphabet)


def manhattan(src, tar, qval=2, normalized=False, alphabet=None):
    """Return the Manhattan distance between two strings.

    Manhattan distance is the city-block or taxi-cab distance, equivalent
    to Minkowski distance in :math:`L^1`-space.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param normalized: normalizes to [0, 1] if True
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the Manhattan distance
    :rtype: float

    >>> manhattan('cat', 'hat')
    4.0
    >>> manhattan('Niall', 'Neil')
    7.0
    >>> manhattan('Colin', 'Cuilen')
    9.0
    >>> manhattan('ATCG', 'TAGC')
    10.0
    """
    return minkowski(src, tar, qval, 1, normalized, alphabet)


def dist_manhattan(src, tar, qval=2, alphabet=None):
    """Return the normalized Manhattan distance between two strings.

    The normalized Manhattan distance is a distance
    metric in :math:`L^1-space`, normalized to [0, 1].

    This is identical to Canberra distance.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Manhattan distance
    :rtype: float

    >>> dist_manhattan('cat', 'hat')
    0.5
    >>> round(dist_manhattan('Niall', 'Neil'), 12)
    0.636363636364
    >>> round(dist_manhattan('Colin', 'Cuilen'), 12)
    0.692307692308
    >>> dist_manhattan('ATCG', 'TAGC')
    1.0
    """
    return manhattan(src, tar, qval, True, alphabet)


def sim_manhattan(src, tar, qval=2, alphabet=None):
    """Return the normalized Manhattan similarity of two strings.

    Manhattan similarity is the complement of Manhattan distance:
    :math:`sim_{Manhattan} = 1 - dist_{Manhattan}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Manhattan similarity
    :rtype: float

    >>> sim_manhattan('cat', 'hat')
    0.5
    >>> round(sim_manhattan('Niall', 'Neil'), 12)
    0.363636363636
    >>> round(sim_manhattan('Colin', 'Cuilen'), 12)
    0.307692307692
    >>> sim_manhattan('ATCG', 'TAGC')
    0.0
    """
    return 1-manhattan(src, tar, qval, True, alphabet)


def euclidean(src, tar, qval=2, normalized=False, alphabet=None):
    """Return the Euclidean distance between two strings.

    Euclidean distance is the straigh-line or as-the-crow-flies distance,
    equivalent to Minkowski distance in :math:`L^2`-space.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param normalized: normalizes to [0, 1] if True
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the Euclidean distance
    :rtype: float

    >>> euclidean('cat', 'hat')
    2.0
    >>> round(euclidean('Niall', 'Neil'), 12)
    2.645751311065
    >>> euclidean('Colin', 'Cuilen')
    3.0
    >>> round(euclidean('ATCG', 'TAGC'), 12)
    3.162277660168
    """
    return minkowski(src, tar, qval, 2, normalized, alphabet)


def dist_euclidean(src, tar, qval=2, alphabet=None):
    """Return the normalized Euclidean distance between two strings.

    The normalized Euclidean distance is a distance
    metric in :math:`L^2-space`, normalized to [0, 1].

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Euclidean distance
    :rtype: float

    >>> round(dist_euclidean('cat', 'hat'), 12)
    0.57735026919
    >>> round(dist_euclidean('Niall', 'Neil'), 12)
    0.683130051064
    >>> round(dist_euclidean('Colin', 'Cuilen'), 12)
    0.727606875109
    >>> dist_euclidean('ATCG', 'TAGC')
    1.0
    """
    return euclidean(src, tar, qval, True, alphabet)


def sim_euclidean(src, tar, qval=2, alphabet=None):
    """Return the normalized Euclidean similarity of two strings.

    Euclidean similarity is the complement of Euclidean distance:
    :math:`sim_{Euclidean} = 1 - dist_{Euclidean}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Euclidean similarity
    :rtype: float

    >>> round(sim_euclidean('cat', 'hat'), 12)
    0.42264973081
    >>> round(sim_euclidean('Niall', 'Neil'), 12)
    0.316869948936
    >>> round(sim_euclidean('Colin', 'Cuilen'), 12)
    0.272393124891
    >>> sim_euclidean('ATCG', 'TAGC')
    0.0
    """
    return 1-euclidean(src, tar, qval, True, alphabet)


def chebyshev(src, tar, qval=2, normalized=False, alphabet=None):
    r"""Return the Chebyshev distance between two strings.

    Euclidean distance is the chessboard distance,
    equivalent to Minkowski distance in :math:`L^\infty-space`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param normalized: normalizes to [0, 1] if True
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the Chebyshev distance
    :rtype: float

    >>> chebyshev('cat', 'hat')
    1.0
    >>> chebyshev('Niall', 'Neil')
    1.0
    >>> chebyshev('Colin', 'Cuilen')
    1.0
    >>> chebyshev('ATCG', 'TAGC')
    1.0
    >>> chebyshev('ATCG', 'TAGC', qval=1)
    0.0
    >>> chebyshev('ATCGATTCGGAATTTC', 'TAGCATAATCGCCG', qval=1)
    3.0
    """
    return minkowski(src, tar, qval, float('inf'), normalized, alphabet)


def sim_cosine(src, tar, qval=2):
    r"""Return the cosine similarity of two strings.

    For two sets X and Y, the cosine similarity, Otsuka-Ochiai coefficient, or
    Ochiai coefficient :cite:`Otsuka:1936,Ochiai:1957` is:
    :math:`sim_{cosine}(X, Y) = \\frac{|X \\cap Y|}{\\sqrt{|X| \\cdot |Y|}}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
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

    return q_intersection_mag / sqrt(q_src_mag * q_tar_mag)


def dist_cosine(src, tar, qval=2):
    """Return the cosine distance between two strings.

    Cosine distance is the complement of cosine similarity:
    :math:`dist_{cosine} = 1 - sim_{cosine}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
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

    This is a Python translation of the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    :cite:`Winkler:1994`.
    The above file is a US Government publication and, accordingly,
    in the public domain.

    This is based on the Jaro-Winkler distance, but also attempts to correct
    for some common typos and frequently confused characters. It is also
    limited to uppercase ASCII characters, so it is appropriate to American
    names, but not much else.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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
    def _in_range(char):
        """Return True if char is in the range (0, 91)."""
        return 91 > ord(char) > 0

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
        low_lim = (i - search_range) if (i >= search_range) else 0
        hi_lim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in range(low_lim, hi_lim+1):
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
            j = 0
            for j in range(k, len(yang)):  # pragma: no branch
                if yang_flag[j] != 0:
                    k = j + 1
                    break
            if ying[i] != yang[j]:
                n_trans += 1
    n_trans //= 2

    # Adjust for similarities in unmatched characters
    n_simi = 0
    if minv > num_com:
        for i in range(len(ying)):
            if ying_flag[i] == 0 and _in_range(ying[i]):
                for j in range(len(yang)):
                    if yang_flag[j] == 0 and _in_range(yang[j]):
                        if (ying[i], yang[j]) in adjwt:
                            n_simi += adjwt[(ying[i], yang[j])]
                            yang_flag[j] = 2
                            break
    num_sim = n_simi/10.0 + num_com

    # Main weight computation
    weight = num_sim / len(ying) + num_sim / len(yang) + \
        (num_com - n_trans) / num_com
    weight /= 3.0

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
        if (long_strings and (minv > 4) and (num_com > i+1) and
                (2*num_com >= minv+i)):
            if not ying[0].isdigit():
                weight += (1.0-weight) * ((num_com-i-1) /
                                          (len(ying)+len(yang)-i*2+2))

    return weight


def dist_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 distance between two strings.

    strcmp95 distance is the complement of strcmp95 similarity:
    :math:`dist_{strcmp95} = 1 - sim_{strcmp95}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large. It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :returns: strcmp95 distance
    :rtype: float

    >>> round(dist_strcmp95('cat', 'hat'), 12)
    0.222222222222
    >>> round(dist_strcmp95('Niall', 'Neil'), 12)
    0.1545
    >>> round(dist_strcmp95('aluminum', 'Catalan'), 12)
    0.345238095238
    >>> round(dist_strcmp95('ATCG', 'TAGC'), 12)
    0.166666666667
    """
    return 1 - sim_strcmp95(src, tar, long_strings)


def sim_jaro_winkler(src, tar, qval=1, mode='winkler', long_strings=False,
                     boost_threshold=0.7, scaling_factor=0.1):
    """Return the Jaro or Jaro-Winkler similarity of two strings.

    Jaro(-Winkler) distance is a string edit distance initially proposed by
    Jaro and extended by Winkler :cite:`Jaro:1989,Winkler:1990`.

    This is Python based on the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    :cite:`Winkler:1994`. The above file is a US Government publication and,
    accordingly, in the public domain.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    >>> round(sim_jaro_winkler('cat', 'hat'), 12)
    0.777777777778
    >>> round(sim_jaro_winkler('Niall', 'Neil'), 12)
    0.805
    >>> round(sim_jaro_winkler('aluminum', 'Catalan'), 12)
    0.60119047619
    >>> round(sim_jaro_winkler('ATCG', 'TAGC'), 12)
    0.833333333333

    >>> round(sim_jaro_winkler('cat', 'hat', mode='jaro'), 12)
    0.777777777778
    >>> round(sim_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
    0.783333333333
    >>> round(sim_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
    0.60119047619
    >>> round(sim_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
    0.833333333333
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
        low_lim = (i - search_range) if (i >= search_range) else 0
        hi_lim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in range(low_lim, hi_lim+1):
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
            j = 0
            for j in range(k, lent):  # pragma: no branch
                if tar_flag[j] != 0:
                    k = j + 1
                    break
            if src[i] != tar[j]:
                n_trans += 1
    n_trans //= 2

    # Main weight computation for Jaro distance
    weight = num_com / lens + num_com / lent + (num_com - n_trans) / num_com
    weight /= 3.0

    # Continue to boost the weight if the strings are similar
    # This is the Winkler portion of Jaro-Winkler distance
    if mode == 'winkler' and weight > boost_threshold:

        # Adjust for having up to the first 4 characters in common
        j = 4 if (minv >= 4) else minv
        i = 0
        while (i < j) and (src[i] == tar[i]):
            i += 1
        weight += i * scaling_factor * (1.0 - weight)

        # Optionally adjust for long strings.

        # After agreeing beginning chars, at least two more must agree and
        # the agreeing characters must be > .5 of remaining characters.
        if (long_strings and (minv > 4) and (num_com > i+1) and
                (2*num_com >= minv+i)):
            weight += (1.0-weight) * ((num_com-i-1) / (lens+lent-i*2+2))

    return weight


def dist_jaro_winkler(src, tar, qval=1, mode='winkler', long_strings=False,
                      boost_threshold=0.7, scaling_factor=0.1):
    """Return the Jaro or Jaro-Winkler distance between two strings.

    Jaro(-Winkler) similarity is the complement of Jaro(-Winkler) distance:
    :math:`sim_{Jaro(-Winkler)} = 1 - dist_{Jaro(-Winkler)}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    >>> round(dist_jaro_winkler('cat', 'hat'), 12)
    0.222222222222
    >>> round(dist_jaro_winkler('Niall', 'Neil'), 12)
    0.195
    >>> round(dist_jaro_winkler('aluminum', 'Catalan'), 12)
    0.39880952381
    >>> round(dist_jaro_winkler('ATCG', 'TAGC'), 12)
    0.166666666667

    >>> round(dist_jaro_winkler('cat', 'hat', mode='jaro'), 12)
    0.222222222222
    >>> round(dist_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
    0.216666666667
    >>> round(dist_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
    0.39880952381
    >>> round(dist_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
    0.166666666667
    """
    return 1 - sim_jaro_winkler(src, tar, qval, mode, long_strings,
                                boost_threshold, scaling_factor)


def lcsseq(src, tar):
    """Return the longest common subsequence of two strings.

    Longest common subsequence (LCSseq) is the longest subsequence of
    characters that two strings have in common.

    Based on the dynamic programming algorithm from
    http://rosettacode.org/wiki/Longest_common_subsequence#Dynamic_Programming_6
    :cite:`rosettacode:2018b`. This is licensed GFDL 1.2.

    Modifications include:
        conversion to a numpy array in place of a list of lists

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: the longest common subsequence
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
    lengths = np_zeros((len(src)+1, len(tar)+1), dtype=np_int)

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

    Longest common subsequence similarity (:math:`sim_{LCSseq}`).

    This employs the LCSseq function to derive a similarity metric:
    :math:`sim_{LCSseq}(s,t) = \\frac{|LCSseq(s,t)|}{max(|s|, |t|)}`

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Longest common subsequence distance (:math:`dist_{LCSseq}`).

    This employs the LCSseq function to derive a similarity metric:
    :math:`dist_{LCSseq}(s,t) = 1 - sim_{LCSseq}(s,t)`

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Longest common substring (LCSstr).

    Based on the code from
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python
    :cite:`Wikibooks:2018`.
    This is licensed Creative Commons: Attribution-ShareAlike 3.0.

    Modifications include:

        - conversion to a numpy array in place of a list of lists
        - conversion to Python 2/3-safe range from xrange via six

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: the longest common substring
    :rtype: str

    >>> lcsstr('cat', 'hat')
    'at'
    >>> lcsstr('Niall', 'Neil')
    'N'
    >>> lcsstr('aluminum', 'Catalan')
    'al'
    >>> lcsstr('ATCG', 'TAGC')
    'A'
    """
    lengths = np_zeros((len(src)+1, len(tar)+1), dtype=np_int)
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

    Longest common substring similarity (:math:`sim_{LCSstr}`).

    This employs the LCS function to derive a similarity metric:
    :math:`sim_{LCSstr}(s,t) = \\frac{|LCSstr(s,t)|}{max(|s|, |t|)}`

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Longest common substring distance (:math:`dist_{LCSstr}`).

    This employs the LCS function to derive a similarity metric:
    :math:`dist_{LCSstr}(s,t) = 1 - sim_{LCSstr}(s,t)`

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    This follows the Ratcliff-Obershelp algorithm :cite:`Ratcliff:1988` to
    derive a similarity measure:

        1. Find the length of the longest common substring in src & tar.
        2. Recurse on the strings to the left & right of each this substring
           in src & tar. The base case is a 0 length common substring, in which
           case, return 0. Otherwise, return the sum of the current longest
           common substring and the left & right recursed sums.
        3. Multiply this length by 2 and divide by the sum of the lengths of
           src & tar.

    Cf.
    http://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: Ratcliff-Obershelp similarity
    :rtype: float

    >>> round(sim_ratcliff_obershelp('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_ratcliff_obershelp('Niall', 'Neil'), 12)
    0.666666666667
    >>> round(sim_ratcliff_obershelp('aluminum', 'Catalan'), 12)
    0.4
    >>> sim_ratcliff_obershelp('ATCG', 'TAGC')
    0.5
    """
    def _lcsstr_stl(src, tar):
        """Return start positions & length for Ratcliff-Obershelp.

        Return the start position in the source string, start position in
        the target string, and length of the longest common substring of
        strings src and tar.
        """
        lengths = np_zeros((len(src)+1, len(tar)+1), dtype=np_int)
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
        return src_longest-longest, tar_longest-longest, longest

    def _sstr_matches(src, tar):
        """Return the sum of substring match lengths.

        This follows the Ratcliff-Obershelp algorithm :cite:`Ratcliff:1988`:
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
                _sstr_matches(src[src_start+length:],
                              tar[tar_start+length:]))

    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0
    return 2*_sstr_matches(src, tar)/(len(src)+len(tar))


def dist_ratcliff_obershelp(src, tar):
    """Return the Ratcliff-Obershelp distance between two strings.

    Ratcliff-Obsershelp distance the complement of Ratcliff-Obershelp
    similarity:
    :math:`dist_{Ratcliff-Obershelp} = 1 - sim_{Ratcliff-Obershelp}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: Ratcliff-Obershelp distance
    :rtype: float

    >>> round(dist_ratcliff_obershelp('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_ratcliff_obershelp('Niall', 'Neil'), 12)
    0.333333333333
    >>> round(dist_ratcliff_obershelp('aluminum', 'Catalan'), 12)
    0.6
    >>> dist_ratcliff_obershelp('ATCG', 'TAGC')
    0.5
    """
    return 1 - sim_ratcliff_obershelp(src, tar)


def mra_compare(src, tar):
    """Return the MRA comparison rating of two strings.

    The Western Airlines Surname Match Rating Algorithm comparison rating, as
    presented on page 18 of :cite:`Moore:1977`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    This is the MRA normalized to :math:`[0, 1]`, given that MRA itself is
    constrained to the range :math:`[0, 6]`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    MRA distance is the complement of MRA similarity:
    :math:`dist_{MRA} = 1 - sim_{MRA}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str compressor: a compression scheme to use for the similarity
        calculation, from the following:

            - `zlib` -- standard zlib/gzip
            - `bz2` -- bzip2 (default)
            - `lzma` -- Lempel–Ziv–Markov chain algorithm
            - `arith` -- arithmetic coding
            - `rle` -- run-length encoding
            - `bwtrle` -- Burrows-Wheeler transform followed by run-length
              encoding

    :param dict probs: a dictionary trained with ac_train (for the arith
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
        src_comp = encode(src, 'bz2_codec')[15:]
        tar_comp = encode(tar, 'bz2_codec')[15:]
        concat_comp = encode(src+tar, 'bz2_codec')[15:]
        concat_comp2 = encode(tar+src, 'bz2_codec')[15:]
    elif compressor == 'lzma':
        if 'lzma' in modules:
            src_comp = lzma.compress(src)[14:]
            tar_comp = lzma.compress(tar)[14:]
            concat_comp = lzma.compress(src+tar)[14:]
            concat_comp2 = lzma.compress(tar+src)[14:]
        else:
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
        src_comp = encode(src, 'zlib_codec')[2:]
        tar_comp = encode(tar, 'zlib_codec')[2:]
        concat_comp = encode(src+tar, 'zlib_codec')[2:]
        concat_comp2 = encode(tar+src, 'zlib_codec')[2:]
    return ((min(len(concat_comp), len(concat_comp2)) -
             min(len(src_comp), len(tar_comp))) /
            max(len(src_comp), len(tar_comp)))


def sim_compression(src, tar, compressor='bz2', probs=None):
    """Return the normalized compression similarity of two strings.

    Normalized compression similarity is the complement of normalized
    compression distance:
    :math:`sim_{NCS} = 1 - dist_{NCD}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Monge-Elkan is defined in :cite:`Monge:1996`.

    Note: Monge-Elkan is NOT a symmetric similarity algoritm. Thus, the
    similarity of src to tar is not necessarily equal to the similarity of
    tar to src. If the sym argument is True, a symmetric value is calculated,
    at the cost of doubling the computation time (since the
    :math:`sim_{Monge-Elkan}(src, tar)` and
    :math:`sim_{Monge-Elkan}(tar, src)` are both calculated and then averaged).

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param function sim_func: the internal similarity metric to employ
    :param bool symmetric: return a symmetric similarity measure
    :returns: Monge-Elkan similarity
    :rtype: float

    >>> sim_monge_elkan('cat', 'hat')
    0.75
    >>> round(sim_monge_elkan('Niall', 'Neil'), 12)
    0.666666666667
    >>> round(sim_monge_elkan('aluminum', 'Catalan'), 12)
    0.388888888889
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

    Monge-Elkan distance is the complement of Monge-Elkan similarity:
    :math:`dist_{Monge-Elkan} = 1 - sim_{Monge-Elkan}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param function sim_func: the internal similarity metric to employ
    :param bool symmetric: return a symmetric similarity measure
    :returns: Monge-Elkan distance
    :rtype: float

    >>> dist_monge_elkan('cat', 'hat')
    0.25
    >>> round(dist_monge_elkan('Niall', 'Neil'), 12)
    0.333333333333
    >>> round(dist_monge_elkan('aluminum', 'Catalan'), 12)
    0.611111111111
    >>> dist_monge_elkan('ATCG', 'TAGC')
    0.5
    """
    return 1 - sim_monge_elkan(src, tar, sim_func, symmetric)


def sim_ident(src, tar):
    """Return the identity similarity of two strings.

    Identity similarity is 1 if the two strings are identical, otherwise 0.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    This is 0 if the two strings are identical, otherwise 1, i.e.
    :math:`dist_{identity} = 1 - sim_{identity}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: identity distance
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

    With the default parameters, this is identical to sim_ident.
    It is possible for sim_matrix to return values outside of the range
    :math:`[0, 1]`, if values outside that range are present in mat,
    mismatch_cost, or match_cost.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    The Needleman-Wunsch score :cite:`Needleman:1970` is a standard edit
    distance measure.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param float gap_cost: the cost of an alignment gap (1 by default)
    :param function sim_func: a function that returns the similarity of two
        characters (identity similarity by default)
    :returns: Needleman-Wunsch score
    :rtype: float

    >>> needleman_wunsch('cat', 'hat')
    2.0
    >>> needleman_wunsch('Niall', 'Neil')
    1.0
    >>> needleman_wunsch('aluminum', 'Catalan')
    -1.0
    >>> needleman_wunsch('ATCG', 'TAGC')
    0.0
    """
    d_mat = np_zeros((len(src)+1, len(tar)+1), dtype=np_float32)

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

    The Smith-Waterman score :cite:`Smith:1981` is a standard edit distance
    measure, differing from Needleman-Wunsch in that it focuses on local
    alignment and disallows negative scores.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param float gap_cost: the cost of an alignment gap (1 by default)
    :param function sim_func: a function that returns the similarity of two
        characters (identity similarity by default)
    :returns: Smith-Waterman score
    :rtype: float

    >>> smith_waterman('cat', 'hat')
    2.0
    >>> smith_waterman('Niall', 'Neil')
    1.0
    >>> smith_waterman('aluminum', 'Catalan')
    0.0
    >>> smith_waterman('ATCG', 'TAGC')
    1.0
    """
    d_mat = np_zeros((len(src)+1, len(tar)+1), dtype=np_float32)

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

    The Gotoh score :cite:`Gotoh:1982` is essentially Needleman-Wunsch with
    affine gap penalties.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param float gap_open: the cost of an open alignment gap (1 by default)
    :param float gap_ext: the cost of an alignment gap extension (0.4 by
        default)
    :param function sim_func: a function that returns the similarity of two
        characters (identity similarity by default)
    :returns: Gotoh score
    :rtype: float

    >>> gotoh('cat', 'hat')
    2.0
    >>> gotoh('Niall', 'Neil')
    1.0
    >>> round(gotoh('aluminum', 'Catalan'), 12)
    -0.4
    >>> gotoh('cat', 'hat')
    2.0
    """
    d_mat = np_zeros((len(src)+1, len(tar)+1), dtype=np_float32)
    p_mat = np_zeros((len(src)+1, len(tar)+1), dtype=np_float32)
    q_mat = np_zeros((len(src)+1, len(tar)+1), dtype=np_float32)

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
    """Return the length similarity of two strings.

    Length similarity is the ratio of the length of the shorter string to the
    longer.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Length distance is the complement of length similarity:
    :math:`dist_{length} = 1 - sim_{length}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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
    """Return the prefix similarity of two strings.

    Prefix similarity is the ratio of the length of the shorter term that
    exactly matches the longer term to the length of the shorter term,
    beginning at the start of both terms.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Prefix distance is the complement of prefix similarity:
    :math:`dist_{prefix} = 1 - sim_{prefix}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Suffix similarity is the ratio of the length of the shorter term that
    exactly matches the longer term to the length of the shorter term,
    beginning at the end of both terms.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Suffix distance is the complement of suffix similarity:
    :math:`dist_{suffix} = 1 - sim_{suffix}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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


def sim_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS similarity of two strings.

    Modified Language-Independent Product Name Search (MLIPNS) is described in
    :cite:`Shannaq:2010`. This function returns only 1.0 (similar) or 0.0
    (not similar). LIPNS similarity is identical to normalized Hamming
    similarity.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param float threshold: a number [0, 1] indicating the maximum similarity
        score, below which the strings are considered 'similar' (0.25 by
        default)
    :param int max_mismatches: a number indicating the allowable number of
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
    ham = hamming(src, tar, diff_lens=True)
    max_length = max(len(src), len(tar))
    while src and tar and mismatches <= max_mismatches:
        if max_length < 1 or (1-(max_length-ham)/max_length) <= threshold:
            return 1.0
        else:
            mismatches += 1
            ham -= 1
            max_length -= 1

    if max_length < 1:
        return 1.0
    return 0.0


def dist_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS distance between two strings.

    MLIPNS distance is the complement of MLIPNS similarity:
    :math:`dist_{MLIPNS} = 1 - sim_{MLIPNS}`. This function returns only 0.0
    (distant) or 1.0 (not distant).

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param float threshold: a number [0, 1] indicating the maximum similarity
        score, below which the strings are considered 'similar' (0.25 by
        default)
    :param int max_mismatches: a number indicating the allowable number of
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
    return 1.0 - sim_mlipns(src, tar, threshold, max_mismatches)


def bag(src, tar):
    """Return the bag distance between two strings.

    Bag distance is proposed in :cite:`Bartolini:2002`. It is defined as:
    :math:`max(|multiset(src)-multiset(tar)|, |multiset(tar)-multiset(src)|)`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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

    Bag distance is normalized by dividing by :math:`max( |src|, |tar| )`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: normalized bag distance
    :rtype: float

    >>> dist_bag('cat', 'hat')
    0.3333333333333333
    >>> dist_bag('Niall', 'Neil')
    0.4
    >>> dist_bag('aluminum', 'Catalan')
    0.625
    >>> dist_bag('ATCG', 'TAGC')
    0.0
    """
    if tar == src:
        return 0.0
    if not src or not tar:
        return 1.0

    max_length = max(len(src), len(tar))

    return bag(src, tar)/max_length


def sim_bag(src, tar):
    """Return the normalized bag similarity of two strings.

    Normalized bag similarity is the complement of normalized bag distance:
    :math:`sim_{bag} = 1 - dist_{bag}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: normalized bag similarity
    :rtype: float

    >>> round(sim_bag('cat', 'hat'), 12)
    0.666666666667
    >>> sim_bag('Niall', 'Neil')
    0.6
    >>> sim_bag('aluminum', 'Catalan')
    0.375
    >>> sim_bag('ATCG', 'TAGC')
    1.0
    """
    return 1-dist_bag(src, tar)


def editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the Editex distance between two strings.

    As described on pages 3 & 4 of :cite:`Zobel:1996`.

    The local variant is based on :cite:`Ring:2009`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
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
    src = unicode_normalize('NFKD', text_type(src.upper()))
    tar = unicode_normalize('NFKD', text_type(tar.upper()))
    # convert ß to SS (for Python2)
    src = src.replace('ß', 'SS')
    tar = tar.replace('ß', 'SS')

    if src == tar:
        return 0
    if not src:
        return len(tar) * mismatch_cost
    if not tar:
        return len(src) * mismatch_cost

    d_mat = np_zeros((len(src)+1, len(tar)+1), dtype=np_int)
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

    The Editex distance is normalized by dividing the Editex distance
    (calculated by any of the three supported methods) by the greater of
    the number of characters in src times the cost of a delete and
    the number of characters in tar times the cost of an insert.
    For the case in which all operations have :math:`cost = 1`, this is
    equivalent to the greater of the length of the two strings src & tar.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param tuple cost: a 3-tuple representing the cost of the four possible
        edits:
        match, same-group, and mismatch respectively (by default: (0, 1, 2))
    :param bool local: if True, the local variant of Editex is used
    :returns: normalized Editex distance
    :rtype: float

    >>> round(dist_editex('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_editex('Niall', 'Neil'), 12)
    0.2
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

    The Editex similarity is the complement of Editex distance:
    :math:`sim_{Editex} = 1 - dist_{Editex}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param tuple cost: a 3-tuple representing the cost of the four possible
        edits:
        match, same-group, and mismatch respectively (by default: (0, 1, 2))
    :param bool local: if True, the local variant of Editex is used
    :returns: normalized Editex similarity
    :rtype: float

    >>> round(sim_editex('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_editex('Niall', 'Neil'), 12)
    0.8
    >>> sim_editex('aluminum', 'Catalan')
    0.25
    >>> sim_editex('ATCG', 'TAGC')
    0.25
    """
    return 1 - dist_editex(src, tar, cost, local)


def eudex_hamming(src, tar, weights='exponential', max_length=8,
                  normalized=False):
    """Calculate the Hamming distance between the Eudex hashes of two terms.

    Cf. :cite:`Ticki:2016`.

    - If weights is set to None, a simple Hamming distance is calculated.
    - If weights is set to 'exponential', weight decays by powers of 2, as
      proposed in the eudex specification: https://github.com/ticki/eudex.
    - If weights is set to 'fibonacci', weight decays through the Fibonacci
      series, as in the eudex reference implementation.
    - If weights is set to a callable function, this assumes it creates a
      generator and the generator is used to populate a series of weights.
    - If weights is set to an iterable, the iterable's values should be
      integers and will be used as the weights.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str, iterable, or generator function weights: the weights or weights
        generator function
    :param max_length: the number of characters to encode as a eudex hash
    :param bool normalized: normalizes to [0, 1] if True
    :returns: the Eudex Hamming distance
    :rtype: int

    >>> eudex_hamming('cat', 'hat')
    128
    >>> eudex_hamming('Niall', 'Neil')
    2
    >>> eudex_hamming('Colin', 'Cuilen')
    10
    >>> eudex_hamming('ATCG', 'TAGC')
    403

    >>> eudex_hamming('cat', 'hat', weights='fibonacci')
    34
    >>> eudex_hamming('Niall', 'Neil', weights='fibonacci')
    2
    >>> eudex_hamming('Colin', 'Cuilen', weights='fibonacci')
    7
    >>> eudex_hamming('ATCG', 'TAGC', weights='fibonacci')
    117

    >>> eudex_hamming('cat', 'hat', weights=None)
    1
    >>> eudex_hamming('Niall', 'Neil', weights=None)
    1
    >>> eudex_hamming('Colin', 'Cuilen', weights=None)
    2
    >>> eudex_hamming('ATCG', 'TAGC', weights=None)
    9

    >>> # Using the OEIS A000142:
    >>> eudex_hamming('cat', 'hat', [1, 1, 2, 6, 24, 120, 720, 5040])
    1
    >>> eudex_hamming('Niall', 'Neil', [1, 1, 2, 6, 24, 120, 720, 5040])
    720
    >>> eudex_hamming('Colin', 'Cuilen', [1, 1, 2, 6, 24, 120, 720, 5040])
    744
    >>> eudex_hamming('ATCG', 'TAGC', [1, 1, 2, 6, 24, 120, 720, 5040])
    6243
    """
    def _gen_fibonacci():
        """Yield the next Fibonacci number.

        Based on https://www.python-course.eu/generators.php
        Starts at Fibonacci number 3 (the second 1)

        :returns: the next Fibonacci number
        :rtype: int
        """
        num_a, num_b = 1, 2
        while True:
            yield num_a
            num_a, num_b = num_b, num_a + num_b

    def _gen_exponential(base=2):
        """Yield the next value in an exponential series of the base.

        Starts at base**0

        :param int base: the base to exponentiate
        :returns: the next power of `base`
        :rtype: int
        """
        exp = 0
        while True:
            yield base ** exp
            exp += 1

    # Calculate the eudex hashes and XOR them
    xored = (eudex(src, max_length=max_length) ^
             eudex(tar, max_length=max_length))

    # Simple hamming distance (all bits are equal)
    if not weights:
        binary = bin(xored)
        distance = binary.count('1')
        if normalized:
            return distance/(len(binary)-2)
        return distance

    # If weights is a function, it should create a generator,
    # which we now use to populate a list
    if callable(weights):
        weights = weights()
    elif weights == 'exponential':
        weights = _gen_exponential()
    elif weights == 'fibonacci':
        weights = _gen_fibonacci()
    if isinstance(weights, GeneratorType):
        weights = [next(weights) for _ in range(max_length)][::-1]

    # Sum the weighted hamming distance
    distance = 0
    max_distance = 0
    while (xored or normalized) and weights:
        max_distance += 8*weights[-1]
        distance += bin(xored & 0xFF).count('1') * weights.pop()
        xored >>= 8

    if normalized:
        distance /= max_distance

    return distance


def dist_eudex(src, tar, weights='exponential', max_length=8):
    """Return normalized Hamming distance between Eudex hashes of two terms.

    This is Eudex distance normalized to [0, 1].

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str, iterable, or generator function weights: the weights or weights
        generator function
    :param max_length: the number of characters to encode as a eudex hash
    :returns: the normalized Eudex distance
    :rtype: float

    >>> round(dist_eudex('cat', 'hat'), 12)
    0.062745098039
    >>> round(dist_eudex('Niall', 'Neil'), 12)
    0.000980392157
    >>> round(dist_eudex('Colin', 'Cuilen'), 12)
    0.004901960784
    >>> round(dist_eudex('ATCG', 'TAGC'), 12)
    0.197549019608
    """
    return eudex_hamming(src, tar, weights, max_length, True)


def sim_eudex(src, tar, weights='exponential', max_length=8):
    """Return normalized Hamming similarity between Eudex hashes of two terms.

    Normalized Eudex similarity is the complement of normalized Eudex distance:
    :math:`sim_{Eudex} = 1 - dist_{Eudex}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str, iterable, or generator function weights: the weights or weights
        generator function
    :param max_length: the number of characters to encode as a eudex hash
    :returns: the normalized Eudex similarity
    :rtype: float

    >>> round(sim_eudex('cat', 'hat'), 12)
    0.937254901961
    >>> round(sim_eudex('Niall', 'Neil'), 12)
    0.999019607843
    >>> round(sim_eudex('Colin', 'Cuilen'), 12)
    0.995098039216
    >>> round(sim_eudex('ATCG', 'TAGC'), 12)
    0.802450980392
    """
    return 1-dist_eudex(src, tar, weights, max_length)


def sift4_simplest(src, tar, max_offset=5):
    """Return the "simplest" Sift4 distance between two terms.

    This is an approximation of edit distance, described in
    :cite:`Zackwehdex:2014`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param max_offset: the number of characters to search for matching letters
    :returns: the Sift4 distance according to the simplest formula
    :rtype: int

    >>> sift4_simplest('cat', 'hat')
    1
    >>> sift4_simplest('Niall', 'Neil')
    2
    >>> sift4_simplest('Colin', 'Cuilen')
    3
    >>> sift4_simplest('ATCG', 'TAGC')
    2
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


def sift4_common(src, tar, max_offset=5, max_distance=0):
    """Return the "common" Sift4 distance between two terms.

    This is an approximation of edit distance, described in
    :cite:`Zackwehdex:2014`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :returns: the Sift4 distance according to the common formula
    :rtype: int

    >>> sift4_common('cat', 'hat')
    1
    >>> sift4_common('Niall', 'Neil')
    2
    >>> sift4_common('Colin', 'Cuilen')
    3
    >>> sift4_common('ATCG', 'TAGC')
    2
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


def dist_sift4(src, tar, max_offset=5, max_distance=0):
    """Return the normalized "common" Sift4 distance between two terms.

    This is Sift4 distance, normalized to [0, 1].

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :returns: the normalized Sift4 distance
    :rtype: float

    >>> round(dist_sift4('cat', 'hat'), 12)
    0.333333333333
    >>> dist_sift4('Niall', 'Neil')
    0.4
    >>> dist_sift4('Colin', 'Cuilen')
    0.5
    >>> dist_sift4('ATCG', 'TAGC')
    0.5
    """
    return (sift4_common(src, tar, max_offset, max_distance) /
            (max(len(src), len(tar), 1)))


def sim_sift4(src, tar, max_offset=5, max_distance=0):
    """Return the normalized "common" Sift4 similarity of two terms.

    Normalized Sift4 similarity is the complement of normalized Sift4 distance:
    :math:`sim_{Sift4} = 1 - dist_{Sift4}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :returns: the normalized Sift4 similarity
    :rtype: float

    >>> round(sim_sift4('cat', 'hat'), 12)
    0.666666666667
    >>> sim_sift4('Niall', 'Neil')
    0.6
    >>> sim_sift4('Colin', 'Cuilen')
    0.5
    >>> sim_sift4('ATCG', 'TAGC')
    0.5
    """
    return 1-dist_sift4(src, tar, max_offset, max_distance)


def sim_baystat(src, tar, min_ss_len=None, left_ext=None, right_ext=None):
    """Return the Baystat similarity.

    Good results for shorter words are reported when setting min_ss_len to 1
    and either left_ext OR right_ext to 1.

    The Baystat similarity is defined in :cite:`Furnohr:2002`.

    This is ostensibly a port of the R module PPRL's implementation:
    https://github.com/cran/PPRL/blob/master/src/MTB_Baystat.cpp
    :cite:`Rukasz:2018`. As such, this could be made more pythonic.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param int min_ss_len: minimum substring length to be considered
    :param int left_ext: left-side extension length
    :param int right_ext: right-side extension length
    :returns: the Baystat similarity
    :rtype: float

    >>> round(sim_baystat('cat', 'hat'), 12)
    0.666666666667
    >>> sim_baystat('Niall', 'Neil')
    0.4
    >>> round(sim_baystat('Colin', 'Cuilen'), 12)
    0.166666666667
    >>> sim_baystat('ATCG', 'TAGC')
    0.0
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

    while True:
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

            # The following is unnecessary, I think
            # if (search_begin + left_ext_len + min_ss_len + right_ext_len <=
            #         len(tar)):
            search_val = tar[search_begin:(search_begin + left_ext_len +
                                           min_ss_len + right_ext_len)]

            ix += 1

        if hit_len > 0:
            tar = flagged_tar

        match_len += hit_len
        pos += ix


def dist_baystat(src, tar, min_ss_len=None, left_ext=None, right_ext=None):
    """Return the Baystat distance.

    Normalized Baystat similarity is the complement of normalized Baystat
    distance: :math:`sim_{Baystat} = 1 - dist_{Baystat}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param int min_ss_len: minimum substring length to be considered
    :param int left_ext: left-side extension length
    :param int right_ext: right-side extension length
    :returns: the Baystat distance
    :rtype: float

    >>> round(dist_baystat('cat', 'hat'), 12)
    0.333333333333
    >>> dist_baystat('Niall', 'Neil')
    0.6
    >>> round(dist_baystat('Colin', 'Cuilen'), 12)
    0.833333333333
    >>> dist_baystat('ATCG', 'TAGC')
    1.0
    """
    return 1-sim_baystat(src, tar, min_ss_len, left_ext, right_ext)


def typo(src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5), layout='QWERTY'):
    """Return the typo distance between two strings.

    This is inspired by Typo-Distance :cite:`Song:2011`, and a fair bit of
    this was copied from that module. Compared to the original, this supports
    different metrics for substitution.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str metric: supported values include: 'euclidean', 'manhattan',
          'log-euclidean', and 'log-manhattan'
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits: inserts, deletes, substitutions, and shift, respectively (by
        default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless
        a log metric is used.
    :param str layout: name of the keyboard layout to use (Currently supported:
        QWERTY, Dvorak, AZERTY, QWERTZ)
    :returns: typo distance
    :rtype: float

    >>> typo('cat', 'hat')
    1.5811388
    >>> typo('Niall', 'Neil')
    2.8251407
    >>> typo('Colin', 'Cuilen')
    3.4142137
    >>> typo('ATCG', 'TAGC')
    2.5

    >>> typo('cat', 'hat', metric='manhattan')
    2.0
    >>> typo('Niall', 'Neil', metric='manhattan')
    3.0
    >>> typo('Colin', 'Cuilen', metric='manhattan')
    3.5
    >>> typo('ATCG', 'TAGC', metric='manhattan')
    2.5

    >>> typo('cat', 'hat', metric='log-manhattan')
    0.804719
    >>> typo('Niall', 'Neil', metric='log-manhattan')
    2.2424533
    >>> typo('Colin', 'Cuilen', metric='log-manhattan')
    2.2424533
    >>> typo('ATCG', 'TAGC', metric='log-manhattan')
    2.3465736
    """
    ins_cost, del_cost, sub_cost, shift_cost = cost

    if src == tar:
        return 0.0
    if not src:
        return len(tar) * ins_cost
    if not tar:
        return len(src) * del_cost

    kbs = {'QWERTY': (
        (('`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='),
         ('', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
          '\\'),
         ('', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\''),
         ('', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/')),
        (('~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'),
         ('', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'),
         ('', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'),
         ('', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?'))
    ), 'Dvorak': (
        (('`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '[', ']'),
         ('', '\'', ',', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l', '/', '=',
          '\\'),
         ('', 'a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's', '-'),
         ('', ';', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z')),
        (('~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}'),
         ('', '"', '<', '>', 'P', 'Y', 'F', 'G', 'C', 'R', 'L', '?', '+', '|'),
         ('', 'A', 'O', 'E', 'U', 'I', 'D', 'H', 'T', 'N', 'S', '_'),
         ('', ':', 'Q', 'J', 'K', 'X', 'B', 'M', 'W', 'V', 'Z'))
    ), 'AZERTY': (
        (('²', '&', 'é', '"', '\'', '(', '-', 'è', '_', 'ç', 'à', ')', '='),
         ('', 'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '', '$'),
         ('', 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'ù', '*'),
         ('<', 'w', 'x', 'c', 'v', 'b', 'n', ',', ';', ':', '!')),
        (('~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '°', '+'),
         ('', 'A', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '', '£'),
         ('', 'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'Ù', 'μ'),
         ('>', 'W', 'X', 'C', 'V', 'B', 'N', '?', '.', '/', '§'))
    ), 'QWERTZ': (
        (('', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ß', ''),
         ('', 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', ' ü', '+',
          '\\'),
         ('', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#'),
         ('<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-')),
        (('°', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ''),
         ('', 'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'Ü', '*', ''),
         ('', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', '\''),
         ('>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_'))
    )}

    keyboard = kbs[layout]
    lowercase = {item for sublist in keyboard[0] for item in sublist}
    uppercase = {item for sublist in keyboard[1] for item in sublist}

    def _kb_array_for_char(char):
        """Return the keyboard layout that contains ch."""
        if char in lowercase:
            return keyboard[0]
        elif char in uppercase:
            return keyboard[1]
        raise ValueError(char + ' not found in any keyboard layouts')

    def _get_char_coord(char, kb_array):
        """Return the row & column of char in the keyboard."""
        for row in kb_array:  # pragma: no branch
            if char in row:
                return kb_array.index(row), row.index(char)

    def _euclidean_keyboard_distance(char1, char2):
        row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
        row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
        return ((row1 - row2) ** 2 + (col1 - col2) ** 2) ** 0.5

    def _manhattan_keyboard_distance(char1, char2):
        row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
        row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
        return abs(row1 - row2) + abs(col1 - col2)

    def _log_euclidean_keyboard_distance(char1, char2):
        return log(1 + _euclidean_keyboard_distance(char1, char2))

    def _log_manhattan_keyboard_distance(char1, char2):
        return log(1 + _manhattan_keyboard_distance(char1, char2))

    metric_dict = {'euclidean': _euclidean_keyboard_distance,
                   'manhattan': _manhattan_keyboard_distance,
                   'log-euclidean': _log_euclidean_keyboard_distance,
                   'log-manhattan': _log_manhattan_keyboard_distance}

    def _substitution_cost(char1, char2):
        cost = sub_cost
        cost *= (metric_dict[metric](char1, char2) +
                 shift_cost * (_kb_array_for_char(char1) !=
                               _kb_array_for_char(char2)))
        return cost

    d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)
    for i in range(len(src) + 1):
        d_mat[i, 0] = i * del_cost
    for j in range(len(tar) + 1):
        d_mat[0, j] = j * ins_cost

    for i in range(len(src)):
        for j in range(len(tar)):
            d_mat[i + 1, j + 1] = min(
                d_mat[i + 1, j] + ins_cost,  # ins
                d_mat[i, j + 1] + del_cost,  # del
                d_mat[i, j] + (_substitution_cost(src[i], tar[j])
                               if src[i] != tar[j] else 0)  # sub/==
            )

    return d_mat[len(src), len(tar)]


def dist_typo(src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5)):
    """Return the normalized typo distance between two strings.

    This is typo distance, normalized to [0, 1].

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str metric: supported values include: 'euclidean', 'manhattan',
          'log-euclidean', and 'log-manhattan'
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits: inserts, deletes, substitutions, and shift, respectively (by
        default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless
        a log metric is used.
    :returns: normalized typo distance
    :rtype: float

    >>> round(dist_typo('cat', 'hat'), 12)
    0.527046283086
    >>> round(dist_typo('Niall', 'Neil'), 12)
    0.565028142929
    >>> round(dist_typo('Colin', 'Cuilen'), 12)
    0.569035609563
    >>> dist_typo('ATCG', 'TAGC')
    0.625
    """
    if src == tar:
        return 0
    ins_cost, del_cost = cost[:2]
    return (typo(src, tar, metric, cost) /
            (max(len(src)*del_cost, len(tar)*ins_cost)))


def sim_typo(src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5)):
    """Return the normalized typo similarity between two strings.

    Normalized typo similarity is the complement of normalized typo distance:
    :math:`sim_{typo} = 1 - dist_{typo}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str metric: supported values include: 'euclidean', 'manhattan',
          'log-euclidean', and 'log-manhattan'
    :param tuple cost: a 4-tuple representing the cost of the four possible
        edits: inserts, deletes, substitutions, and shift, respectively (by
        default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless
        a log metric is used.
    :returns: normalized typo similarity
    :rtype: float

    >>> round(sim_typo('cat', 'hat'), 12)
    0.472953716914
    >>> round(sim_typo('Niall', 'Neil'), 12)
    0.434971857071
    >>> round(sim_typo('Colin', 'Cuilen'), 12)
    0.430964390437
    >>> sim_typo('ATCG', 'TAGC')
    0.375
    """
    return 1 - dist_typo(src, tar, metric, cost)


def dist_indel(src, tar):
    """Return the indel distance between two strings.

    This is equivalent to levenshtein distance, when only inserts and deletes
    are possible.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: indel distance
    :rtype: float

    >>> round(dist_indel('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_indel('Niall', 'Neil'), 12)
    0.333333333333
    >>> round(dist_indel('Colin', 'Cuilen'), 12)
    0.454545454545
    >>> dist_indel('ATCG', 'TAGC')
    0.5
    """
    if src == tar:
        return 0
    return (levenshtein(src, tar, mode='lev', cost=(1, 1, 9999, 9999)) /
            (len(src) + len(tar)))


def sim_indel(src, tar):
    """Return the indel similarity of two strings.

    This is equivalent to levenshtein similarity, when only inserts and deletes
    are possible.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: indel similarity
    :rtype: float

    >>> round(sim_indel('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_indel('Niall', 'Neil'), 12)
    0.666666666667
    >>> round(sim_indel('Colin', 'Cuilen'), 12)
    0.545454545455
    >>> sim_indel('ATCG', 'TAGC')
    0.5
    """
    return 1-dist_indel(src, tar)


def _synoname_strip_punct(word):
    """Return a word with punctuation stripped out.

    :param word: a word to strip punctuation from
    :returns: The word stripped of punctuation

    >>> _synoname_strip_punct('AB;CD EF-GH$IJ')
    'ABCD EFGHIJ'
    """
    stripped = ''
    for char in word:
        if char not in set(',-./:;"&\'()!{|}?$%*+<=>[\\]^_`~'):
            stripped += char
    return stripped.strip()


def _synoname_word_approximation(src_ln, tar_ln, src_fn='', tar_fn='',
                                 features=None):
    """Return the Synoname word approximation score for two names.

    :param str src_ln: last name of the source
    :param str tar_ln: last name of the target
    :param str src_fn: first name of the source (optional)
    :param str tar_fn: first name of the target (optional)
    :param features: a dict containing special features calculated via
        fingerprint.synoname_toolcode() (optional)
    :returns: The word approximation score
    :rtype: float

    >>> _synoname_word_approximation('Smith Waterman', 'Waterman',
    ... 'Tom Joe Bob', 'Tom Joe')
    0.6
    """
    if features is None:
        features = {}
    if 'src_specials' not in features:
        features['src_specials'] = []
    if 'tar_specials' not in features:
        features['tar_specials'] = []

    src_len_specials = len(features['src_specials'])
    tar_len_specials = len(features['tar_specials'])

    # 1
    if (('gen_conflict' in features and features['gen_conflict']) or
            ('roman_conflict' in features and features['roman_conflict'])):
        return 0

    # 3 & 7
    full_tar1 = ' '.join((tar_ln, tar_fn)).replace('-', ' ').strip()
    for s_pos, s_type in features['tar_specials']:
        if s_type == 'a':
            full_tar1 = full_tar1[:-(1+len(_synoname_special_table[s_pos][1]))]
        elif s_type == 'b':
            loc = full_tar1.find(' '+_synoname_special_table[s_pos][1]+' ')+1
            full_tar1 = (full_tar1[:loc] +
                         full_tar1[loc +
                                   len(_synoname_special_table[s_pos][1]):])
        elif s_type == 'c':
            full_tar1 = full_tar1[1+len(_synoname_special_table[s_pos][1]):]

    full_src1 = ' '.join((src_ln, src_fn)).replace('-', ' ').strip()
    for s_pos, s_type in features['src_specials']:
        if s_type == 'a':
            full_src1 = full_src1[:-(1+len(_synoname_special_table[s_pos][1]))]
        elif s_type == 'b':
            loc = full_src1.find(' '+_synoname_special_table[s_pos][1]+' ')+1
            full_src1 = (full_src1[:loc] +
                         full_src1[loc +
                                   len(_synoname_special_table[s_pos][1]):])
        elif s_type == 'c':
            full_src1 = full_src1[1+len(_synoname_special_table[s_pos][1]):]

    full_tar2 = full_tar1
    for s_pos, s_type in features['tar_specials']:
        if s_type == 'd':
            full_tar2 = full_tar2[len(_synoname_special_table[s_pos][1]):]
        elif s_type == 'X' and _synoname_special_table[s_pos][1] in full_tar2:
            loc = full_tar2.find(' '+_synoname_special_table[s_pos][1])
            full_tar2 = (full_tar2[:loc] +
                         full_tar2[loc +
                                   len(_synoname_special_table[s_pos][1]):])

    full_src2 = full_src1
    for s_pos, s_type in features['src_specials']:
        if s_type == 'd':
            full_src2 = full_src2[len(_synoname_special_table[s_pos][1]):]
        elif s_type == 'X' and _synoname_special_table[s_pos][1] in full_src2:
            loc = full_src2.find(' '+_synoname_special_table[s_pos][1])
            full_src2 = (full_src2[:loc] +
                         full_src2[loc +
                                   len(_synoname_special_table[s_pos][1]):])

    full_tar1 = _synoname_strip_punct(full_tar1)
    tar1_words = full_tar1.split()
    tar1_num_words = len(tar1_words)

    full_src1 = _synoname_strip_punct(full_src1)
    src1_words = full_src1.split()
    src1_num_words = len(src1_words)

    full_tar2 = _synoname_strip_punct(full_tar2)
    tar2_words = full_tar2.split()
    tar2_num_words = len(tar2_words)

    full_src2 = _synoname_strip_punct(full_src2)
    src2_words = full_src2.split()
    src2_num_words = len(src2_words)

    # 2
    if (src1_num_words < 2 and src_len_specials == 0 and src2_num_words < 2 and
            tar_len_specials == 0):
        return 0

    # 4
    if (tar1_num_words == 1 and src1_num_words == 1 and
            tar1_words[0] == src1_words[0]):
        return 1
    if tar1_num_words < 2 and tar_len_specials == 0:
        return 0

    # 5
    last_found = False
    for word in tar1_words:
        if src_ln.endswith(word) or word+' ' in src_ln:
            last_found = True

    if not last_found:
        for word in src1_words:
            if tar_ln.endswith(word) or word+' ' in tar_ln:
                last_found = True

    # 6
    matches = 0
    if last_found:
        for i, s_word in enumerate(src1_words):
            for j, t_word in enumerate(tar1_words):
                if s_word == t_word:
                    src1_words[i] = '@'
                    tar1_words[j] = '@'
                    matches += 1
    w_ratio = matches/max(tar1_num_words, src1_num_words)
    if matches > 1 or (matches == 1 and
                       src1_num_words == 1 and tar1_num_words == 1 and
                       (tar_len_specials > 0 or src_len_specials > 0)):
        return w_ratio

    # 8
    if (tar2_num_words == 1 and src2_num_words == 1 and
            tar2_words[0] == src2_words[0]):
        return 1
    # I see no way that the following can be True if the equivalent in
    # #4 was False.
    if tar2_num_words < 2 and tar_len_specials == 0:  # pragma: no cover
        return 0

    # 9
    last_found = False
    for word in tar2_words:
        if src_ln.endswith(word) or word+' ' in src_ln:
            last_found = True

    if not last_found:
        for word in src2_words:
            if tar_ln.endswith(word) or word+' ' in tar_ln:
                last_found = True

    if not last_found:
        return 0

    # 10
    matches = 0
    if last_found:
        for i, s_word in enumerate(src2_words):
            for j, t_word in enumerate(tar2_words):
                if s_word == t_word:
                    src2_words[i] = '@'
                    tar2_words[j] = '@'
                    matches += 1
    w_ratio = matches/max(tar2_num_words, src2_num_words)
    if matches > 1 or (matches == 1 and
                       src2_num_words == 1 and tar2_num_words == 1 and
                       (tar_len_specials > 0 or src_len_specials > 0)):
        return w_ratio

    return 0


def synoname(src, tar, word_approx_min=0.3, char_approx_min=0.73,
             tests=2**12-1, ret_name=False):
    """Return the Synoname similarity type of two words.

    Cf. :cite:`Getty:1991,Gross:1991`

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool ret_name: return the name of the match type rather than the
        int value
    :param float word_approx_min: the minimum word approximation value to
        signal a 'word_approx' match
    :param float char_approx_min: the minimum character approximation value to
        signal a 'char_approx' match
    :param int or Iterable tests: either an integer indicating tests to
        perform or a list of test names to perform (defaults to performing all
        tests)
    :param bool ret_name: if True, returns the match name rather than its
        integer equivalent
    :returns: Synoname value
    :rtype: int (or str if ret_name is True)

    >>> synoname(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''))
    2
    >>> synoname(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''),
    ... ret_name=True)
    'omission'
    >>> synoname(('Dore', 'Gustave', ''),
    ... ('Dore', 'Paul Gustave Louis Christophe', ''),
    ... ret_name=True)
    'inclusion'
    >>> synoname(('Pereira', 'I. R.', ''), ('Pereira', 'I. Smith', ''),
    ... ret_name=True)
    'word_approx'
    """
    test_dict = {val: 2**n for n, val in enumerate([
        'exact', 'omission', 'substitution', 'transposition', 'punctuation',
        'initials', 'extension', 'inclusion', 'no_first', 'word_approx',
        'confusions', 'char_approx'])}
    match_name = ['', 'exact', 'omission', 'substitution', 'transposition',
                  'punctuation', 'initials', 'extension', 'inclusion',
                  'no_first', 'word_approx', 'confusions', 'char_approx',
                  'no_match']
    match_type_dict = {val: n for n, val in enumerate(match_name)}

    if isinstance(tests, Iterable):
        new_tests = 0
        for term in tests:
            if term in test_dict:
                new_tests += test_dict[term]
        tests = new_tests

    if isinstance(src, tuple):
        src_ln, src_fn, src_qual = src
    elif '#' in src:
        src_ln, src_fn, src_qual = src.split('#')[-3:]
    else:
        src_ln, src_fn, src_qual = src, '', ''

    if isinstance(tar, tuple):
        tar_ln, tar_fn, tar_qual = tar
    elif '#' in tar:
        tar_ln, tar_fn, tar_qual = tar.split('#')[-3:]
    else:
        tar_ln, tar_fn, tar_qual = tar, '', ''

    def _split_special(spec):
        spec_list = []
        while spec:
            spec_list.append((int(spec[:3]), spec[3:4]))
            spec = spec[4:]
        return spec_list

    def _fmt_retval(val):
        if ret_name:
            return match_name[val]
        return val

    # 1. Preprocessing

    # Lowercasing
    src_fn = src_fn.strip().lower()
    src_ln = src_ln.strip().lower()
    src_qual = src_qual.strip().lower()

    tar_fn = tar_fn.strip().lower()
    tar_ln = tar_ln.strip().lower()
    tar_qual = tar_qual.strip().lower()

    # Create toolcodes
    src_ln, src_fn, src_tc = synoname_toolcode(src_ln, src_fn, src_qual)
    tar_ln, tar_fn, tar_tc = synoname_toolcode(tar_ln, tar_fn, tar_qual)

    src_generation = int(src_tc[2])
    src_romancode = int(src_tc[3:6])
    src_len_fn = int(src_tc[6:8])
    src_tc = src_tc.split('$')
    src_specials = _split_special(src_tc[1])

    tar_generation = int(tar_tc[2])
    tar_romancode = int(tar_tc[3:6])
    tar_len_fn = int(tar_tc[6:8])
    tar_tc = tar_tc.split('$')
    tar_specials = _split_special(tar_tc[1])

    gen_conflict = ((src_generation != tar_generation) and
                    bool(src_generation or tar_generation))
    roman_conflict = ((src_romancode != tar_romancode) and
                      bool(src_romancode or tar_romancode))

    ln_equal = src_ln == tar_ln
    fn_equal = src_fn == tar_fn

    # approx_c
    def _approx_c():
        if gen_conflict or roman_conflict:
            return False, 0

        full_src = ' '.join((src_ln, src_fn))
        if full_src.startswith('master '):
            full_src = full_src[len('master '):]
            for intro in ['of the ', 'of ', 'known as the ', 'with the ',
                          'with ']:
                if full_src.startswith(intro):
                    full_src = full_src[len(intro):]

        full_tar = ' '.join((tar_ln, tar_fn))
        if full_tar.startswith('master '):
            full_tar = full_tar[len('master '):]
            for intro in ['of the ', 'of ', 'known as the ', 'with the ',
                          'with ']:
                if full_tar.startswith(intro):
                    full_tar = full_tar[len(intro):]

        loc_ratio = sim_ratcliff_obershelp(full_src, full_tar)
        return loc_ratio >= char_approx_min, loc_ratio

    approx_c_result, ca_ratio = _approx_c()

    if tests & test_dict['exact'] and fn_equal and ln_equal:
        return _fmt_retval(match_type_dict['exact'])
    if tests & test_dict['omission']:
        if (fn_equal and
                levenshtein(src_ln, tar_ln, cost=(1, 1, 99, 99)) == 1):
            if not roman_conflict:
                return _fmt_retval(match_type_dict['omission'])
        elif (ln_equal and
              levenshtein(src_fn, tar_fn, cost=(1, 1, 99, 99)) == 1):
            return _fmt_retval(match_type_dict['omission'])
    if tests & test_dict['substitution']:
        if (fn_equal and
                levenshtein(src_ln, tar_ln, cost=(99, 99, 1, 99)) == 1):
            return _fmt_retval(match_type_dict['substitution'])
        elif (ln_equal and
              levenshtein(src_fn, tar_fn, cost=(99, 99, 1, 99)) == 1):
            return _fmt_retval(match_type_dict['substitution'])
    if tests & test_dict['transposition']:
        if (fn_equal and
                (levenshtein(src_ln, tar_ln, mode='osa', cost=(99, 99, 99, 1))
                 == 1)):
            return _fmt_retval(match_type_dict['transposition'])
        elif (ln_equal and
              (levenshtein(src_fn, tar_fn, mode='osa', cost=(99, 99, 99, 1))
               == 1)):
            return _fmt_retval(match_type_dict['transposition'])
    if tests & test_dict['punctuation']:
        np_src_fn = _synoname_strip_punct(src_fn)
        np_tar_fn = _synoname_strip_punct(tar_fn)
        np_src_ln = _synoname_strip_punct(src_ln)
        np_tar_ln = _synoname_strip_punct(tar_ln)

        if (np_src_fn == np_tar_fn) and (np_src_ln == np_tar_ln):
            return _fmt_retval(match_type_dict['punctuation'])

        np_src_fn = _synoname_strip_punct(src_fn.replace('-', ' '))
        np_tar_fn = _synoname_strip_punct(tar_fn.replace('-', ' '))
        np_src_ln = _synoname_strip_punct(src_ln.replace('-', ' '))
        np_tar_ln = _synoname_strip_punct(tar_ln.replace('-', ' '))

        if (np_src_fn == np_tar_fn) and (np_src_ln == np_tar_ln):
            return _fmt_retval(match_type_dict['punctuation'])

    if tests & test_dict['initials'] and ln_equal:
        if src_fn and tar_fn:
            src_initials = _synoname_strip_punct(src_fn).split()
            tar_initials = _synoname_strip_punct(tar_fn).split()
            initials = bool((len(src_initials) == len(''.join(src_initials)))
                            or
                            (len(tar_initials) == len(''.join(tar_initials))))
            if initials:
                src_initials = ''.join(_[0] for _ in src_initials)
                tar_initials = ''.join(_[0] for _ in tar_initials)
                if src_initials == tar_initials:
                    return _fmt_retval(match_type_dict['initials'])
                initial_diff = abs(len(src_initials)-len(tar_initials))
                if (initial_diff and
                        ((initial_diff ==
                          levenshtein(src_initials, tar_initials,
                                      cost=(1, 99, 99, 99))) or
                         (initial_diff ==
                          levenshtein(tar_initials, src_initials,
                                      cost=(1, 99, 99, 99))))):
                    return _fmt_retval(match_type_dict['initials'])
    if tests & test_dict['extension']:
        if src_ln[1] == tar_ln[1] and (src_ln.startswith(tar_ln) or
                                       tar_ln.startswith(src_ln)):
            if (((not src_len_fn and not tar_len_fn) or
                 (tar_fn and src_fn.startswith(tar_fn)) or
                 (src_fn and tar_fn.startswith(src_fn)))
                    and not roman_conflict):
                return _fmt_retval(match_type_dict['extension'])
    if tests & test_dict['inclusion'] and ln_equal:
        if (src_fn and src_fn in tar_fn) or (tar_fn and tar_fn in src_ln):
            return _fmt_retval(match_type_dict['inclusion'])
    if tests & test_dict['no_first'] and ln_equal:
        if src_fn == '' or tar_fn == '':
            return _fmt_retval(match_type_dict['no_first'])
    if tests & test_dict['word_approx']:
        ratio = _synoname_word_approximation(src_ln, tar_ln, src_fn, tar_fn,
                                             {'gen_conflict': gen_conflict,
                                              'roman_conflict': roman_conflict,
                                              'src_specials': src_specials,
                                              'tar_specials': tar_specials})
        if ratio == 1 and tests & test_dict['confusions']:
            if (' '.join((src_fn, src_ln)).strip() ==
                    ' '.join((tar_fn, tar_ln)).strip()):
                return _fmt_retval(match_type_dict['confusions'])
        if ratio >= word_approx_min:
            return _fmt_retval(match_type_dict['word_approx'])
    if tests & test_dict['char_approx']:
        if ca_ratio >= char_approx_min:
            return _fmt_retval(match_type_dict['char_approx'])
    return _fmt_retval(match_type_dict['no_match'])


###############################################################################


def sim(src, tar, method=sim_levenshtein):
    """Return a similarity of two strings.

    This is a generalized function for calling other similarity functions.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param function method: specifies the similarity metric (Levenshtein by
        default)
    :returns: similarity according to the specified function
    :rtype: float

    >>> round(sim('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim('Niall', 'Neil'), 12)
    0.4
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

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param function method: specifies the similarity metric (Levenshtein by
        default) -- Note that this takes a similarity metric function, not
        a distance metric function.
    :returns: distance according to the specified function
    :rtype: float

    >>> round(dist('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist('Niall', 'Neil'), 12)
    0.6
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
