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

"""abydos.distance._marking.

Ehrenfeucht & Haussler's marking distance
"""

from ._distance import _Distance

__all__ = ['Marking']


class Marking(_Distance):
    r"""Ehrenfeucht & Haussler's marking distance.

    This edit distance :cite:`Ehrenfeucht:1988` is the number of `marked`
    characters in one word that must be masked in order for that word to
    consist entirely of substrings of another word.

    It is normalized by the length of the first word.

    .. versionadded:: 0.4.0
    """

    def __init__(self, **kwargs):
        """Initialize Marking instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(Marking, self).__init__(**kwargs)

    def dist_abs(self, src, tar):
        """Return the marking distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        int
            marking distance

        Examples
        --------
        >>> cmp = Marking()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2
        >>> cmp.dist_abs('cbaabdcb', 'abcba')
        2


        .. versionadded:: 0.4.0

        """
        distance = 0
        unmatched = src[:]
        for i in range(len(unmatched) - 1, -1, -1):
            if unmatched[i:] not in tar:
                distance += 1
                unmatched = unmatched[:i]

        return distance

    def dist(self, src, tar):
        """Return the normalized marking distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            marking distance

        Examples
        --------
        >>> cmp = Marking()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.6
        >>> cmp.dist('aluminum', 'Catalan')
        0.625
        >>> cmp.dist('ATCG', 'TAGC')
        0.5
        >>> cmp.dist('cbaabdcb', 'abcba')
        0.25


        .. versionadded:: 0.4.0

        """
        score = self.dist_abs(src, tar)
        if score:
            return score / len(src)
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
