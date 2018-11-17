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

"""abydos.distance._gotoh.

Gotoh score
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

__all__ = ['Gotoh', 'gotoh']


class Gotoh(NeedlemanWunsch):
    """Gotoh score.

    The Gotoh score :cite:`Gotoh:1982` is essentially Needleman-Wunsch with
    affine gap penalties.
    """

    def dist_abs(self, src, tar, gap_open=1, gap_ext=0.4, sim_func=sim_ident):
        """Return the Gotoh score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        gap_open : float
            The cost of an open alignment gap (1 by default)
        gap_ext : float
            The cost of an alignment gap extension (0.4 by default)
        sim_func : function
            A function that returns the similarity of two characters (identity
            similarity by default)

        Returns
        -------
        float
            Gotoh score

        Examples
        --------
        >>> cmp = Gotoh()
        >>> cmp.dist_abs('cat', 'hat')
        2.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.0
        >>> round(cmp.dist_abs('aluminum', 'Catalan'), 12)
        -0.4
        >>> cmp.dist_abs('cat', 'hat')
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


def gotoh(src, tar, gap_open=1, gap_ext=0.4, sim_func=sim_ident):
    """Return the Gotoh score of two strings.

    This is a wrapper for :py:meth:`Gotoh.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    gap_open : float
        The cost of an open alignment gap (1 by default)
    gap_ext : float
        The cost of an alignment gap extension (0.4 by default)
    sim_func : function
        A function that returns the similarity of two characters (identity
        similarity by default)

    Returns
    -------
    float
        Gotoh score

    Examples
    --------
    >>> gotoh('cat', 'hat')
    2.0
    >>> gotoh('Niall', 'Neil')
    1.0
    >>> round(gotoh('aluminum', 'Catalan'), 12)
    -0.4
    >>> gotoh('cat', 'hat')
    2.0

    """
    return Gotoh().dist_abs(src, tar, gap_open, gap_ext, sim_func)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
