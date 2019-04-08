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

"""abydos.distance._shapira_storer_ii.

Shapira & Storer II edit distance with block moves, greedy' algorithm
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._shapira_storer_i import ShapiraStorerI

__all__ = ['ShapiraStorerII']


class ShapiraStorerII(ShapiraStorerI):
    """Shapira & Storer II edit distance with block moves, greedy' algorithm.

    Shapira & Storer's greedy' edit distance :cite:`Shapira:2007` is similar to
    Levenshtein edit distance, but with two important distinctions:

        - It considers blocks of characters, if they occur in both the source
          and target strings, so the edit distance between 'abcab' and 'abc'
          is only 1, since the substring 'ab' occurs in both and can be
          inserted as a block into 'abc'.
        - It allows three edit operations: insert, delete, and move (but not
          substitute). Thus the distance between 'abcde' and 'deabc' is only 1
          because the block 'abc' can be moved in 1 move operation, rather than
          being deleted and inserted in 2 separate operations.
        - Distinct from the greedy algorithm, the greedy' algorithm only
          replaces one instance of coinciding blocks in the source and target
          at a time.


    .. versionadded:: 0.4.0
    """

    def __init__(self, **kwargs):
        """Initialize ShapiraStorerII instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(ShapiraStorerII, self).__init__(**kwargs)

    def dist_abs(self, src, tar):
        """Return the Shapira & Storer II edit distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The Shapira & Storer II edit distance between src & tar

        Examples
        --------
        >>> cmp = ShapiraStorerII()
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
        next_char = 'A'
        lcs = self._lcs.lcsstr(src, tar)
        while len(lcs) > 1:
            while next_char in alphabet:
                next_char = chr(ord(next_char) + 1)
            p = self._lcs.lcsstr(src, tar)
            src = src.replace(p, next_char, 1)
            tar = tar.replace(p, next_char, 1)
            alphabet |= {next_char}
            lcs = self._lcs.lcsstr(src, tar)

        d = self._edit_with_moves(src, tar)
        return d

    def dist(self, src, tar):
        """Return the normalized Shapira & Storer II distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Shapira & Storer II distance between src & tar

        Examples
        --------
        >>> cmp = ShapiraStorerII()
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
