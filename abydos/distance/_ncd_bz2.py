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

"""abydos.distance._ncd_bz2.

NCD using bzip2
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import bz2

from ._distance import _Distance

__all__ = ['NCDbz2', 'dist_ncd_bz2', 'sim_ncd_bz2']


class NCDbz2(_Distance):
    """Normalized Compression Distance using bzip2 compression.

    Cf. https://en.wikipedia.org/wiki/Bzip2

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.
    """

    _level = 9

    def __init__(self, level=9):
        """Initialize bzip2 compressor.

        Parameters
        ----------
        level : int
            The compression level (0 to 9)

        """
        self._level = level

    def dist(self, src, tar):
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


def dist_ncd_bz2(src, tar):
    """Return the NCD between two strings using bzip2 compression.

    This is a wrapper for :py:meth:`NCDbz2.dist`.

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
    >>> dist_ncd_bz2('cat', 'hat')
    0.06666666666666667
    >>> dist_ncd_bz2('Niall', 'Neil')
    0.03125
    >>> dist_ncd_bz2('aluminum', 'Catalan')
    0.17647058823529413
    >>> dist_ncd_bz2('ATCG', 'TAGC')
    0.03125

    """
    return NCDbz2().dist(src, tar)


def sim_ncd_bz2(src, tar):
    """Return the NCD similarity between two strings using bzip2 compression.

    This is a wrapper for :py:meth:`NCDbz2.sim`.

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
    >>> sim_ncd_bz2('cat', 'hat')
    0.9333333333333333
    >>> sim_ncd_bz2('Niall', 'Neil')
    0.96875
    >>> sim_ncd_bz2('aluminum', 'Catalan')
    0.8235294117647058
    >>> sim_ncd_bz2('ATCG', 'TAGC')
    0.96875

    """
    return NCDbz2().sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
