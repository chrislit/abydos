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

"""abydos.distance._prefix.

Prefix similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six.moves import range

from ._distance import _Distance

__all__ = ['Prefix', 'dist_prefix', 'sim_prefix']


class Prefix(_Distance):
    """Prefix similiarity and distance."""

    def sim(self, src, tar):
        """Return the prefix similarity of two strings.

        Prefix similarity is the ratio of the length of the shorter term that
        exactly matches the longer term to the length of the shorter term,
        beginning at the start of both terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Prefix similarity

        Examples
        --------
        >>> cmp = Prefix()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.25
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
        min_len = len(min_word)
        for i in range(min_len, 0, -1):
            if min_word[:i] == max_word[:i]:
                return i / min_len
        return 0.0


def sim_prefix(src, tar):
    """Return the prefix similarity of two strings.

    This is a wrapper for :py:meth:`Prefix.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Prefix similarity

    Examples
    --------
    >>> sim_prefix('cat', 'hat')
    0.0
    >>> sim_prefix('Niall', 'Neil')
    0.25
    >>> sim_prefix('aluminum', 'Catalan')
    0.0
    >>> sim_prefix('ATCG', 'TAGC')
    0.0

    """
    return Prefix().sim(src, tar)


def dist_prefix(src, tar):
    """Return the prefix distance between two strings.

    This is a wrapper for :py:meth:`Prefix.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Prefix distance

    Examples
    --------
    >>> dist_prefix('cat', 'hat')
    1.0
    >>> dist_prefix('Niall', 'Neil')
    0.75
    >>> dist_prefix('aluminum', 'Catalan')
    1.0
    >>> dist_prefix('ATCG', 'TAGC')
    1.0

    """
    return Prefix().dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
