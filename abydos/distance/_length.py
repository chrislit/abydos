# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.distance._length.

Length similarity & distance
"""

from ._distance import _Distance

__all__ = ['Length']


class Length(_Distance):
    """Length similarity and distance.

    .. versionadded:: 0.3.6
    """

    def sim(self, src: str, tar: str) -> float:
        """Return the length similarity of two strings.

        Length similarity is the ratio of the length of the shorter string to
        the longer.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Length similarity

        Examples
        --------
        >>> cmp = Length()
        >>> cmp.sim('cat', 'hat')
        1.0
        >>> cmp.sim('Niall', 'Neil')
        0.8
        >>> cmp.sim('aluminum', 'Catalan')
        0.875
        >>> cmp.sim('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        return (
            len(src) / len(tar) if len(src) < len(tar) else len(tar) / len(src)
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
