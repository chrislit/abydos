# Copyright 2019-2020 by Christopher C. Little.
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
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        5
        >>> cmp.dist_abs('aluminum', 'Catalan')
        6
        >>> cmp.dist_abs('ATCG', 'TAGC')
        4


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
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.8
        >>> cmp.dist('aluminum', 'Catalan')
        0.625
        >>> cmp.dist('ATCG', 'TAGC')
        0.75


        .. versionadded:: 0.4.0

        """
        num = self.dist_abs(src, tar) - 1
        if num == 0:
            return 0.0
        return num / len(src)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
