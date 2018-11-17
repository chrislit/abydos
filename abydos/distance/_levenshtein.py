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

"""abydos.distance._levenshtein.

The distance._Levenshtein module implements string edit distance functions
based on Levenshtein distance, including:

    - Levenshtein distance
    - Optimal String Alignment distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


from numpy import int as np_int
from numpy import zeros as np_zeros

from six.moves import range

from ._distance import _Distance

__all__ = ['Levenshtein', 'dist_levenshtein', 'levenshtein', 'sim_levenshtein']


class Levenshtein(_Distance):
    """Levenshtein distance.

    This is the standard edit distance measure. Cf.
    :cite:`Levenshtein:1965,Levenshtein:1966`.

    Optimal string alignment (aka restricted
    Damerau-Levenshtein distance) :cite:`Boytsov:2011` is also supported.

    The ordinary Levenshtein & Optimal String Alignment distance both
    employ the Wagner-Fischer dynamic programming algorithm
    :cite:`Wagner:1974`.

    Levenshtein edit distance ordinarily has unit insertion, deletion, and
    substitution costs.
    """

    def dist_abs(self, src, tar, mode='lev', cost=(1, 1, 1, 1)):
        """Return the Levenshtein distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        mode : str
            Specifies a mode for computing the Levenshtein distance:

                - ``lev`` (default) computes the ordinary Levenshtein distance,
                  in which edits may include inserts, deletes, and
                  substitutions
                - ``osa`` computes the Optimal String Alignment distance, in
                  which edits may include inserts, deletes, substitutions, and
                  transpositions but substrings may only be edited once

        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and transpositions, respectively
            (by default: (1, 1, 1, 1))

        Returns
        -------
        int (may return a float if cost has float values)
            The Levenshtein distance between src & tar

        Examples
        --------
        >>> cmp = Levenshtein()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        3

        >>> cmp.dist_abs('ATCG', 'TAGC', mode='osa')
        2
        >>> cmp.dist_abs('ACTG', 'TAGC', mode='osa')
        4

        """
        ins_cost, del_cost, sub_cost, trans_cost = cost

        if src == tar:
            return 0
        if not src:
            return len(tar) * ins_cost
        if not tar:
            return len(src) * del_cost

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
                    d_mat[i, j]
                    + (sub_cost if src[i] != tar[j] else 0),  # sub/==
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
                            d_mat[i + 1, j + 1],
                            d_mat[i - 1, j - 1] + trans_cost,
                        )

        return d_mat[len(src), len(tar)]

    def dist(self, src, tar, mode='lev', cost=(1, 1, 1, 1)):
        """Return the normalized Levenshtein distance between two strings.

        The Levenshtein distance is normalized by dividing the Levenshtein
        distance (calculated by any of the three supported methods) by the
        greater of the number of characters in src times the cost of a delete
        and the number of characters in tar times the cost of an insert.
        For the case in which all operations have :math:`cost = 1`, this is
        equivalent to the greater of the length of the two strings src & tar.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        mode : str
            Specifies a mode for computing the Levenshtein distance:

                - ``lev`` (default) computes the ordinary Levenshtein distance,
                  in which edits may include inserts, deletes, and
                  substitutions
                - ``osa`` computes the Optimal String Alignment distance, in
                  which edits may include inserts, deletes, substitutions, and
                  transpositions but substrings may only be edited once

        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and transpositions, respectively
            (by default: (1, 1, 1, 1))

        Returns
        -------
        float
            The normalized Levenshtein distance between src & tar

        Examples
        --------
        >>> cmp = Levenshtein()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.6
        >>> cmp.dist('aluminum', 'Catalan')
        0.875
        >>> cmp.dist('ATCG', 'TAGC')
        0.75

        """
        if src == tar:
            return 0
        ins_cost, del_cost = cost[:2]
        return levenshtein(src, tar, mode, cost) / (
            max(len(src) * del_cost, len(tar) * ins_cost)
        )


def levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein distance between two strings.

    This is a wrapper of :py:meth:`Levenshtein.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    mode : str
        Specifies a mode for computing the Levenshtein distance:

            - ``lev`` (default) computes the ordinary Levenshtein distance, in
              which edits may include inserts, deletes, and substitutions
            - ``osa`` computes the Optimal String Alignment distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions but substrings may only be edited once

    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    int (may return a float if cost has float values)
        The Levenshtein distance between src & tar

    Examples
    --------
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

    """
    return Levenshtein().dist_abs(src, tar, mode, cost)


def dist_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the normalized Levenshtein distance between two strings.

    This is a wrapper of :py:meth:`Levenshtein.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    mode : str
        Specifies a mode for computing the Levenshtein distance:

            - ``lev`` (default) computes the ordinary Levenshtein distance, in
              which edits may include inserts, deletes, and substitutions
            - ``osa`` computes the Optimal String Alignment distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions but substrings may only be edited once

    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    float
        The Levenshtein distance between src & tar

    Examples
    --------
    >>> round(dist_levenshtein('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_levenshtein('Niall', 'Neil'), 12)
    0.6
    >>> dist_levenshtein('aluminum', 'Catalan')
    0.875
    >>> dist_levenshtein('ATCG', 'TAGC')
    0.75

    """
    return Levenshtein().dist(src, tar, mode, cost)


def sim_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein similarity of two strings.

    This is a wrapper of :py:meth:`Levenshtein.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    mode : str
        Specifies a mode for computing the Levenshtein distance:

            - ``lev`` (default) computes the ordinary Levenshtein distance, in
              which edits may include inserts, deletes, and substitutions
            - ``osa`` computes the Optimal String Alignment distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions but substrings may only be edited once

    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    float
        The Levenshtein similarity between src & tar

    Examples
    --------
    >>> round(sim_levenshtein('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_levenshtein('Niall', 'Neil'), 12)
    0.4
    >>> sim_levenshtein('aluminum', 'Catalan')
    0.125
    >>> sim_levenshtein('ATCG', 'TAGC')
    0.25

    """
    return Levenshtein().sim(src, tar, mode, cost)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
