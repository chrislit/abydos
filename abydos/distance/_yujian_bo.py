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

"""abydos.distance._yujian_bo.

Yujian-Bo normalized Levenshtein distance
"""

from ._levenshtein import Levenshtein

__all__ = ['YujianBo']


class YujianBo(Levenshtein):
    r"""Yujian-Bo normalized Levenshtein distance.

    Yujian-Bo's normalization of Levenshtein distance :cite:`Yujian:2007`,
    given Levenshtein distance :math:`GLD(X, Y)` between two strings X and Y,
    is

        .. math::

            dist_{N-GLD}(X, Y) =
            \frac{2 \cdot GLD(X, Y)}{|X| + |Y| + GLD(X, Y)}

    .. versionadded:: 0.4.0
    """

    def __init__(self, cost=(1, 1, 1, 1), **kwargs):
        """Initialize YujianBo instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(YujianBo, self).__init__(cost=cost, **kwargs)

    def dist_abs(self, src, tar):
        """Return the Yujian-Bo normalized edit distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The Yujian-Bo normalized edit distance between src & tar

        Examples
        --------
        >>> cmp = YujianBo()
        >>> cmp.dist_abs('cat', 'hat')
        0.2857142857142857
        >>> cmp.dist_abs('Niall', 'Neil')
        0.5
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.6363636363636364
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.5454545454545454


        .. versionadded:: 0.4.0

        """
        return self.dist(src, tar)

    def dist(self, src, tar):
        """Return the Yujian-Bo normalized edit distance between strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The Yujian-Bo normalized edit distance between src & tar

        Examples
        --------
        >>> cmp = YujianBo()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.285714285714
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.5
        >>> cmp.dist('aluminum', 'Catalan')
        0.6363636363636364
        >>> cmp.dist('ATCG', 'TAGC')
        0.5454545454545454


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        ins_cost, del_cost = self._cost[:2]
        gld = super(YujianBo, self).dist_abs(src, tar)
        return 2 * gld / (len(src) * del_cost + len(tar) * ins_cost + gld)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
