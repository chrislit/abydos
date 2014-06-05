# -*- coding: utf-8 -*-
"""abydos.distance

The distance module implements string edit distance functions including:
    Levenshtein distance (incl. a [0, 1] normalized variant)
    Optimal String Alignment distance (incl. a [0, 1] normalized variant)
    Levenshtein-Damerau distance (incl. a [0, 1] normalized variant)
    Hamming distance (incl. a [0, 1] normalized variant)
    Tversky index
    Sørensen–Dice coefficient & distance
    Jaccard similarity coefficient & distance
    Tanimoto coefficient & distance
    Jaro distance
    Jaro-Winkler distance (incl. the strcmp95 algorithm variant)
    Longest common substring
    Match Rating Algorithm similarity


Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
from __future__ import division
from ._compat import _range
import numpy as np
import sys
import math
from collections import defaultdict
from .qgram import QGrams
from .phonetic import mra
import codecs
try:
    import lzma
except ImportError:
    # If there system lacks the lzma library, that's fine, but lzma comrpession
    # similarity won't be supported.
    pass


def levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein distance between two string arguments

    Arguments:
    src, tar -- two strings to be compared
    mode -- specifies a mode for computing the Levenshtein distance:
            'lev' (default) computes the ordinary Levenshtein distance,
                in which edits may include inserts, deletes, and substitutions
            'osa' computes the Optimal String Alignment distance, in which
                edits may include inserts, deletes, substitutions, and
                transpositions but substrings may only be edited once
            'dam' computes the Damerau-Levenshtein distance, in which
                edits may include inserts, deletes, substitutions, and
                transpositions and substrings may undergo repeated edits
    cost -- a 4-tuple representing the cost of the four possible edits:
                inserts, deletes, substitutions, and transpositions,
                respectively (by default: (1, 1, 1, 1))

    Description:
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
    """
    ins_cost, del_cost, sub_cost, trans_cost = cost

    if len(src) == 0:
        return len(tar) * ins_cost
    if len(tar) == 0:
        return len(src) * del_cost

    if 'dam' in mode:
        return _damerau_levenshtein(src, tar, cost)

    # pylint: disable=no-member
    d_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)
    # pylint: enable=no-member
    for i in _range(len(src)+1):
        d_mat[i, 0] = i * del_cost
    for j in _range(len(tar)+1):
        d_mat[0, j] = j * ins_cost

    for i in _range(len(src)):
        for j in _range(len(tar)):
            d_mat[i+1, j+1] = min(
                d_mat[i+1, j] + ins_cost, # ins
                d_mat[i, j+1] + del_cost, # del
                d_mat[i, j] + (sub_cost if src[i] != tar[j] else 0) # sub/==
            )

            if mode == 'osa':
                if (i+1 > 1 and j+1 > 1 and src[i] == tar[j-1] and
                    src[i-1] == tar[j]):
                    d_mat[i+1, j+1] = min(
                                      d_mat[i+1, j+1],
                                      d_mat[i-1, j-1] + trans_cost  # trans
                                      )

    return d_mat[len(src), len(tar)]


