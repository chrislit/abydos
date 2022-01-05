# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.distance._hamming.

Hamming distance
"""

from typing import Any

from ._distance import _Distance

__all__ = ['Hamming']


class Hamming(_Distance):
    """Hamming distance.

    Hamming distance :cite:`Hamming:1950` equals the number of character
    positions at which two strings differ. For strings of unequal lengths,
    it is not normally defined. By default, this implementation calculates the
    Hamming distance of the first n characters where n is the lesser of the two
    strings' lengths and adds to this the difference in string lengths.

    .. versionadded:: 0.3.6
    """

    def __init__(self, diff_lens: bool = True, **kwargs: Any) -> None:
        """Initialize Hamming instance.

        Parameters
        ----------
        diff_lens : bool
            If True (default), this returns the Hamming distance for those
            characters that have a matching character in both strings plus the
            difference in the strings' lengths. This is equivalent to extending
            the shorter string with obligatorily non-matching characters. If
            False, an exception is raised in the case of strings of unequal
            lengths.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super().__init__(**kwargs)
        self._diff_lens = diff_lens

    def dist_abs(self, src: str, tar: str) -> float:
        """Return the Hamming distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The Hamming distance between src & tar

        Raises
        ------
        ValueError
            Undefined for sequences of unequal length; set diff_lens to True
            for Hamming distance between strings of unequal lengths.

        Examples
        --------
        >>> cmp = Hamming()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        8
        >>> cmp.dist_abs('ATCG', 'TAGC')
        4


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if not self._diff_lens and len(src) != len(tar):
            raise ValueError(
                'Undefined for sequences of unequal length; set diff_lens '
                + 'to True for Hamming distance between strings of unequal '
                + 'lengths.'
            )

        hdist = 0
        if self._diff_lens:
            hdist += abs(len(src) - len(tar))
        hdist += sum(c1 != c2 for c1, c2 in zip(src, tar))

        return hdist

    def dist(self, src: str, tar: str) -> float:
        """Return the normalized Hamming distance between two strings.

        Hamming distance normalized to the interval [0, 1].

        The Hamming distance is normalized by dividing it
        by the greater of the number of characters in src & tar (unless
        diff_lens is set to False, in which case an exception is raised).

        The arguments are identical to those of the hamming() function.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Hamming distance

        Examples
        --------
        >>> cmp = Hamming()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.6
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0
        return self.dist_abs(src, tar) / max(len(src), len(tar))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
