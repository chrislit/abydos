# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.distance._mra.

The Match Rating Algorithm's distance measure
"""

from ._distance import _Distance
from ..phonetic import MRA as MRAPhonetic

__all__ = ['MRA']


class MRA(_Distance):
    """Match Rating Algorithm comparison rating.

    The Western Airlines Surname Match Rating Algorithm comparison rating, as
    presented on page 18 of :cite:`Moore:1977`.

    .. versionadded:: 0.3.6
    """

    _phonetic_alg = MRAPhonetic()

    def dist_abs(self, src, tar):
        """Return the MRA comparison rating of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            MRA comparison rating

        Examples
        --------
        >>> cmp = MRA()
        >>> cmp.dist_abs('cat', 'hat')
        5
        >>> cmp.dist_abs('Niall', 'Neil')
        6
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        5


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 6
        if src == '' or tar == '':
            return 0
        src = list(self._phonetic_alg.encode(src))
        tar = list(self._phonetic_alg.encode(tar))

        if abs(len(src) - len(tar)) > 2:
            return 0

        length_sum = len(src) + len(tar)
        if length_sum < 5:
            min_rating = 5
        elif length_sum < 8:
            min_rating = 4
        elif length_sum < 12:
            min_rating = 3
        else:
            min_rating = 2

        for _ in range(2):
            new_src = []
            new_tar = []
            minlen = min(len(src), len(tar))
            for i in range(minlen):
                if src[i] != tar[i]:
                    new_src.append(src[i])
                    new_tar.append(tar[i])
            src = new_src + src[minlen:]
            tar = new_tar + tar[minlen:]
            src.reverse()
            tar.reverse()

        similarity = 6 - max(len(src), len(tar))

        if similarity >= min_rating:
            return similarity
        return 0

    def sim(self, src, tar):
        """Return the normalized MRA similarity of two strings.

        This is the MRA normalized to :math:`[0, 1]`, given that MRA itself is
        constrained to the range :math:`[0, 6]`.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized MRA similarity

        Examples
        --------
        >>> cmp = MRA()
        >>> cmp.sim('cat', 'hat')
        0.8333333333333334
        >>> cmp.sim('Niall', 'Neil')
        1.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.8333333333333334


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return mra_compare(src, tar) / 6


if __name__ == '__main__':
    import doctest

    doctest.testmod()