def _damerau_levenshtein(src, tar, cost=(1, 1, 1, 1)):
    """Return the Damerau-Levenshtein distance between two string arguments

    Arguments:
    src, tar -- two strings to be compared
    cost -- a 4-tuple representing the cost of the four possible edits:
                inserts, deletes, substitutions, and transpositions,
                respectively (by default: (1, 1, 1, 1))

    Description:
    This computes the Damerau-Levenshtein distance. Cf.
    https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

    Damerau-Levenshtein code based on Java code by Kevin L. Stern,
    under the MIT license:
    https://github.com/KevinStern/software-and-algorithms/blob/master/src/main/java/blogspot/software_and_algorithms/stern_library/string/DamerauLevenshteinAlgorithm.java
    """
    ins_cost, del_cost, sub_cost, trans_cost = cost

    if 2*trans_cost < ins_cost + del_cost:
        raise ValueError('Unsupported cost assignment; the cost of two \
transpositions must not be less than the cost of an insert \
plus a delete.')

    # pylint: disable=no-member
    d_mat = (np.zeros((len(src))*(len(tar)), dtype=np.int).
            reshape((len(src), len(tar))))
    # pylint: enable=no-member

    if src[0] != tar[0]:
        d_mat[0, 0] = min(sub_cost, ins_cost + del_cost)

    src_index_by_character = {}
    src_index_by_character[src[0]] = 0
    for i in _range(1, len(src)):
        del_distance = d_mat[i-1, 0] + del_cost
        ins_distance = (i+1) * del_cost + ins_cost
        match_distance = i * del_cost + \
        (0 if src[i] == tar[0] else sub_cost)
        d_mat[i, 0] = min(del_distance, ins_distance, match_distance)

    for j in _range(1, len(tar)):
        del_distance = (j+1) * ins_cost + del_cost
        ins_distance = d_mat[0, j-1] + ins_cost
        match_distance = j * ins_cost + \
        (0 if src[0] == tar[j] else sub_cost)
        d_mat[0, j] = min(del_distance, ins_distance, match_distance)

    for i in _range(1, len(src)):
        max_src_letter_match_index = (0 if src[i] == tar[0] else -1)
        for j in _range(1, len(tar)):
            candidate_swap_index = -1 if tar[j] not in \
            src_index_by_character else src_index_by_character[tar[j]]
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


def dist_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein distance normalized to the interval [0, 1]
    The arguments are identical to those of the levenshtein() function.

    Description:
    The Levenshtein distance is normalized by dividing the Levenshtein distance
    (calculated by any of the three supported methods) by the greater of
    the number of characters in src times the cost of a delete and
    the number of characters in tar times the cost of an insert.
    For the case in which all operations have cost == 1, this is equivalent
    to the greater of the length of the two strings src & tar.
    """
    if src == tar:
        return 0
    ins_cost, del_cost = cost[:2]
    return levenshtein(src, tar, mode, cost) \
        / (max(len(src)*del_cost, len(tar)*ins_cost))


def sim_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein similarity normalized to the interval [0, 1]
    The arguments are identical to those of the levenshtein() function.

    Description:
    The Levenshtein similarity is 1 - the Levenshtein distance
    """
    return 1 - dist_levenshtein(src, tar, mode, cost)


def hamming(src, tar, difflens=True):
    """Return the Hamming distance between two string arguments

    Arguments:
    src, tar -- two strings to be compared
    allow_different_lengths --
        If True (default, this returns the Hamming distance for those characters
        that have a matching character in both strings plus the difference in
        the strings' lengths. This is equivalent to  extending the shorter
        string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.

    Description:
    Hamming distance equals the number of character positions at which two
    strings differ. For strings of unequal lengths, it is not normally defined.
    By default, this implementation calculates the Hamming distance of the
    first n characters where n is the lesser of the two strings' lengths and
    adds to this the difference in string lengths.
    """
    if not difflens and len(src) != len(tar):
        raise ValueError("Undefined for sequences of unequal length; set \
difflens to True for Hamming distance between strings of unequal \
lengths.")

    hdist = 0
    if difflens:
        hdist += abs(len(src)-len(tar))
    hdist += sum(c1 != c2 for c1, c2 in zip(src, tar))

    return hdist


def dist_hamming(src, tar, difflens=True):
    """Return the Hamming distance normalized to the interval [0, 1]
    The arguments are identical to those of the hamming() function.

    Description:
    The Hamming distance is normalized by dividing the Levenshtein distance
    by the greater of the number of characters in src & tar (unless difflens is
    set to False, in which case an exception is raised).
    """
    if src == tar:
        return 0
    return hamming(src, tar, difflens) / max(len(src), len(tar))


