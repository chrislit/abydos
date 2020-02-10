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

"""abydos.distance._ncd_bwtrle.

NCD using BWT plus RLE
"""

from ._ncd_rle import NCDrle
from ..compression import BWT

__all__ = ['NCDbwtrle']


class NCDbwtrle(NCDrle):
    """Normalized Compression Distance using BWT plus RLE.

    Cf. https://en.wikipedia.org/wiki/Burrows-Wheeler_transform

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    .. versionadded:: 0.3.6
    """

    _bwt = BWT()

    def dist(self, src: str, tar: str) -> float:
        """Return the NCD between two strings using BWT plus RLE.

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
        >>> cmp = NCDbwtrle()
        >>> cmp.dist('cat', 'hat')
        0.75
        >>> cmp.dist('Niall', 'Neil')
        0.8333333333333334
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.8


        .. versionadded:: 0.3.5
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0

        src_comp = self._rle.encode(self._bwt.encode(src))
        tar_comp = self._rle.encode(self._bwt.encode(tar))
        concat_comp = self._rle.encode(self._bwt.encode(src + tar))
        concat_comp2 = self._rle.encode(self._bwt.encode(tar + src))

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
