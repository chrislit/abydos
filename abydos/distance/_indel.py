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

"""abydos.distance._indel.

Indel distance
"""

from typing import Any

from ._levenshtein import Levenshtein

__all__ = ['Indel']


class Indel(Levenshtein):
    """Indel distance.

    This is equivalent to Levenshtein distance, when only inserts and deletes
    are possible.

    .. versionadded:: 0.3.6

    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize Levenshtein instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super().__init__(
            mode='lev', cost=(1, 1, float('inf'), float('inf')), **kwargs
        )

    def dist(self, src: str, tar: str) -> float:
        """Return the normalized indel distance between two strings.

        This is equivalent to normalized Levenshtein distance, when only
        inserts and deletes are possible.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized indel distance

        Examples
        --------
        >>> cmp = Indel()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.333333333333
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.454545454545
        >>> cmp.dist('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.3.6

        """
        if src == tar:
            return 0.0
        return self.dist_abs(src, tar) / (len(src) + len(tar))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
