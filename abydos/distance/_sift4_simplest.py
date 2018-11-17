# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.distance._sift4_simplest.

Sift4 Simplest approximate string distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six.moves import range

from ._sift4 import Sift4

__all__ = ['Sift4Simplest', 'sift4_simplest']


class Sift4Simplest(Sift4):
    """Sift4 Simplest version.

    This is an approximation of edit distance, described in
    :cite:`Zackwehdex:2014`.
    """

    def dist_abs(self, src, tar, max_offset=5):
        """Return the "simplest" Sift4 distance between two terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        max_offset : int
            The number of characters to search for matching letters

        Returns
        -------
        int
            The Sift4 distance according to the simplest formula

        Examples
        --------
        >>> cmp = Sift4Simplest()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2

        """
        if not src:
            return len(tar)

        if not tar:
            return len(src)

        src_len = len(src)
        tar_len = len(tar)

        src_cur = 0
        tar_cur = 0
        lcss = 0
        local_cs = 0

        while (src_cur < src_len) and (tar_cur < tar_len):
            if src[src_cur] == tar[tar_cur]:
                local_cs += 1
            else:
                lcss += local_cs
                local_cs = 0
                if src_cur != tar_cur:
                    src_cur = tar_cur = max(src_cur, tar_cur)
                for i in range(max_offset):
                    if not (
                        (src_cur + i < src_len) or (tar_cur + i < tar_len)
                    ):
                        break
                    if (src_cur + i < src_len) and (
                        src[src_cur + i] == tar[tar_cur]
                    ):
                        src_cur += i
                        local_cs += 1
                        break
                    if (tar_cur + i < tar_len) and (
                        src[src_cur] == tar[tar_cur + i]
                    ):
                        tar_cur += i
                        local_cs += 1
                        break

            src_cur += 1
            tar_cur += 1

        lcss += local_cs
        return round(max(src_len, tar_len) - lcss)


def sift4_simplest(src, tar, max_offset=5):
    """Return the "simplest" Sift4 distance between two terms.

    This is a wrapper for :py:meth:`Sift4Simplest.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    max_offset : int
        The number of characters to search for matching letters

    Returns
    -------
    int
        The Sift4 distance according to the simplest formula

    Examples
    --------
    >>> sift4_simplest('cat', 'hat')
    1
    >>> sift4_simplest('Niall', 'Neil')
    2
    >>> sift4_simplest('Colin', 'Cuilen')
    3
    >>> sift4_simplest('ATCG', 'TAGC')
    2

    """
    return Sift4Simplest().dist_abs(src, tar, max_offset)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