def sim_hamming(src, tar, difflens=True):
    """Return the Hamming similarity normalized to the interval [0, 1]
    The arguments are identical to those of the hamming() function.

    Description:
    The Hamming similarity is 1 - the Hamming distance
    """
    return 1 - dist_hamming(src, tar, difflens)


def sim_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky index of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram
    alpha, beta -- two Tversky index parameters as indicated in the
        description below

    Description:
    The Tversky index is defined as:
    For two sets X and Y:
    S(X,Y) = |X∩Y| / (|X∩Y| + α|X-Y| + β|Y-X|)

    Cf. https://en.wikipedia.org/wiki/Tversky_index

    α = β = 1 is equivalent to the Jaccard & Tanimoto similarity coefficients
    α = β = 0.5 is equivalent to the Sorensen-Dice similarity coefficient

    Unequal α and β will tend to emphasize one or the other set's contributions
        (α>β emphasizes the contributions of X over Y; α<β emphasizes the
        contributions of Y over X).
    α and β > 1 emphsize unique contributions over the intersection.
    α and β < 1 emphsize the intersection over unique contributions.

    The symmetric variant is defined in Jiminez, Sergio, Claudio Becerra, and
    Alexander Gelbukh. 2013. SOFTCARDINALITY-CORE: Improving Text Overlap with
    Distributional Measures for Semantic Textual Similarity. This is activated
    by specifying a bias parameter.
    Cf. http://aclweb.org/anthology/S/S13/S13-1028.pdf
    """
    if alpha < 0 or beta < 0:
        raise ValueError('Unsupported weight assignment; alpha and beta must \
be greater than or equal to 0.')

    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0

    q_src = QGrams(src, qval)
    q_tar = QGrams(tar, qval)
    q_src_mag = q_src.count()
    q_tar_mag = q_tar.count()
    q_intersection_mag = sum((q_src & q_tar).values())

    if len(q_src) == 0 or len(q_tar) == 0:
        return 0.0

    if bias is None:
        return q_intersection_mag / (q_intersection_mag + alpha *
                                 (q_src_mag - q_intersection_mag)
                                  + beta * (q_tar_mag - q_intersection_mag))
    else:
        a_val = min(q_src_mag - q_intersection_mag,
                    q_tar_mag - q_intersection_mag)
        b_val = max(q_src_mag - q_intersection_mag,
                    q_tar_mag - q_intersection_mag)
        c_val = q_intersection_mag + bias
        return c_val / (beta * (alpha * a_val + (1 - alpha) * b_val) + c_val)


def dist_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky distance of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram
    alpha, beta -- two Tversky index parameters as indicated in the
        description below

    Description:
    The Tversky distance is 1 - the Tversky index (similarity)

    The symmetric variant is defined in Jiminez, Sergio, Claudio Becerra, and
    Alexander Gelbukh. 2013. SOFTCARDINALITY-CORE: Improving Text Overlap with
    Distributional Measures for Semantic Textual Similarity. This is activated
    by specifying a bias parameter.
    Cf. http://aclweb.org/anthology/S/S13/S13-1028.pdf
    """
    return 1 - sim_tversky(src, tar, qval, alpha, beta, bias)


def sim_dice(src, tar, qval=2):
    """Return the Sørensen–Dice coefficient of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    For two sets X and Y, the Sørensen–Dice coefficient is
    S(X,Y) = 2 * |X∩Y| / (|X| + |Y|)
    This is identical to the Tanimoto similarity coefficient
    and the Tversky index for α = β = 0.5
    """
    return sim_tversky(src, tar, qval, 0.5, 0.5)


def dist_dice(src, tar, qval=2):
    """Return the Sørensen–Dice distance of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    Sørensen–Dice distance is 1 - the Sørensen–Dice coefficient
    """
    return 1 - sim_dice(src, tar, qval)


