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

"""abydos.distance._ncd_lzma.

NCD using LZMA
"""

import lzma

from typing import Any

from ._distance import _Distance


__all__ = ['NCDlzma']


class NCDlzma(_Distance):
    """Normalized Compression Distance using LZMA compression.

    Cf. https://en.wikipedia.org/wiki/Lempel-Ziv-Markov_chain_algorithm

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    .. versionadded:: 0.3.6
    """

    _level = 6

    def __init__(self, level: int = 6, **kwargs: Any) -> None:
        """Initialize LZMA compressor.

        Parameters
        ----------
        level : int
            The compression level (0 to 9)


        .. versionadded:: 0.5.0

        """
        super().__init__(**kwargs)
        self._level = level

    def dist(self, src: str, tar: str) -> float:
        """Return the NCD between two strings using LZMA compression.

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
        >>> cmp = NCDlzma()
        >>> cmp.dist('cat', 'hat')
        0.08695652173913043
        >>> cmp.dist('Niall', 'Neil')
        0.16
        >>> cmp.dist('aluminum', 'Catalan')
        0.16
        >>> cmp.dist('ATCG', 'TAGC')
        0.08695652173913043


        .. versionadded:: 0.3.5
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0

        src_b = src.encode('utf-8')
        tar_b = tar.encode('utf-8')

        src_comp = lzma.compress(src_b, preset=self._level)[14:]
        tar_comp = lzma.compress(tar_b, preset=self._level)[14:]
        concat_comp = lzma.compress(src_b + tar_b, preset=self._level)[14:]
        concat_comp2 = lzma.compress(tar_b + src_b, preset=self._level)[14:]

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
