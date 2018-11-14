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

"""abydos.distance._smith_waterman.

Smith-Waterman score
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

from ._ident import sim_ident
from ._needleman_wunsch import NeedlemanWunsch

__all__ = ['SmithWaterman', 'smith_waterman']


class SmithWaterman(NeedlemanWunsch):
    """Smith-Waterman score.

    The Smith-Waterman score :cite:`Smith:1981` is a standard edit distance
    measure, differing from Needleman-Wunsch in that it focuses on local
    alignment and disallows negative scores.
    """

    def dist_abs(self, src, tar, gap_cost=1, sim_func=sim_ident):
        """Return the Smith-Waterman score of two strings.

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
            Smith-Waterman score

        Examples
        --------
        >>> cmp = SmithWaterman()
        >>> cmp.dist_abs('cat', 'hat')
        2.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
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


def smith_waterman(src, tar, gap_cost=1, sim_func=sim_ident):
    """Return the Smith-Waterman score of two strings.

    This is a wrapper for :py:meth:`SmithWaterman.dist_abs`.

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
        Smith-Waterman score

    Examples
    --------
    >>> smith_waterman('cat', 'hat')
    2.0
    >>> smith_waterman('Niall', 'Neil')
    1.0
    >>> smith_waterman('aluminum', 'Catalan')
    0.0
    >>> smith_waterman('ATCG', 'TAGC')
    1.0

    """
    return SmithWaterman().dist_abs(src, tar, gap_cost, sim_func)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