def sim_jaccard(src, tar, qval=2):
    """Return the Jaccard similarity coefficient of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    For two sets X and Y, the Jaccard similarity coefficient is
    S(X,Y) = |X∩Y| / |X∪Y|
    This is identical to the Tanimoto similarity coefficient
    and the Tversky index for α = β = 1
    """
    return sim_tversky(src, tar, qval, 1, 1)


def dist_jaccard(src, tar, qval=2):
    """Return the Jaccard distance of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    Jaccard distance is 1 - the Jaccard coefficient
    """
    return 1 - sim_jaccard(src, tar, qval)


def sim_overlap(src, tar, qval=2):
    """Return the overlap coefficient of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    For two sets X and Y, the overlap coefficient is
    S(X,Y) = |X∩Y| / min(|X|,|Y|)
    """
    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0

    q_src = QGrams(src, qval)
    q_tar = QGrams(tar, qval)
    q_src_mag = q_src.count()
    q_tar_mag = q_tar.count()
    q_intersection_mag = sum((q_src & q_tar).values())

    return q_intersection_mag / min(q_src_mag, q_tar_mag)


def dist_overlap(src, tar, qval=2):
    """Return the overlap distance of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    overlap distance is 1 - the overlap coefficient
    """
    return 1 - sim_overlap(src, tar, qval)


def sim_tanimoto(src, tar, qval=2):
    """Return the Tanimoto similarity of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    For two sets X and Y, the Tanimoto similarity coefficient is
    S(X,Y) = |X∩Y| / |X∪Y|
    This is identical to the Jaccard similarity coefficient
    and the Tversky index for α = β = 1
    """
    return sim_jaccard(src, tar, qval)


def tanimoto(src, tar, qval=2):
    """Return the Tanimoto distance of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    Tanimoto distance is -log2(Tanimoto coefficient)
    """
    coeff = sim_jaccard(src, tar, qval)
    if coeff != 0:
        return math.log(coeff, 2)
    else:
        return float('-inf')


def sim_cosine(src, tar, qval=2):
    """Return the cosine similarity (Ochiai coefficient) of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    For two sets X and Y, the cosine similarity (Ochiai coefficient) is:
    S(X,Y) = |X∩Y| / √(|X| * |Y|)
    """
    if src == tar:
        return 1.0
    if not src or not tar:
        return 0.0

    q_src = QGrams(src, qval)
    q_tar = QGrams(tar, qval)
    q_src_mag = q_src.count()
    q_tar_mag = q_tar.count()
    q_intersection_mag = sum((q_src & q_tar).values())

    return q_intersection_mag / math.sqrt(q_src_mag * q_tar_mag)


def dist_cosine(src, tar, qval=2):
    """Return the cosine distance of two strings

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram

    Description:
    Coside distance is defined as 1 - the cosine similarity
    """
    return 1 - sim_cosine(src, tar, qval)


def sim_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 similarity between two string arguments.

    Arguments:
    src, tar -- two strings to be compared
    long_strings -- set to True to "Increase the probability of a match when
        the number of matched characters is large.  This option allows for a
        little more tolerance when the strings are large.  It is not an
        appropriate test when comparing fixed length fields such as phone and
        social security numbers."

    Description:
    This is a Python translation of the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    The above file is a US Government publication and, accordingly,
    in the public domain.

    This is based on the Jaro-Winkler distance, but also attempts to correct
    for some common typos and frequently confused characters. It is also
    limited to uppercase ASCII characters, so it is appropriate to American
    names, but not much else.
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
    ying_flag = [0 for i in _range(search_range)]
    yang_flag = [0 for j in _range(search_range)]
    search_range = search_range // 2 - 1
    if search_range < 0:
        search_range = 0

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

        #Optionally adjust for long strings.

        # After agreeing beginning chars, at least two more must agree and
        # the agreeing characters must be > .5 of remaining characters.
        if ((long_strings) and (minv > 4) and (num_com > i+1) and
            (2*num_com >= minv+i)):
            if not ying[0].isdigit():
                weight += (1.0-weight) * ((num_com-i-1) /
                                          (len(ying)+len(yang)-i*2+2))

    return weight


