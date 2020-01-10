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

"""abydos.distance._suffix.

Suffix similarity & distance
"""

from ._distance import _Distance

__all__ = ['Suffix']


class Suffix(_Distance):
    """Suffix similarity and distance.

    .. versionadded:: 0.3.6
    """

    def sim(self, src, tar):
        """Return the suffix similarity of two strings.

        Suffix similarity is the ratio of the length of the shorter term that
        exactly matches the longer term to the length of the shorter term,
        beginning at the end of both terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Suffix similarity

        Examples
        --------
        >>> cmp = Suffix()
        >>> cmp.sim('cat', 'hat')
        0.6666666666666666
        >>> cmp.sim('Niall', 'Neil')
        0.25
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
        min_len = len(min_word)
        for i in range(min_len, 0, -1):
            if min_word[-i:] == max_word[-i:]:
                return i / min_len
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
