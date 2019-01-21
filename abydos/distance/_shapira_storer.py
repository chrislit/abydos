# -*- coding: utf-8 -*-

# Copyright 2014-2019 by Christopher C. Little.
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

"""abydos.distance._shapira_storer.

Shapira & Storer edit distance with moves
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter

from numpy import int as np_int
from numpy import zeros as np_zeros

from six.moves import range

from ._lcsstr import LCSstr
from ._levenshtein import Levenshtein

__all__ = ['ShapiraStorer']


class ShapiraStorer(Levenshtein):
    """Shapira & Storer edit distance with moves.

    Shapira & Storer's edit distance :cite:`Shapira:2007` is similar to
    Levenshtein edit distance, but with two important distinctions:

        - It considers blocks of characters, if they occur in both the source
          and target strings, so the edit distance between 'abcab' and 'abc'
          is only 1, since the substring 'ab' occurs in both and can be
          inserted as a block into 'abc'.
        - It allows three edit operations: insert, delete, and move (but not
          substitute). Thus the distance between 'abcde' and 'deabc' is only 1
          because the block 'abc' can be moved in 1 move operation, rather than
          being deleted and inserted in 2 separate operations.


    .. versionadded:: 0.4.0
    """

    def __init__(self, **kwargs):
        """Initialize ShapiraStorer instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(ShapiraStorer, self).__init__(**kwargs)
        self.lcs = LCSstr()

    def dist_abs(self, src, tar):
        """Return the Shapira & Storer edit distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The Shapira & Storer edit distance between src & tar

        Examples
        --------
        >>> cmp = ShapiraStorer()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        3


        .. versionadded:: 0.4.0

        """
        alphabet = set(src) | set(tar)
        next_char = ord('A')
        lcs = self.lcs.lcsstr(src, tar)
        while len(lcs) > 1:
            while chr(next_char) in alphabet:
                next_char += 1
            p = self.lcs.lcsstr(src, tar)
            src = src.replace(p, next_char)
            tar = tar.replace(p, next_char)
            alphabet |= next_char
            lcs = self.lcs.lcsstr(src, tar)
        d = self._edit_with_moves(src, tar)
        return d

    def _edit_with_moves(self, src, tar):
        """Return the edit distance between two strings using ins, del, & move.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The Levenshtein distance between src & tar


        .. versionadded:: 0.4.0

        """
        ins_cost, del_cost = (1, 1)

        if src == tar:
            return 0
        if not src:
            return len(tar) * ins_cost
        if not tar:
            return len(src) * del_cost

        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
        for i in range(len(src) + 1):
            d_mat[i, 0] = i * del_cost
        for j in range(len(tar) + 1):
            d_mat[0, j] = j * ins_cost

        for i in range(len(src)):
            for j in range(len(tar)):
                d_mat[i + 1, j + 1] = min(
                    d_mat[i + 1, j] + ins_cost,  # ins
                    d_mat[i, j + 1] + del_cost,  # del
                    d_mat[i, j]
                    + (float('inf') if src[i] != tar[j] else 0),  # sub/==
                )

        distance = d_mat[len(src), len(tar)]

        # Do a backtrace on d_mat to discover an optimal path & count
        # inserted & deleted characters
        i = len(src)
        j = len(tar)
        inserts = Counter()
        deletes = Counter()
        while i > 0 and j > 0:
            ante = [d_mat[i - 1, j - 1], d_mat[i - 1, j], d_mat[i, j - 1]]
            least = ante.index(min(ante))
            old_dist = d_mat[i, j]
            if least == 0:
                i -= 1
                j -= 1
                if d_mat[i, j] < old_dist:
                    deletes[src[i]] += 1
                    inserts[tar[j]] += 1
            elif least == 1:
                i -= 1
                if d_mat[i, j] < old_dist:
                    deletes[src[i]] += 1
            else:
                j -= 1
                if d_mat[i, j] < old_dist:
                    inserts[tar[j]] += 1
        while i > 0:
            i -= 1
            if d_mat[i, j] < old_dist:
                deletes[src[i]] += 1
        while j > 0:
            j -= 1
            if d_mat[i, j] < old_dist:
                inserts[tar[j]] += 1

        moves = sum((inserts & deletes).values())

        return distance - moves

    def dist(self, src, tar):
        """Return the normalized Shapira & Storer distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Levenshtein distance between src & tar

        Examples
        --------
        >>> cmp = ShapiraStorer()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.6
        >>> cmp.dist('aluminum', 'Catalan')
        0.875
        >>> cmp.dist('ATCG', 'TAGC')
        0.75


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0
        ins_cost, del_cost = self._cost[:2]
        return self.dist_abs(src, tar) / (
            self._normalizer([len(src) * del_cost, len(tar) * ins_cost])
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
