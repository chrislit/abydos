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

"""abydos.distance._shapira_storer_i.

Shapira & Storer I edit distance with block moves, greedy algorithm
"""

from collections import Counter

from numpy import int as np_int
from numpy import zeros as np_zeros

from ._distance import _Distance
from ._lcsstr import LCSstr

__all__ = ['ShapiraStorerI']


class ShapiraStorerI(_Distance):
    """Shapira & Storer I edit distance with block moves, greedy algorithm.

    Shapira & Storer's greedy edit distance :cite:`Shapira:2007` is similar to
    Levenshtein edit distance, but with two important distinctions:

        - It considers blocks of characters, if they occur in both the source
          and target strings, so the edit distance between 'abcab' and 'abc'
          is only 1, since the substring 'ab' occurs in both and can be
          inserted as a block into 'abc'.
        - It allows three edit operations: insert, delete, and move (but not
          substitute). Thus the distance between 'abcde' and 'deabc' is only 1
          because the block 'abc' can be moved in 1 move operation, rather than
          being deleted and inserted in 2 separate operations.

    If prime is set to True at initialization, this employs the greedy'
    algorithm, which limits replacements of blocks in the two strings to
    matching occurrences of the LCS.

    .. versionadded:: 0.4.0
    """

    _lcs = LCSstr()

    def __init__(self, cost=(1, 1), prime=False, **kwargs):
        """Initialize ShapiraStorerI instance.

        Parameters
        ----------
        prime : bool
            If True, employs the greedy' algorithm rather than greedy
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        self._cost = cost
        self._prime = prime
        super(ShapiraStorerI, self).__init__(**kwargs)

    def dist_abs(self, src, tar):
        """Return the Shapira & Storer I edit distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The Shapira & Storer I edit distance between src & tar

        Examples
        --------
        >>> cmp = ShapiraStorerI()
        >>> cmp.dist_abs('cat', 'hat')
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        9
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2


        .. versionadded:: 0.4.0

        """
        alphabet = set(src) | set(tar)
        next_char = 'A'
        lcs = self._lcs.lcsstr(src, tar)
        while len(lcs) > 1:
            while next_char in alphabet:
                next_char = chr(ord(next_char) + 1)
            if self._prime:
                count = min(src.count(lcs), tar.count(lcs))
                src = src.replace(lcs, next_char, count)
                tar = tar.replace(lcs, next_char, count)
            else:
                src = src.replace(lcs, next_char)
                tar = tar.replace(lcs, next_char)
            alphabet |= {next_char}
            lcs = self._lcs.lcsstr(src, tar)

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
        ins_cost, del_cost = self._cost[:2]

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
        """Return the normalized Shapira & Storer I distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Shapira & Storer I distance between src & tar

        Examples
        --------
        >>> cmp = ShapiraStorerI()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.333333333333
        >>> cmp.dist('aluminum', 'Catalan')
        0.6
        >>> cmp.dist('ATCG', 'TAGC')
        0.25


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0
        ins_cost, del_cost = self._cost[:2]
        src_len = len(src)
        tar_len = len(tar)
        return self.dist_abs(src, tar) / (
            sum([src_len * del_cost, tar_len * ins_cost])
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
