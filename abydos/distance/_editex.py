# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.distance._editex.

editex
"""

from sys import float_info
from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from numpy import float as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance
from .. import __version__

__all__ = ['Editex', 'dist_editex', 'editex', 'sim_editex']


class Editex(_Distance):
    """Editex.

    As described on pages 3 & 4 of :cite:`Zobel:1996`.

    The local variant is based on :cite:`Ring:2009`.

    .. versionadded:: 0.3.6
    .. versionchanged:: 0.4.0
        Added taper option
    """

    _letter_groups = (
        frozenset('AEIOUY'),
        frozenset('BP'),
        frozenset('CKQ'),
        frozenset('DT'),
        frozenset('LR'),
        frozenset('MN'),
        frozenset('GJ'),
        frozenset('FPV'),
        frozenset('SXZ'),
    )

    _all_letters = frozenset('ABCDEFGIJKLMNOPQRSTUVXYZ')

    def __init__(self, cost=(0, 1, 2), local=False, taper=False, **kwargs):
        """Initialize Editex instance.

        Parameters
        ----------
        cost : tuple
            A 3-tuple representing the cost of the four possible edits: match,
            same-group, and mismatch respectively (by default: (0, 1, 2))
        local : bool
            If True, the local variant of Editex is used
        taper : bool
            Enables cost tapering. Following :cite:`Zobel:1996`, it causes
            edits at the start of the string to "just [exceed] twice the
            minimum penalty for replacement or deletion at the end of the
            string".
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(Editex, self).__init__(**kwargs)
        self._cost = cost
        self._local = local
        self._taper_enabled = taper

    def _taper(self, pos, length):
        return (
            round(1 + ((length - pos) / length) * (1 + float_info.epsilon), 15)
            if self._taper_enabled
            else 1
        )

    def dist_abs(self, src, tar):
        """Return the Editex distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            Editex distance

        Examples
        --------
        >>> cmp = Editex()
        >>> cmp.dist_abs('cat', 'hat')
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('aluminum', 'Catalan')
        12
        >>> cmp.dist_abs('ATCG', 'TAGC')
        6


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        match_cost, group_cost, mismatch_cost = self._cost

        def r_cost(ch1, ch2):
            """Return r(a,b) according to Zobel & Dart's definition.

            Parameters
            ----------
            ch1 : str
                The first character to compare
            ch2 : str
                The second character to compare

            Returns
            -------
            int
                r(a,b) according to Zobel & Dart's definition

            .. versionadded:: 0.1.0

            """
            if ch1 == ch2:
                return match_cost
            if ch1 in self._all_letters and ch2 in self._all_letters:
                for group in self._letter_groups:
                    if ch1 in group and ch2 in group:
                        return group_cost
            return mismatch_cost

        def d_cost(ch1, ch2):
            """Return d(a,b) according to Zobel & Dart's definition.

            Parameters
            ----------
            ch1 : str
                The first character to compare
            ch2 : str
                The second character to compare

            Returns
            -------
            int
                d(a,b) according to Zobel & Dart's definition

            .. versionadded:: 0.1.0

            """
            if ch1 != ch2 and (ch1 == 'H' or ch1 == 'W'):
                return group_cost
            return r_cost(ch1, ch2)

        # convert both src & tar to NFKD normalized unicode
        src = unicode_normalize('NFKD', src.upper())
        tar = unicode_normalize('NFKD', tar.upper())

        src_len = len(src)
        tar_len = len(tar)
        max_len = max(src_len, tar_len)

        if src == tar:
            return 0.0
        if not src:
            return sum(
                mismatch_cost * self._taper(pos, max_len)
                for pos in range(tar_len)
            )
        if not tar:
            return sum(
                mismatch_cost * self._taper(pos, max_len)
                for pos in range(src_len)
            )

        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float)
        src = ' ' + src
        tar = ' ' + tar

        if not self._local:
            for i in range(1, src_len + 1):
                d_mat[i, 0] = d_mat[i - 1, 0] + d_cost(
                    src[i - 1], src[i]
                ) * self._taper(i, max_len)
        for j in range(1, tar_len + 1):
            d_mat[0, j] = d_mat[0, j - 1] + d_cost(
                tar[j - 1], tar[j]
            ) * self._taper(j, max_len)

        for i in range(1, src_len + 1):
            for j in range(1, tar_len + 1):
                d_mat[i, j] = min(
                    d_mat[i - 1, j]
                    + d_cost(src[i - 1], src[i])
                    * self._taper(max(i, j), max_len),
                    d_mat[i, j - 1]
                    + d_cost(tar[j - 1], tar[j])
                    * self._taper(max(i, j), max_len),
                    d_mat[i - 1, j - 1]
                    + r_cost(src[i], tar[j]) * self._taper(max(i, j), max_len),
                )

        if int(d_mat[src_len, tar_len]) == d_mat[src_len, tar_len]:
            return int(d_mat[src_len, tar_len])
        else:
            return d_mat[src_len, tar_len]

    def dist(self, src, tar):
        """Return the normalized Editex distance between two strings.

        The Editex distance is normalized by dividing the Editex distance
        (calculated by any of the three supported methods) by the greater of
        the number of characters in src times the cost of a delete and
        the number of characters in tar times the cost of an insert.
        For the case in which all operations have :math:`cost = 1`, this is
        equivalent to the greater of the length of the two strings src & tar.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            Normalized Editex distance

        Examples
        --------
        >>> cmp = Editex()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.2
        >>> cmp.dist('aluminum', 'Catalan')
        0.75
        >>> cmp.dist('ATCG', 'TAGC')
        0.75


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0

        match_cost, group_cost, mismatch_cost = self._cost
        src_len = len(src)
        tar_len = len(tar)

        if self._taper_enabled:
            normalize_term = max(
                [
                    sum(
                        self._taper(pos, src_len) * mismatch_cost
                        for pos in range(src_len)
                    ),
                    sum(
                        self._taper(pos, tar_len) * mismatch_cost
                        for pos in range(tar_len)
                    ),
                ]
            )
        else:
            normalize_term = max(
                src_len * mismatch_cost, tar_len * mismatch_cost
            )
        return self.dist_abs(src, tar) / normalize_term


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Editex.dist_abs method instead.',
)
def editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the Editex distance between two strings.

    This is a wrapper for :py:meth:`Editex.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    cost : tuple
        A 3-tuple representing the cost of the four possible edits: match,
        same-group, and mismatch respectively (by default: (0, 1, 2))
    local : bool
        If True, the local variant of Editex is used

    Returns
    -------
    int
        Editex distance

    Examples
    --------
    >>> editex('cat', 'hat')
    2
    >>> editex('Niall', 'Neil')
    2
    >>> editex('aluminum', 'Catalan')
    12
    >>> editex('ATCG', 'TAGC')
    6

    .. versionadded:: 0.1.0

    """
    return Editex(cost, local).dist_abs(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Editex.dist method instead.',
)
def dist_editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the normalized Editex distance between two strings.

    This is a wrapper for :py:meth:`Editex.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    cost : tuple
        A 3-tuple representing the cost of the four possible edits: match,
        same-group, and mismatch respectively (by default: (0, 1, 2))
    local : bool
        If True, the local variant of Editex is used

    Returns
    -------
    int
        Normalized Editex distance

    Examples
    --------
    >>> round(dist_editex('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_editex('Niall', 'Neil'), 12)
    0.2
    >>> dist_editex('aluminum', 'Catalan')
    0.75
    >>> dist_editex('ATCG', 'TAGC')
    0.75

    .. versionadded:: 0.1.0

    """
    return Editex(cost, local).dist(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Editex.sim method instead.',
)
def sim_editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the normalized Editex similarity of two strings.

    This is a wrapper for :py:meth:`Editex.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    cost : tuple
        A 3-tuple representing the cost of the four possible edits: match,
        same-group, and mismatch respectively (by default: (0, 1, 2))
    local : bool
        If True, the local variant of Editex is used

    Returns
    -------
    int
        Normalized Editex similarity

    Examples
    --------
    >>> round(sim_editex('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_editex('Niall', 'Neil'), 12)
    0.8
    >>> sim_editex('aluminum', 'Catalan')
    0.25
    >>> sim_editex('ATCG', 'TAGC')
    0.25

    .. versionadded:: 0.1.0

    """
    return Editex(cost, local).sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
