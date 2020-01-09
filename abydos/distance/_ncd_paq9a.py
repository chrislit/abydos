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

"""abydos.distance._ncd_paq9a.

NCD using PAQ9A
"""

from ._distance import _Distance

try:
    import paq
except ImportError:  # pragma: no cover
    # If the system lacks the paq9a library, that's fine, but PAQ9A compression
    # similarity won't be supported.
    paq = None

__all__ = ['NCDpaq9a']


class NCDpaq9a(_Distance):
    """Normalized Compression Distance using PAQ9A compression.

    Cf. http://mattmahoney.net/dc/#paq9a

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    .. versionadded:: 0.4.0
    """

    def dist(self, src, tar):
        """Return the NCD between two strings using PAQ9A compression.

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
            Install the paq module in order to use PAQ9A

        Examples
        --------
        >>> cmp = NCDpaq9a()
        >>> cmp.dist('cat', 'hat')
        0.42857142857142855
        >>> cmp.dist('Niall', 'Neil')
        0.5555555555555556
        >>> cmp.dist('aluminum', 'Catalan')
        0.5833333333333334
        >>> cmp.dist('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        if paq is not None:
            src_comp = paq.compress(src)
            tar_comp = paq.compress(tar)
            concat_comp = paq.compress(src + tar)
            concat_comp2 = paq.compress(tar + src)
        else:  # pragma: no cover
            raise ValueError('Install the paq module in order to use PAQ9A')

        # Each string returned by PAQ9A's compressor has 4 header bytes
        # followed by a byte of information then 3 null bytes. And it is
        # concluded with 3 bytes of \xff. So 4+3+3 invariant bytes are
        # subtracted here.
        return (
            (min(len(concat_comp), len(concat_comp2)) - 10)
            - (min(len(src_comp), len(tar_comp)) - 10)
        ) / (max(len(src_comp), len(tar_comp)) - 10)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
