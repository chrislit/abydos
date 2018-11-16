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

"""abydos.distance._ncd_lzma.

NCD using LZMA
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance

try:
    import lzma
except ImportError:  # pragma: no cover
    # If the system lacks the lzma library, that's fine, but lzma compression
    # similarity won't be supported.
    lzma = None

__all__ = ['NCDlzma', 'dist_ncd_lzma', 'sim_ncd_lzma']


class NCDlzma(_Distance):
    """Normalized Compression Distance using LZMA compression.

    Cf. https://en.wikipedia.org/wiki/Lempel-Ziv-Markov_chain_algorithm

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.
    """

    def dist(self, src, tar):
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

        Raises
        ------
        ValueError
            Install the PylibLZMA module in order to use LZMA

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

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        if lzma is not None:
            src_comp = lzma.compress(src)[14:]
            tar_comp = lzma.compress(tar)[14:]
            concat_comp = lzma.compress(src + tar)[14:]
            concat_comp2 = lzma.compress(tar + src)[14:]
        else:  # pragma: no cover
            raise ValueError(
                'Install the PylibLZMA module in order to use LZMA'
            )

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


def dist_ncd_lzma(src, tar):
    """Return the NCD between two strings using LZMA compression.

    This is a wrapper for :py:meth:`NCDlzma.dist`.

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
    >>> dist_ncd_lzma('cat', 'hat')
    0.08695652173913043
    >>> dist_ncd_lzma('Niall', 'Neil')
    0.16
    >>> dist_ncd_lzma('aluminum', 'Catalan')
    0.16
    >>> dist_ncd_lzma('ATCG', 'TAGC')
    0.08695652173913043

    """
    return NCDlzma().dist(src, tar)


def sim_ncd_lzma(src, tar):
    """Return the NCD similarity between two strings using LZMA compression.

    This is a wrapper for :py:meth:`NCDlzma.sim`.

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
    >>> sim_ncd_lzma('cat', 'hat')
    0.9130434782608696
    >>> sim_ncd_lzma('Niall', 'Neil')
    0.84
    >>> sim_ncd_lzma('aluminum', 'Catalan')
    0.84
    >>> sim_ncd_lzma('ATCG', 'TAGC')
    0.9130434782608696

    """
    return NCDlzma().sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