def dist_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 distance between two string arguments.

    Arguments:
    src, tar -- two strings to be compared
    long_strings -- set to True to "Increase the probability of a match when
        the number of matched characters is large.  This option allows for a
        little more tolerance when the strings are large.  It is not an
        appropriate test when comparing fixed length fields such as phone and
        social security numbers."

    Description:
    strcmp95 distance is 1 - strcmp95 similarity
    """
    return 1 - sim_strcmp95(src, tar, long_strings)


def sim_jaro_winkler(src, tar, qval=1, mode='winkler', long_strings=False, \
                 boost_threshold=0.7, scaling_factor=0.1):
    """Return the Jaro(-Winkler) distance between two string arguments.

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram (defaults to 1: character-wise matching)
    mode -- indicates which variant of this distance metric to compute:
        'winkler' -- computes the Jaro-Winkler distance (default)
            which increases the score for matches near the start of the word
        'jaro' -- computes the Jaro distance

    The following arguments apply only when mode is 'winkler':
    long_strings -- set to True to "Increase the probability of a match when
        the number of matched characters is large.  This option allows for a
        little more tolerance when the strings are large.  It is not an
        appropriate test when comparing fixed length fields such as phone and
        social security numbers."
    boost_threshold -- a value between 0 and 1, below which the Winkler boost
        is not applied (defaults to 0.7)
    scaling_factor -- a value between 0 and 0.25, indicating by how much to
        boost scores for matching prefixes (defaults to 0.1)

    Description:
    This is a Python based on the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    The above file is a US Government publication and, accordingly,
    in the public domain.
    """
    if src == tar:
        return 1.0

    if mode == 'winkler':
        if boost_threshold > 1 or boost_threshold < 0:
            raise ValueError('Unsupported boost_threshold assignment; \
boost_threshold must be between 0 and 1.')
        if scaling_factor > 0.25 or boost_threshold < 0:
            raise ValueError('Unsupported scaling_factor assignment; \
scaling_factor must be between 0 and 0.25.')

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
    src_flag = [0 for i in _range(search_range)]
    tar_flag = [0 for j in _range(search_range)]
    search_range = search_range//2 - 1
    if search_range < 0:
        search_range = 0

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
        if ((long_strings) and (minv > 4) and (num_com > i+1) and
            (2*num_com >= minv+i)):
            weight += (1.0-weight) * ((num_com-i-1) / (lens+lent-i*2+2))

    return weight


def dist_jaro_winkler(src, tar, qval=1, mode='winkler', long_strings=False, \
                 boost_threshold=0.7, scaling_factor=0.1):
    """Return the Jaro(-Winkler) distance between two string arguments.

    Arguments:
    src, tar -- two strings to be compared
    qval -- the length of each q-gram (defaults to 1: character-wise matching)
    mode -- indicates which variant of this distance metric to compute:
        'winkler' -- computes the Jaro-Winkler distance (default)
            which increases the score for matches near the start of the word
        'jaro' -- computes the Jaro distance

    The following arguments apply only when mode is 'winkler':
    long_strings -- set to True to "Increase the probability of a match when
        the number of matched characters is large.  This option allows for a
        little more tolerance when the strings are large.  It is not an
        appropriate test when comparing fixed length fields such as phone and
        social security numbers."
    boost_threshold -- a value between 0 and 1, below which the Winkler boost
        is not applied (defaults to 0.7)
    scaling_factor -- a value between 0 and 0.25, indicating by how much to
        boost scores for matching prefixes (defaults to 0.1)

    Description:
    Jaro-Winkler distance is 1 - the Jaro-Winkler similarity
    """
    return 1 - sim_jaro_winkler(src, tar, qval, mode, long_strings,
                                boost_threshold, scaling_factor)


def lcsseq(src, tar):
    """Returns the longest common subsequence (LCSseq) of two strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
    Based on the dynamic programming algorithm from
    http://rosettacode.org/wiki/Longest_common_subsequence#Dynamic_Programming_6
    This is licensed GFDL 1.2

    Modifications include:
        conversion to a numpy array in place of a list of lists
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
    """Returns the longest common subsequence similarity (sim_{LCSseq}) of two
    strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
    This employs the LCSseq function to derive a similarity metric:
    sim_{LCSseq}(s,t) = |LCSseq(s,t)| / max(|s|, |t|)
    """
    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0
    return len(lcsseq(src, tar)) / max(len(src), len(tar))


