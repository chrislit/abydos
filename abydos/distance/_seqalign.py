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

"""abydos.distance.seqalign.

The distance.seqalign module implements string edit distance functions
used in sequence alignment:

    - Matrix similarity
    - Needleman-Wunsch score
    - Smith-Waterman score
    - Gotoh score
"""

from __future__ import unicode_literals

from numpy import float32 as np_float32
from numpy import zeros as np_zeros

from six.moves import range

from ._basic import sim_ident

__all__ = ['gotoh', 'needleman_wunsch', 'sim_matrix', 'smith_waterman']


def sim_matrix(
    src,
    tar,
    mat=None,
    mismatch_cost=0,
    match_cost=1,
    symmetric=True,
    alphabet=None,
):
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
    d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)

    for i in range(len(src) + 1):
        d_mat[i, 0] = -(i * gap_cost)
    for j in range(len(tar) + 1):
        d_mat[0, j] = -(j * gap_cost)
    for i in range(1, len(src) + 1):
        for j in range(1, len(tar) + 1):
            match = d_mat[i - 1, j - 1] + sim_func(src[i - 1], tar[j - 1])
            delete = d_mat[i - 1, j] - gap_cost
            insert = d_mat[i, j - 1] - gap_cost
            d_mat[i, j] = max(match, delete, insert)
    return d_mat[d_mat.shape[0] - 1, d_mat.shape[1] - 1]


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
    d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)

    for i in range(len(src) + 1):
        d_mat[i, 0] = 0
    for j in range(len(tar) + 1):
        d_mat[0, j] = 0
    for i in range(1, len(src) + 1):
        for j in range(1, len(tar) + 1):
            match = d_mat[i - 1, j - 1] + sim_func(src[i - 1], tar[j - 1])
            delete = d_mat[i - 1, j] - gap_cost
            insert = d_mat[i, j - 1] - gap_cost
            d_mat[i, j] = max(0, match, delete, insert)
    return d_mat[d_mat.shape[0] - 1, d_mat.shape[1] - 1]


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
    d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)
    p_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)
    q_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)

    d_mat[0, 0] = 0
    p_mat[0, 0] = float('-inf')
    q_mat[0, 0] = float('-inf')
    for i in range(1, len(src) + 1):
        d_mat[i, 0] = float('-inf')
        p_mat[i, 0] = -gap_open - gap_ext * (i - 1)
        q_mat[i, 0] = float('-inf')
        q_mat[i, 1] = -gap_open
    for j in range(1, len(tar) + 1):
        d_mat[0, j] = float('-inf')
        p_mat[0, j] = float('-inf')
        p_mat[1, j] = -gap_open
        q_mat[0, j] = -gap_open - gap_ext * (j - 1)

    for i in range(1, len(src) + 1):
        for j in range(1, len(tar) + 1):
            sim_val = sim_func(src[i - 1], tar[j - 1])
            d_mat[i, j] = max(
                d_mat[i - 1, j - 1] + sim_val,
                p_mat[i - 1, j - 1] + sim_val,
                q_mat[i - 1, j - 1] + sim_val,
            )

            p_mat[i, j] = max(
                d_mat[i - 1, j] - gap_open, p_mat[i - 1, j] - gap_ext
            )

            q_mat[i, j] = max(
                d_mat[i, j - 1] - gap_open, q_mat[i, j - 1] - gap_ext
            )

    i, j = (n - 1 for n in d_mat.shape)
    return max(d_mat[i, j], p_mat[i, j], q_mat[i, j])


if __name__ == '__main__':
    import doctest

    doctest.testmod()
