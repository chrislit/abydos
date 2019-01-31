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

"""abydos.distance._cormode_lz.

Cormode's LZ distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance

__all__ = ['CormodeLZ']


class CormodeLZ(_Distance):
    r"""Cormode's LZ distance.

    Cormode's LZ distance :cite:`Cormode:2000,Cormode:2003`

    .. versionadded:: 0.4.0
    """

    def __init__(self, **kwargs):
        """Initialize CormodeLZ instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(CormodeLZ, self).__init__(**kwargs)

    def dist_abs(self, src, tar):
        """Return the Cormode's LZ distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Cormode's LZ distance

        Examples
        --------
        >>> cmp = CormodeLZ()
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
        edits = 0
        pos = 0
        span = 1

        while max(pos + 1, pos + span) <= len(src):
            if (src[pos : pos + span] in tar) or (
                src[pos : pos + span] in src[:pos]
            ):
                span += 1
            else:
                edits += 1
                pos += max(1, span - 1)
                span = 1

        return 1 + edits

    def dist(self, src, tar):
        """Return the normalized Cormode's LZ distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Cormode's LZ distance

        Examples
        --------
        >>> cmp = CormodeLZ()
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
        return (self.dist_abs(src, tar) - 1) / (len(src) - 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
