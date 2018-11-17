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

"""abydos.distance._bag.

Bag similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter

from ._token_distance import _TokenDistance

__all__ = ['Bag', 'bag', 'dist_bag', 'sim_bag']


class Bag(_TokenDistance):
    """Bag distance.

    Bag distance is proposed in :cite:`Bartolini:2002`. It is defined as:
    :math:`max(|multiset(src)-multiset(tar)|, |multiset(tar)-multiset(src)|)`.
    """

    def dist_abs(self, src, tar):
        """Return the bag distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            Bag distance

        Examples
        --------
        >>> cmp = Bag()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('aluminum', 'Catalan')
        5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0
        >>> cmp.dist_abs('abcdefg', 'hijklm')
        7
        >>> cmp.dist_abs('abcdefg', 'hijklmno')
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
        return max(
            sum((src_bag - tar_bag).values()),
            sum((tar_bag - src_bag).values()),
        )

    def dist(self, src, tar):
        """Return the normalized bag distance between two strings.

        Bag distance is normalized by dividing by :math:`max( |src|, |tar| )`.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized bag distance

        Examples
        --------
        >>> cmp = Bag()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.4
        >>> cmp.dist('aluminum', 'Catalan')
        0.625
        >>> cmp.dist('ATCG', 'TAGC')
        0.0

        """
        if tar == src:
            return 0.0
        if not src or not tar:
            return 1.0

        max_length = max(len(src), len(tar))

        return self.dist_abs(src, tar) / max_length


def bag(src, tar):
    """Return the bag distance between two strings.

    This is a wrapper for :py:meth:`Bag.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    int
        Bag distance

    Examples
    --------
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
    return Bag().dist_abs(src, tar)


def dist_bag(src, tar):
    """Return the normalized bag distance between two strings.

    This is a wrapper for :py:meth:`Bag.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Normalized bag distance

    Examples
    --------
    >>> dist_bag('cat', 'hat')
    0.3333333333333333
    >>> dist_bag('Niall', 'Neil')
    0.4
    >>> dist_bag('aluminum', 'Catalan')
    0.625
    >>> dist_bag('ATCG', 'TAGC')
    0.0

    """
    return Bag().dist(src, tar)


def sim_bag(src, tar):
    """Return the normalized bag similarity of two strings.

    This is a wrapper for :py:meth:`Bag.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Normalized bag similarity

    Examples
    --------
    >>> round(sim_bag('cat', 'hat'), 12)
    0.666666666667
    >>> sim_bag('Niall', 'Neil')
    0.6
    >>> sim_bag('aluminum', 'Catalan')
    0.375
    >>> sim_bag('ATCG', 'TAGC')
    1.0

    """
    return Bag().sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
