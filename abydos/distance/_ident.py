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

"""abydos.distance._ident.

Identity similarity & distance
"""

from ._distance import _Distance

__all__ = ['Ident']


class Ident(_Distance):
    """Identity distance and similarity.

    .. versionadded:: 0.3.6
    """

    def sim(self, src: str, tar: str) -> float:
        """Return the identity similarity of two strings.

        Identity similarity is 1.0 if the two strings are identical,
        otherwise 0.0

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Identity similarity

        Examples
        --------
        >>> cmp = Ident()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('cat', 'cat')
        1.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return 1.0 if src == tar else 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
