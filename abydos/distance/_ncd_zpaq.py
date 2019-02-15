# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._ncd_zpaq.

NCD using NCDzpaq
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance

try:
    import zpaq
except ImportError:  # pragma: no cover
    # If the system lacks the zpaq library, that's fine, but zpaq compression
    # similarity won't be supported.
    zpaq = None

__all__ = ['NCDzpaq']


class NCDzpaq(_Distance):
    """Normalized Compression Distance using ZPAQ compression.

    Cf. http://mattmahoney.net/dc/zpaq.html

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    .. versionadded:: 0.4.0
    """

    def dist(self, src, tar):
        """Return the NCD between two strings using ZPAQ compression.

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
            Install the zpaq module in order to use ZPAQ

        Examples
        --------
        >>> cmp = NCDzpaq()
        >>> cmp.dist('cat', 'hat')
        0.08695652173913043
        >>> cmp.dist('Niall', 'Neil')
        0.16
        >>> cmp.dist('aluminum', 'Catalan')
        0.16
        >>> cmp.dist('ATCG', 'TAGC')
        0.08695652173913043


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        if zpaq is not None:
            src_comp = zpaq.compress(src)
            tar_comp = zpaq.compress(tar)
            concat_comp = zpaq.compress(src + tar)
            concat_comp2 = zpaq.compress(tar + src)
        else:  # pragma: no cover
            raise ValueError('Install the zpaq module in order to use ZPAQ')

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
