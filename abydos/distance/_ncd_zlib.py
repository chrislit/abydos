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

"""abydos.distance._ncd_zlib.

NCD using zlib
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import zlib

from ._distance import _Distance


__all__ = ['NCDzlib', 'dist_ncd_zlib', 'sim_ncd_zlib']


class NCDzlib(_Distance):
    """Normalized Compression Distance using zlib compression.

    Cf. https://zlib.net/

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.
    """

    _compressor = None

    def __init__(self, level=zlib.Z_DEFAULT_COMPRESSION):
        """Initialize zlib compressor.

        Parameters
        ----------
        level : int
            The compression level (0 to 9)

        """
        self._compressor = zlib.compressobj(level)

    def dist(self, src, tar):
        """Return the NCD between two strings using zlib compression.

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
        >>> cmp = NCDzlib()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.45454545454545453
        >>> cmp.dist('aluminum', 'Catalan')
        0.5714285714285714
        >>> cmp.dist('ATCG', 'TAGC')
        0.4

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        self._compressor.compress(src)
        src_comp = self._compressor.flush(zlib.Z_FULL_FLUSH)
        self._compressor.compress(tar)
        tar_comp = self._compressor.flush(zlib.Z_FULL_FLUSH)
        self._compressor.compress(src + tar)
        concat_comp = self._compressor.flush(zlib.Z_FULL_FLUSH)
        self._compressor.compress(tar + src)
        concat_comp2 = self._compressor.flush(zlib.Z_FULL_FLUSH)

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


def dist_ncd_zlib(src, tar):
    """Return the NCD between two strings using zlib compression.

    This is a wrapper for :py:meth:`NCDzlib.dist`.

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
    >>> dist_ncd_zlib('cat', 'hat')
    0.3333333333333333
    >>> dist_ncd_zlib('Niall', 'Neil')
    0.45454545454545453
    >>> dist_ncd_zlib('aluminum', 'Catalan')
    0.5714285714285714
    >>> dist_ncd_zlib('ATCG', 'TAGC')
    0.4

    """
    return NCDzlib().dist(src, tar)


def sim_ncd_zlib(src, tar):
    """Return the NCD similarity between two strings using zlib compression.

    This is a wrapper for :py:meth:`NCDzlib.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float: Compression similarity

    Examples
    --------
    >>> sim_ncd_zlib('cat', 'hat')
    0.6666666666666667
    >>> sim_ncd_zlib('Niall', 'Neil')
    0.5454545454545454
    >>> sim_ncd_zlib('aluminum', 'Catalan')
    0.4285714285714286
    >>> sim_ncd_zlib('ATCG', 'TAGC')
    0.6

    """
    return NCDzlib().sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
