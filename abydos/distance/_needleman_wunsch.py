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

"""abydos.distance._needleman_wunsch.

Needleman-Wunsch score
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from numpy import float32 as np_float32
from numpy import zeros as np_zeros

from six.moves import range

from ._distance import _Distance
from ._ident import sim_ident

__all__ = ['NeedlemanWunsch', 'needleman_wunsch']


class NeedlemanWunsch(_Distance):
    """Needleman-Wunsch score.

    The Needleman-Wunsch score :cite:`Needleman:1970` is a standard edit
    distance measure.
    """

    @staticmethod
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

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        mat : dict
            A dict mapping tuples to costs; the tuples are (src, tar) pairs of
            symbols from the alphabet parameter
        mismatch_cost : float
            The value returned if (src, tar) is absent from mat when src does
            not equal tar
        match_cost : float
            The value returned if (src, tar) is absent from mat when src equals
            tar
        symmetric : bool
            True if the cost of src not matching tar is identical to the cost
            of tar not matching src; in this case, the values in mat need only
            contain (src, tar) or (tar, src), not both
        alphabet : str
            A collection of tokens from which src and tar are drawn; if this is
            defined a ValueError is raised if either tar or src is not found in
            alphabet

        Returns
        -------
        float
            Matrix similarity

        Raises
        ------
        ValueError
            src value not in alphabet
        ValueError
            tar value not in alphabet

        Examples
        --------
        >>> NeedlemanWunsch.sim_matrix('cat', 'hat')
        0
        >>> NeedlemanWunsch.sim_matrix('hat', 'hat')
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

    def dist_abs(self, src, tar, gap_cost=1, sim_func=sim_ident):
        """Return the Needleman-Wunsch score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        gap_cost : float
            The cost of an alignment gap (1 by default)
        sim_func : function
            A function that returns the similarity of two characters (identity
            similarity by default)

        Returns
        -------
        float
            Needleman-Wunsch score

        Examples
        --------
        >>> cmp = NeedlemanWunsch()
        >>> cmp.dist_abs('cat', 'hat')
        2.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        -1.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
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


def needleman_wunsch(src, tar, gap_cost=1, sim_func=sim_ident):
    """Return the Needleman-Wunsch score of two strings.

    This is a wrapper for :py:meth:`NeedlemanWunsch.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    gap_cost : float
        The cost of an alignment gap (1 by default)
    sim_func : function
        A function that returns the similarity of two characters (identity
        similarity by default)

    Returns
    -------
    float
        Needleman-Wunsch score

    Examples
    --------
    >>> needleman_wunsch('cat', 'hat')
    2.0
    >>> needleman_wunsch('Niall', 'Neil')
    1.0
    >>> needleman_wunsch('aluminum', 'Catalan')
    -1.0
    >>> needleman_wunsch('ATCG', 'TAGC')
    0.0

    """
    return NeedlemanWunsch().dist_abs(src, tar, gap_cost, sim_func)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
