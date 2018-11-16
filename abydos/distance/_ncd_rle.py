# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.distance._ncd_rle.

NCD using RLE
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance
from ..compression import RLE

__all__ = ['NCDrle', 'dist_ncd_rle', 'sim_ncd_rle']


class NCDrle(_Distance):
    """Normalized Compression Distance using RLE.

    Cf. https://en.wikipedia.org/wiki/Run-length_encoding

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.
    """

    _rle = RLE()

    def dist(self, src, tar):
        """Return the NCD between two strings using RLE.

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
        >>> cmp = NCDrle()
        >>> cmp.dist('cat', 'hat')
        1.0
        >>> cmp.dist('Niall', 'Neil')
        1.0
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0

        """
        if src == tar:
            return 0.0

        src_comp = self._rle.encode(src)
        tar_comp = self._rle.encode(tar)
        concat_comp = self._rle.encode(src + tar)
        concat_comp2 = self._rle.encode(tar + src)

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


def dist_ncd_rle(src, tar):
    """Return the NCD between two strings using RLE.

    This is a wrapper for :py:meth:`NCDrle.dist`.

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
    >>> dist_ncd_rle('cat', 'hat')
    1.0
    >>> dist_ncd_rle('Niall', 'Neil')
    1.0
    >>> dist_ncd_rle('aluminum', 'Catalan')
    1.0
    >>> dist_ncd_rle('ATCG', 'TAGC')
    1.0

    """
    return NCDrle().dist(src, tar)


def sim_ncd_rle(src, tar):
    """Return the NCD similarity between two strings using RLE.

    This is a wrapper for :py:meth:`NCDrle.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Compression similarity

    Examples
    --------
    >>> sim_ncd_rle('cat', 'hat')
    0.0
    >>> sim_ncd_rle('Niall', 'Neil')
    0.0
    >>> sim_ncd_rle('aluminum', 'Catalan')
    0.0
    >>> sim_ncd_rle('ATCG', 'TAGC')
    0.0

    """
    return NCDrle().sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
