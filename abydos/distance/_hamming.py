# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance

__all__ = ['Hamming', 'dist_hamming', 'hamming', 'sim_hamming']


class Hamming(_Distance):
    """Hamming distance.

    Hamming distance :cite:`Hamming:1950` equals the number of character
    positions at which two strings differ. For strings of unequal lengths,
    it is not normally defined. By default, this implementation calculates the
    Hamming distance of the first n characters where n is the lesser of the two
    strings' lengths and adds to this the difference in string lengths.
    """

    def dist_abs(self, src, tar, diff_lens=True):
        """Return the Hamming distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        diff_lens : bool
            If True (default), this returns the Hamming distance for those
            characters that have a matching character in both strings plus the
            difference in the strings' lengths. This is equivalent to extending
            the shorter string with obligatorily non-matching characters. If
            False, an exception is raised in the case of strings of unequal
            lengths.

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

        """
        if not diff_lens and len(src) != len(tar):
            raise ValueError(
                'Undefined for sequences of unequal length; set diff_lens '
                + 'to True for Hamming distance between strings of unequal '
                + 'lengths.'
            )

        hdist = 0
        if diff_lens:
            hdist += abs(len(src) - len(tar))
        hdist += sum(c1 != c2 for c1, c2 in zip(src, tar))

        return hdist

    def dist(self, src, tar, diff_lens=True):
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
        diff_lens : bool
            If True (default), this returns the Hamming distance for those
            characters that have a matching character in both strings plus the
            difference in the strings' lengths. This is equivalent to extending
            the shorter string with obligatorily non-matching characters. If
            False, an exception is raised in the case of strings of unequal
            lengths.

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

        """
        if src == tar:
            return 0.0
        return self.dist_abs(src, tar, diff_lens) / max(len(src), len(tar))


def hamming(src, tar, diff_lens=True):
    """Return the Hamming distance between two strings.

    This is a wrapper for :py:meth:`Hamming.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    diff_lens : bool
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending the
        shorter string with obligatorily non-matching characters. If False, an
        exception is raised in the case of strings of unequal lengths.

    Returns
    -------
    int
        The Hamming distance between src & tar

    Examples
    --------
    >>> hamming('cat', 'hat')
    1
    >>> hamming('Niall', 'Neil')
    3
    >>> hamming('aluminum', 'Catalan')
    8
    >>> hamming('ATCG', 'TAGC')
    4

    """
    return Hamming().dist_abs(src, tar, diff_lens)


def dist_hamming(src, tar, diff_lens=True):
    """Return the normalized Hamming distance between two strings.

    This is a wrapper for :py:meth:`Hamming.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    diff_lens : bool
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending the
        shorter string with obligatorily non-matching characters. If False, an
        exception is raised in the case of strings of unequal lengths.

    Returns
    -------
    float
        The normalized Hamming distance

    Examples
    --------
    >>> round(dist_hamming('cat', 'hat'), 12)
    0.333333333333
    >>> dist_hamming('Niall', 'Neil')
    0.6
    >>> dist_hamming('aluminum', 'Catalan')
    1.0
    >>> dist_hamming('ATCG', 'TAGC')
    1.0

    """
    return Hamming().dist(src, tar, diff_lens)


def sim_hamming(src, tar, diff_lens=True):
    """Return the normalized Hamming similarity of two strings.

    This is a wrapper for :py:meth:`Hamming.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    diff_lens : bool
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending the
        shorter string with obligatorily non-matching characters. If False, an
        exception is raised in the case of strings of unequal lengths.

    Returns
    -------
    float
        The normalized Hamming similarity

    Examples
    --------
    >>> round(sim_hamming('cat', 'hat'), 12)
    0.666666666667
    >>> sim_hamming('Niall', 'Neil')
    0.4
    >>> sim_hamming('aluminum', 'Catalan')
    0.0
    >>> sim_hamming('ATCG', 'TAGC')
    0.0

    """
    return Hamming().sim(src, tar, diff_lens)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
