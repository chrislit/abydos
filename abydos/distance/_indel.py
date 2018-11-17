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

"""abydos.distance._indel.

Indel distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance
from ._levenshtein import Levenshtein

__all__ = ['Indel', 'dist_indel', 'indel', 'sim_indel']


class Indel(_Distance):
    """Indel distance.

    This is equivalent to Levenshtein distance, when only inserts and deletes
    are possible.
    """

    _lev = Levenshtein()

    def dist_abs(self, src, tar):
        """Return the indel distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            Indel distance

        Examples
        --------
        >>> cmp = Indel()
        >>> cmp.dist_abs('cat', 'hat')
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('Colin', 'Cuilen')
        5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        4

        """
        return self._lev.dist_abs(
            src, tar, mode='lev', cost=(1, 1, 9999, 9999)
        )

    def dist(self, src, tar):
        """Return the normalized indel distance between two strings.

        This is equivalent to normalized Levenshtein distance, when only
        inserts and deletes are possible.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized indel distance

        Examples
        --------
        >>> cmp = Indel()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.333333333333
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.454545454545
        >>> cmp.dist('ATCG', 'TAGC')
        0.5

        """
        if src == tar:
            return 0.0
        return self.dist_abs(src, tar) / (len(src) + len(tar))


def indel(src, tar):
    """Return the indel distance between two strings.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    int
        Indel distance

    Examples
    --------
    >>> indel('cat', 'hat')
    2
    >>> indel('Niall', 'Neil')
    3
    >>> indel('Colin', 'Cuilen')
    5
    >>> indel('ATCG', 'TAGC')
    4

    """
    return Indel().dist_abs(src, tar)


def dist_indel(src, tar):
    """Return the normalized indel distance between two strings.

    This is equivalent to normalized Levenshtein distance, when only inserts
    and deletes are possible.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Normalized indel distance

    Examples
    --------
    >>> round(dist_indel('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_indel('Niall', 'Neil'), 12)
    0.333333333333
    >>> round(dist_indel('Colin', 'Cuilen'), 12)
    0.454545454545
    >>> dist_indel('ATCG', 'TAGC')
    0.5

    """
    return Indel().dist(src, tar)


def sim_indel(src, tar):
    """Return the normalized indel similarity of two strings.

    This is equivalent to normalized Levenshtein similarity, when only inserts
    and deletes are possible.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Normalized indel similarity

    Examples
    --------
    >>> round(sim_indel('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_indel('Niall', 'Neil'), 12)
    0.666666666667
    >>> round(sim_indel('Colin', 'Cuilen'), 12)
    0.545454545455
    >>> sim_indel('ATCG', 'TAGC')
    0.5

    """
    return Indel().sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
