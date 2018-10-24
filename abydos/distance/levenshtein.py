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

"""abydos.distance.levenshtein.

The distance.levenshtein module implements string edit distance functions
based on Levenshtein distance, including:

    - Levenshtein distance
    - Optimal String Alignment distance
    - Levenshtein-Damerau distance
    - Indel distance
"""

from __future__ import division, unicode_literals

from sys import maxsize

from numpy import int as np_int
from numpy import zeros as np_zeros

from six.moves import range


__all__ = [
    'damerau_levenshtein',
    'dist_damerau',
    'dist_indel',
    'dist_levenshtein',
    'levenshtein',
    'sim_damerau',
    'sim_indel',
    'sim_levenshtein',
]


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

    d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
    for i in range(len(src) + 1):
        d_mat[i, 0] = i * del_cost
    for j in range(len(tar) + 1):
        d_mat[0, j] = j * ins_cost

    for i in range(len(src)):
        for j in range(len(tar)):
            d_mat[i + 1, j + 1] = min(
                d_mat[i + 1, j] + ins_cost,  # ins
                d_mat[i, j + 1] + del_cost,  # del
                d_mat[i, j] + (sub_cost if src[i] != tar[j] else 0),  # sub/==
            )

            if mode == 'osa':
                if (
                    i + 1 > 1
                    and j + 1 > 1
                    and src[i] == tar[j - 1]
                    and src[i - 1] == tar[j]
                ):
                    # transposition
                    d_mat[i + 1, j + 1] = min(
                        d_mat[i + 1, j + 1], d_mat[i - 1, j - 1] + trans_cost
                    )

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
    return levenshtein(src, tar, mode, cost) / (
        max(len(src) * del_cost, len(tar) * ins_cost)
    )


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

    if 2 * trans_cost < ins_cost + del_cost:
        raise ValueError(
            'Unsupported cost assignment; the cost of two '
            + 'transpositions must not be less than the cost of '
            + 'an insert plus a delete.'
        )

    d_mat = np_zeros((len(src)) * (len(tar)), dtype=np_int).reshape(
        (len(src), len(tar))
    )

    if src[0] != tar[0]:
        d_mat[0, 0] = min(sub_cost, ins_cost + del_cost)

    src_index_by_character = {src[0]: 0}
    for i in range(1, len(src)):
        del_distance = d_mat[i - 1, 0] + del_cost
        ins_distance = (i + 1) * del_cost + ins_cost
        match_distance = i * del_cost + (0 if src[i] == tar[0] else sub_cost)
        d_mat[i, 0] = min(del_distance, ins_distance, match_distance)

    for j in range(1, len(tar)):
        del_distance = (j + 1) * ins_cost + del_cost
        ins_distance = d_mat[0, j - 1] + ins_cost
        match_distance = j * ins_cost + (0 if src[0] == tar[j] else sub_cost)
        d_mat[0, j] = min(del_distance, ins_distance, match_distance)

    for i in range(1, len(src)):
        max_src_letter_match_index = 0 if src[i] == tar[0] else -1
        for j in range(1, len(tar)):
            candidate_swap_index = (
                -1
                if tar[j] not in src_index_by_character
                else src_index_by_character[tar[j]]
            )
            j_swap = max_src_letter_match_index
            del_distance = d_mat[i - 1, j] + del_cost
            ins_distance = d_mat[i, j - 1] + ins_cost
            match_distance = d_mat[i - 1, j - 1]
            if src[i] != tar[j]:
                match_distance += sub_cost
            else:
                max_src_letter_match_index = j

            if candidate_swap_index != -1 and j_swap != -1:
                i_swap = candidate_swap_index

                if i_swap == 0 and j_swap == 0:
                    pre_swap_cost = 0
                else:
                    pre_swap_cost = d_mat[
                        max(0, i_swap - 1), max(0, j_swap - 1)
                    ]
                swap_distance = (
                    pre_swap_cost
                    + (i - i_swap - 1) * del_cost
                    + (j - j_swap - 1) * ins_cost
                    + trans_cost
                )
            else:
                swap_distance = maxsize

            d_mat[i, j] = min(
                del_distance, ins_distance, match_distance, swap_distance
            )
        src_index_by_character[src[i]] = i

    return d_mat[len(src) - 1, len(tar) - 1]


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
    return damerau_levenshtein(src, tar, cost) / (
        max(len(src) * del_cost, len(tar) * ins_cost)
    )


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


def indel(src, tar):
    """Return the indel distance between two strings.

    This is equivalent to Levenshtein distance, when only inserts and deletes
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
    return levenshtein(src, tar, mode='lev', cost=(1, 1, 9999, 9999))


def dist_indel(src, tar):
    """Return the normalized indel distance between two strings.

    This is equivalent to normalized Levenshtein distance, when only inserts
    and deletes are possible.

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
    return indel(src, tar) / (len(src) + len(tar))


def sim_indel(src, tar):
    """Return the normalized indel similarity of two strings.

    This is equivalent to normalized Levenshtein similarity, when only inserts
    and deletes are possible.

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
    return 1 - dist_indel(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
