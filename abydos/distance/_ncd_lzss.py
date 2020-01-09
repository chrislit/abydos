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

"""abydos.distance._ncd_lzss.

NCD using LZSS
"""

from ._distance import _Distance

try:
    import lzss
except ImportError:  # pragma: no cover
    # If the system lacks the lzss library, that's fine, but LZSS compression
    # similarity won't be supported.
    lzss = None

__all__ = ['NCDlzss']


class NCDlzss(_Distance):
    """Normalized Compression Distance using LZSS compression.

    Cf. https://en.wikipedia.org/wiki/Lempel-Ziv-Storer-Szymanski

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    .. versionadded:: 0.4.0
    """

    def dist(self, src, tar):
        """Return the NCD between two strings using LZSS compression.

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
            Install the PyLZSS module in order to use LZSS

        Examples
        --------
        >>> cmp = NCDlzss()
        >>> cmp.dist('cat', 'hat')
        0.75
        >>> cmp.dist('Niall', 'Neil')
        1.0
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.8


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        if lzss is not None:
            src_comp = lzss.encode(src)
            tar_comp = lzss.encode(tar)
            concat_comp = lzss.encode(src + tar)
            concat_comp2 = lzss.encode(tar + src)
        else:  # pragma: no cover
            raise ValueError('Install the PyLZSS module in order to use LZSS')

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
