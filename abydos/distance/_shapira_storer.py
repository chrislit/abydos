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

from ._lcsstr import LCSstr
from ._levenshtein import Levenshtein

__all__ = ['ShapiraStorer']


class ShapiraStorer(Levenshtein):
    """Shapira & Storer edit distance with moves.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self, **kwargs
    ):
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
        d = super(ShapiraStorer, self).dist_abs(src, tar)
        return d

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
