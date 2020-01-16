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

"""abydos.distance._ncd_bz2.

NCD using bzip2
"""

import bz2

from ._distance import _Distance

__all__ = ['NCDbz2']


class NCDbz2(_Distance):
    """Normalized Compression Distance using bzip2 compression.

    Cf. https://en.wikipedia.org/wiki/Bzip2

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    .. versionadded:: 0.3.6
    """

    _level = 9

    def __init__(self, level=9, **kwargs):
        """Initialize bzip2 compressor.

        Parameters
        ----------
        level : int
            The compression level (0 to 9)


        .. versionadded:: 0.3.6
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        super().__init__(**kwargs)
        self._level = level

    def dist(self, src: str, tar: str) -> float:
        """Return the NCD between two strings using bzip2 compression.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Compression distance

        Examples
        --------
        >>> cmp = NCDbz2()
        >>> cmp.dist('cat', 'hat')
        0.06666666666666667
        >>> cmp.dist('Niall', 'Neil')
        0.03125
        >>> cmp.dist('aluminum', 'Catalan')
        0.17647058823529413
        >>> cmp.dist('ATCG', 'TAGC')
        0.03125


        .. versionadded:: 0.3.5
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        src_comp = bz2.compress(src, self._level)[10:]
        tar_comp = bz2.compress(tar, self._level)[10:]
        concat_comp = bz2.compress(src + tar, self._level)[10:]
        concat_comp2 = bz2.compress(tar + src, self._level)[10:]

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