def dist_lcsseq(src, tar):
    """Returns the longest common subsequence distance (dist_{LCSseq}) of two
    strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
    This employs the LCSseq function to derive a similarity metric:
    dist_{LCSseq}(s,t) = 1 - sim_{LCSseq}(s,t)
    """
    return 1 - sim_lcsseq(src, tar)


def lcsstr(src, tar):
    """Returns the longest common substring (LCSstr) of the two strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
    Based on the code from
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python
    This is licensed Creative Commons: Attribution-ShareAlike 3.0

    Modifications include:
        conversion to a numpy array in place of a list of lists
        conversion to Python 2/3-safe _range from xrange
    """
    # pylint: disable=no-member
    lengths = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)
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
    """Returns the longest common subsequence similarity (sim_{LCSstr}) of two
    strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
    This employs the LCS function to derive a similarity metric:
    sim_{LCSstr}(s,t) = |LCSstr(s,t)| / max(|s|, |t|)
    """
    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0
    return len(lcsstr(src, tar)) / max(len(src), len(tar))


def dist_lcsstr(src, tar):
    """Returns the longest common substring distance (dist_{LCSstr}) of two
    strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
    This employs the LCS function to derive a similarity metric:
    dist_{LCSstr}(s,t) = 1 - sim_{LCSstr}(s,t)
    """
    return 1 - sim_lcsstr(src, tar)


def sim_ratcliffobershelp(src, tar):
    """Returns the longest common substring distance (dist_{LCSstr}) of two
    strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
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
    """
    def _lcsstr_stl(src, tar):
        """Return the start position in the source string, start position in
        the target string, and length of the longest common substring of
        strings src and tar
        """
        # pylint: disable=no-member
        lengths = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)
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
        2. Recurse on the strings to the left & right of each this substring
           in src & tar.
        3. Base case is a 0 length common substring, in which case, return 0.
        4. Return the sum.
        """
        src_start, tar_start, length = _lcsstr_stl(src, tar)
        if length == 0:
            return 0
        return (_sstr_matches(src[:src_start], tar[:tar_start])
                + length
                + _sstr_matches(src[src_start+length:], tar[tar_start+length:]))

    if src == tar:
        return 1.0
    elif len(src) == 0 or len(tar) == 0:
        return 0.0
    return 2*_sstr_matches(src, tar)/(len(src)+len(tar))


def dist_ratcliffobershelp(src, tar):
    """Returns the longest common substring distance (dist_{LCSstr}) of two
    strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
    Ratcliff-Obsershelp distance is 1 - Ratcliff-Obershelp similarity
    """
    return 1 - sim_ratcliffobershelp(src, tar)


def mra_compare(src, tar):
    """Return the Western Airlines Surname Match Rating Algorithm comparison
    rating between to strings

    Arguments:
    src, tar -- two strings to be compared

    Description:
    A description of the algorithm can be found on page 18 of
    https://archive.org/details/accessingindivid00moor
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


