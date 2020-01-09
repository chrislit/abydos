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

"""abydos.distance._inclusion.

Bouchard & Pouyez's INClusion Programme
"""

from ._distance import _Distance
from ._levenshtein import Levenshtein

__all__ = ['Inclusion']


class Inclusion(_Distance):
    """Inclusion distance.

    The INC Programme, developed by :cite:`Bouchard:1980` designates two
    terms as being "included" when:

        - One name is shorter than the other
        - There are at least 3 common characters
        - There is at most one difference, disregarding unmatching
          prefixes and suffixes

    In addition to these rules, this implementation considers two terms
    as being "included" if they are identical.

    The return value, though a float, can only take one of two values:
    0.0, indicating inclusion, or 1.0, indication non-inclusion.

    .. versionadded:: 0.4.1
    """

    _lev = Levenshtein()

    def dist(self, src, tar):
        """Return the INClusion Programme value of two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The INC Programme distance

        Examples
        --------
        >>> cmp = Inclusion()
        >>> cmp.dist('cat', 'hat')
        1.0
        >>> cmp.dist('Niall', 'Neil')
        1.0
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 0.0
        if len(src) == len(tar):
            return 1.0

        diff, src, tar = self._lev.alignment(src, tar)

        src = list(src)
        tar = list(tar)

        while src and src[0] == '-':
            src.pop(0)
            tar.pop(0)
            diff -= 1
        while tar and tar[0] == '-':
            src.pop(0)
            tar.pop(0)
            diff -= 1
        while src and src[-1] == '-':
            src.pop()
            tar.pop()
            diff -= 1
        while tar and tar[-1] == '-':
            src.pop()
            tar.pop()
            diff -= 1

        if diff > 1:
            return 1.0
        if len(src) - diff < 3:
            return 1.0
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
