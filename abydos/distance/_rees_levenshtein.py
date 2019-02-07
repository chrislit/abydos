# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._rees_levenshtein.

Rees-Levenshtein distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from numpy import float as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['ReesLevenshtein']


class ReesLevenshtein(_Distance):
    r"""Rees-Levenshtein distance.

    Rees-Levenshtein distance :cite:`CITATION`

    .. versionadded:: 0.4.0
    """

    def __init__(self, normalizer=max, **kwargs):
        """Initialize ReesLevenshtein instance.

        Parameters
        ----------
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(ReesLevenshtein, self).__init__(**kwargs)
        self._normalizer = normalizer

    def dist_abs(self, p_str1, p_str2, p_block_limit=2):
        """Return the Rees-Levenshtein distance of two strings.

        This is a straightforward port of the PL/SQL implementation at
        https://confluence.csiro.au/public/taxamatch/the-mdld-modified-damerau-levenshtein-distance-algorithm

        Parameters
        ----------
        p_str1 : str
            Source string for comparison
        p_str2 : str
            Target string for comparison
        p_block_limit : int
            The block length limit

        Returns
        -------
        float
            Rees-Levenshtein distance

        Examples
        --------
        >>> cmp = ReesLevenshtein()
        >>> cmp.dist_abs('cat', 'hat')
        0.0
        >>> cmp.dist_abs('Niall', 'Neil')
        0.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        v_str1_length = len(p_str1)
        v_str2_length = len(p_str2)

        if p_str2 == p_str1:
            return 0
        if not p_str1:
            return len(p_str2)
        if not p_str2:
            return len(p_str1)
        if v_str1_length == 1 and v_str2_length == 1:
            return 1

        v_temp_str1 = str(p_str1)
        v_temp_str2 = str(p_str2)

        # first trim common leading characters
        while v_temp_str1[:1] == v_temp_str2[:1]:
            v_temp_str1 = v_temp_str1[1:]
            v_temp_str2 = v_temp_str2[1:]

        # then trim common trailing characters
        while v_temp_str1[-1:] == v_temp_str2[-1:]:
            v_temp_str1 = v_temp_str1[:-1]
            v_temp_str2 = v_temp_str2[:-1]

        v_str1_length = len(v_temp_str1)
        v_str2_length = len(v_temp_str2)

        # then calculate standard Levenshtein Distance
        if v_str1_length == 0 or v_str2_length == 0:
            return max(v_str2_length, v_str1_length)
        if v_str1_length == 1 and v_str2_length == 1:
            return 1

        # create table (NB: this is transposed relative to the PL/SQL version)
        d_mat = np_zeros(
            (v_str1_length + 1, v_str2_length + 1), dtype=np_float
        )

        # enter values in first (leftmost) column
        for i in range(1, v_str1_length + 1):
            d_mat[i, 0] = i
        # populate remaining columns
        for j in range(1, v_str2_length + 1):
            d_mat[0, j] = j

            for i in range(1, v_str1_length + 1):
                if v_temp_str1[i] == v_temp_str2[j]:
                    v_this_cost = 0
                else:
                    v_this_cost = 1

                # extension to cover multiple single, double, triple, etc.
                # character transpositions
                # that includes calculation of original Levenshtein distance
                # when no transposition found
                v_temp_block_length = min(
                    v_str1_length / 2, v_str2_length / 2, p_block_limit
                )
                while v_temp_block_length >= 1:
                    if (
                        i >= v_temp_block_length * 2
                        and j >= v_temp_block_length * 2
                        and v_temp_str1[
                            i
                            - v_temp_block_length * 2
                            - 1 : i
                            - v_temp_block_length * 2
                            - 1
                            + v_temp_block_length
                        ]
                        == v_temp_str2[
                            j
                            - v_temp_block_length
                            - 1 : j
                            - v_temp_block_length
                            - 1
                            + v_temp_block_length
                        ]
                        and v_temp_str1[
                            i
                            - v_temp_block_length
                            - 1 : i
                            - v_temp_block_length
                            - 1
                            + v_temp_block_length
                        ]
                        == v_temp_str2[
                            j
                            - v_temp_block_length * 2
                            - 1 : j
                            - v_temp_block_length * 2
                            - 1
                            + v_temp_block_length
                        ]
                    ):
                        # transposition found
                        d_mat[i, j] = min(
                            d_mat[i, j - 1] + 1,
                            d_mat[i - 1, j] + 1,
                            d_mat[
                                i - v_temp_block_length * 2,
                                j - v_temp_block_length * 2,
                            ]
                            + v_this_cost
                            + v_temp_block_length
                            - 1,
                        )
                        v_temp_block_length = 0
                    elif v_temp_block_length == 1:
                        # no transposition
                        d_mat[i, j] = min(
                            d_mat[i, j - 1] + 1,
                            d_mat[i - 1, j] + 1,
                            d_mat[i - 1, j - 1] + v_this_cost,
                        )
                    v_temp_block_length -= 1
        return d_mat[v_str1_length, v_str2_length]

    def dist(self, src, tar):
        """Return the normalized Rees-Levenshtein distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Rees-Levenshtein distance

        Examples
        --------
        >>> cmp = ReesLevenshtein()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0
        return self.dist_abs(src, tar) / (
            self._normalizer([len(src), len(tar)])
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