def dist_compression(src, tar, compressor='bz2'):
    """Return the normalized compression distance (NCD) of two strings

    Arguments:
    src, tar -- two strings to be compared
    compressor -- a compression scheme to use for the similarity calculation:
                    'bz2', 'lzma', and 'zlib' are the supported options

    Description:
    Cf.
    https://en.wikipedia.org/wiki/Normalized_compression_distance#Normalized_compression_distance
    """
    if src == tar:
        return 0.0

    src = src.encode('utf-8')
    tar = tar.encode('utf-8')

    if compressor == 'bz2':
        src_comp = codecs.encode(src, 'bz2_codec')[15:]
        tar_comp = codecs.encode(tar, 'bz2_codec')[15:]
        concat_comp = codecs.encode(src+tar, 'bz2_codec')[15:]
    elif compressor == 'lzma':
        if 'lzma' in sys.modules:
            src_comp = lzma.compress(src)[14:]
            tar_comp = lzma.compress(tar)[14:]
            concat_comp = lzma.compress(src+tar)[14:]
        else:
            raise ValueError('Install the lzma module in order to use lzma \
compression similarity')
    else: # zlib
        src_comp = codecs.encode(src, 'zlib_codec')[2:]
        tar_comp = codecs.encode(tar, 'zlib_codec')[2:]
        concat_comp = codecs.encode(src+tar, 'zlib_codec')[2:]
    return ((len(concat_comp) - min(len(src_comp), len(tar_comp))) /
           max(len(src_comp), len(tar_comp)))


def sim_compression(src, tar, compression='bz2'):
    """Return the normalized compression similarity (NCS) of two strings

    Arguments:
    src, tar -- two strings to be compared
    compressor -- a compression scheme to use for the similarity calculation:
                    'bz2', 'lzma', and 'zlib' are the supported options

    Description:
    Normalized compression similarity is equal to 1 - the normalized
    compression distance
    """
    return 1 - dist_compression(src, tar, compression)


def sim_monge_elkan(src, tar, sim_func=sim_levenshtein, sym=False):
    """Return the Monge-Elkan similarity of two strings

    Arguments:
    src, tar -- two strings to be compared
    sim_func -- the internal similarity metric to emply
    sym -- return a symmetric similarity measure

    Description:
    Monge-Elkan is defined in:
    Monge, Alvaro E. and Charles P. Elkan. 1996. "The field matching problem:
    Algorithms and applications." KDD-9 Proceedings.
    http://www.aaai.org/Papers/KDD/1996/KDD96-044.pdf

    Note: Monge-Elkan is NOT a symmetric similarity algoritm. Thus, the
    similarity of src to tar is not necessarily equal to the similarity of
    tar to src. If the sym argument is True, a symmetric value is calculated,
    at the cost of doubling the computation time (since the sim(src, tar) and
    sim(tar, src) are both calculated and then averaged).
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

    if sym:
        sim_em = (sim_em + sim_monge_elkan(tar, src, sim, False))/2

    return sim_em


def dist_monge_elkan(src, tar, sim_func=sim_levenshtein, sym=False):
    """Return the Monge-Elkan distance between two strings

    Arguments:
    src, tar -- two strings to be compared
    sim_func -- the internal similarity metric to emply
    sym -- return a symmetric similarity measure

    Description:
    Monge-Elkan is defined in:
    Monge, Alvaro E. and Charles P. Elkan. 1996. "The field matching problem:
    Algorithms and applications." KDD-9 Proceedings.
    http://www.aaai.org/Papers/KDD/1996/KDD96-044.pdf

    Note: Monge-Elkan is NOT a symmetric similarity algoritm. Thus, the
    distance between src and tar is not necessarily equal to the distance
    between tar and src. If the sym argument is True, a symmetric value is
    calculated, at the cost of doubling the computation time (since the sim(src,
    tar) and sim(tar, src) are both calculated and then averaged).
    """
    return 1 - sim_monge_elkan(src, tar, sim_func, sym)


def sim_ident(src, tar):
    """Return the identity similarity of two strings

    Arguments:
    src, tar -- two strings to be compared

    This is 1 if the two strings are identical, otherwise 0.
    """
    return float(src == tar)


def dist_ident(src, tar):
    """Return the identity similarity of two strings:

    Arguments:
    src, tar -- two strings to be compared

    This is 0 if the two strings are identical, otherwise 1, i.e.
    1 - the identity similarity.
    """
    return 1 - sim_ident(src, tar)


def sim_matrix(src, tar, mat={}, mismatch_cost=0, match_cost=1,  symmetric=True,
               alphabet=None):
    """Return the similarity of two strings, defined by a similarity matrix

    Arguments:
    src, tar -- two strings to be compared
    mat -- a dict mapping tuples to costs; the tuples are (src, tar) pairs
            of symbols from the alphabet parameter
    mismatch_cost -- the value returned if (src, tar) is absent from mat when
                    src does not equal tar
    match_cost -- the value returned if (src, tar) is absent from mat when
                    src equals tar
    symmetric -- True if the cost of src not matching tar is identical to
                    the cost of tar not matching src; in this case, the values
                    in mat need only contain (src, tar) or (tar, src), not both
    alphabet -- a collection of tokens from which src and tar are drawn; if
                this is defined a ValueError is raised if either tar or src
                is not found in alphabet

    Description:
    With the default parameters, this is identical to sim_ident.
    It is possible for sim_matrix to return values outside of the range [0,1],
    if values outside that range are present in mat, mismatch_cost, or
    match_cost.
    """
    if alphabet:
        alphabet = tuple(alphabet)
        if src not in alphabet:
            raise ValueError('src value not in alphabet')
        elif tar not in alphabet:
            raise ValueError('tar value not in alphabet')

    if src == tar:
        if (src, src) in mat:
            return mat[(src, src)]
        else:
            return match_cost
    else:
        if (src, tar) in mat:
            return mat[(src, tar)]
        elif symmetric and (tar, src) in mat:
            return mat[(tar, src)]
        else:
            return mismatch_cost


def needleman_wunsch(src, tar, gap_cost=-1, sim_func=sim_ident):
    """Return the Needleman-Wunsch score of two strings

    Arguments:
    src, tar -- two strings to be compared
    gap_cost -- the cost of an alignment gap (5 by default)
    sim_func -- a function that returns the similarity of two characters
                (identity similarity by default)

    Description:
    This is the standard edit distance measure. Cf.
    https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
    http://csb.stanford.edu/class/public/readings/Bioinformatics_I_Lecture6/Needleman_Wunsch_JMB_70_Global_alignment.pdf
    """
    d_mat = np.zeros((len(src)+1, len(tar)+1), dtype=np.int)

    for i in _range(len(src)+1):
        d_mat[i, 0] = i * gap_cost
    for j in _range(len(tar)+1):
        d_mat[0, j] = j * gap_cost
    for i in _range(1,len(src)+1):
        for j in _range(1,len(tar)+1):
            match = d_mat[i-1, j-1] + sim_func(src[i-1], tar[j-1])
            delete = d_mat[i-1, j] + gap_cost
            insert = d_mat[i, j-1] + gap_cost
            d_mat[i, j] = max(match, delete, insert)
    return d_mat[d_mat.shape[0]-1, d_mat.shape[1]-1]


def sim(src, tar, method=sim_levenshtein):
    """Return the similarity of two strings
    This is a generalized function for calling other similarity functions.

    Arguments:
    src, tar -- two strings to be compared
    method -- specifies the similarity metric (levenshtein by default)
    """
    if hasattr(method, '__call__'):
        return method(src, tar)
    else:
        raise AttributeError('Unknown similarity function: ' + str(method))


def dist(src, tar, method=dist_levenshtein):
    """Return the distance between two strings
    This is a generalized function for calling other distance functions.

    Arguments:
    src, tar -- two strings to be compared
    method -- specifies the distance metric (levenshtein by default)
    """
    if hasattr(method, '__call__'):
        return method(src, tar)
    else:
        raise AttributeError('Unknown distance function: ' + str(method))
