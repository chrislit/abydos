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

"""abydos.distance._typo.

Typo edit distance functions.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from numpy import float32 as np_float32
from numpy import zeros as np_zeros

from six.moves import range

from ._distance import _Distance

__all__ = ['Typo', 'dist_typo', 'sim_typo', 'typo']


class Typo(_Distance):
    """Typo distance.

    This is inspired by Typo-Distance :cite:`Song:2011`, and a fair bit of
    this was copied from that module. Compared to the original, this supports
    different metrics for substitution.
    """

    # fmt: off
    _keyboard = {'QWERTY': (
        (('`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='),
         ('', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
          '\\'),
         ('', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\''),
         ('', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/')),
        (('~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'),
         ('', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'),
         ('', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'),
         ('', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?'))
    ), 'Dvorak': (
        (('`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '[', ']'),
         ('', '\'', ',', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l', '/', '=',
          '\\'),
         ('', 'a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's', '-'),
         ('', ';', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z')),
        (('~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}'),
         ('', '"', '<', '>', 'P', 'Y', 'F', 'G', 'C', 'R', 'L', '?', '+', '|'),
         ('', 'A', 'O', 'E', 'U', 'I', 'D', 'H', 'T', 'N', 'S', '_'),
         ('', ':', 'Q', 'J', 'K', 'X', 'B', 'M', 'W', 'V', 'Z'))
    ), 'AZERTY': (
        (('²', '&', 'é', '"', '\'', '(', '-', 'è', '_', 'ç', 'à', ')', '='),
         ('', 'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '', '$'),
         ('', 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'ù', '*'),
         ('<', 'w', 'x', 'c', 'v', 'b', 'n', ',', ';', ':', '!')),
        (('~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '°', '+'),
         ('', 'A', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '', '£'),
         ('', 'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'Ù', 'μ'),
         ('>', 'W', 'X', 'C', 'V', 'B', 'N', '?', '.', '/', '§'))
    ), 'QWERTZ': (
        (('', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ß', ''),
         ('', 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', ' ü', '+',
          '\\'),
         ('', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#'),
         ('<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-')),
        (('°', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ''),
         ('', 'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'Ü', '*', ''),
         ('', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', '\''),
         ('>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_'))
    )}
    # fmt: on

    def dist_abs(
        self,
        src,
        tar,
        metric='euclidean',
        cost=(1, 1, 0.5, 0.5),
        layout='QWERTY',
    ):
        """Return the typo distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        metric : str
            Supported values include: ``euclidean``, ``manhattan``,
            ``log-euclidean``, and ``log-manhattan``
        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and shift, respectively (by
            default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
            significantly less than the cost of an insertion & deletion unless
            a log metric is used.
        layout : str
            Name of the keyboard layout to use (Currently supported:
            ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``)

        Returns
        -------
        float
            Typo distance

        Raises
        ------
        ValueError
            char not found in any keyboard layouts

        Examples
        --------
        >>> cmp = Typo()
        >>> cmp.dist_abs('cat', 'hat')
        1.5811388
        >>> cmp.dist_abs('Niall', 'Neil')
        2.8251407
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3.4142137
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.5

        >>> cmp.dist_abs('cat', 'hat', metric='manhattan')
        2.0
        >>> cmp.dist_abs('Niall', 'Neil', metric='manhattan')
        3.0
        >>> cmp.dist_abs('Colin', 'Cuilen', metric='manhattan')
        3.5
        >>> cmp.dist_abs('ATCG', 'TAGC', metric='manhattan')
        2.5

        >>> cmp.dist_abs('cat', 'hat', metric='log-manhattan')
        0.804719
        >>> cmp.dist_abs('Niall', 'Neil', metric='log-manhattan')
        2.2424533
        >>> cmp.dist_abs('Colin', 'Cuilen', metric='log-manhattan')
        2.2424533
        >>> cmp.dist_abs('ATCG', 'TAGC', metric='log-manhattan')
        2.3465736

        """
        ins_cost, del_cost, sub_cost, shift_cost = cost

        if src == tar:
            return 0.0
        if not src:
            return len(tar) * ins_cost
        if not tar:
            return len(src) * del_cost

        keyboard = self._keyboard[layout]
        lowercase = {item for sublist in keyboard[0] for item in sublist}
        uppercase = {item for sublist in keyboard[1] for item in sublist}

        def _kb_array_for_char(char):
            """Return the keyboard layout that contains ch.

            Parameters
            ----------
            char : str
                The character to lookup

            Returns
            -------
            tuple
                A keyboard

            Raises
            ------
            ValueError
                char not found in any keyboard layouts

            """
            if char in lowercase:
                return keyboard[0]
            elif char in uppercase:
                return keyboard[1]
            raise ValueError(char + ' not found in any keyboard layouts')

        def _substitution_cost(char1, char2):
            cost = sub_cost
            cost *= metric_dict[metric](char1, char2) + shift_cost * (
                _kb_array_for_char(char1) != _kb_array_for_char(char2)
            )
            return cost

        def _get_char_coord(char, kb_array):
            """Return the row & column of char in the keyboard.

            Parameters
            ----------
            char : str
                The character to search for
            kb_array : tuple of tuples
                The array of key positions

            Returns
            -------
            tuple
                The row & column of the key

            """
            for row in kb_array:  # pragma: no branch
                if char in row:
                    return kb_array.index(row), row.index(char)

        def _euclidean_keyboard_distance(char1, char2):
            row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
            row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
            return ((row1 - row2) ** 2 + (col1 - col2) ** 2) ** 0.5

        def _manhattan_keyboard_distance(char1, char2):
            row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
            row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
            return abs(row1 - row2) + abs(col1 - col2)

        def _log_euclidean_keyboard_distance(char1, char2):
            return log(1 + _euclidean_keyboard_distance(char1, char2))

        def _log_manhattan_keyboard_distance(char1, char2):
            return log(1 + _manhattan_keyboard_distance(char1, char2))

        metric_dict = {
            'euclidean': _euclidean_keyboard_distance,
            'manhattan': _manhattan_keyboard_distance,
            'log-euclidean': _log_euclidean_keyboard_distance,
            'log-manhattan': _log_manhattan_keyboard_distance,
        }

        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)
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
                    + (
                        _substitution_cost(src[i], tar[j])
                        if src[i] != tar[j]
                        else 0
                    ),  # sub/==
                )

        return d_mat[len(src), len(tar)]

    def dist(
        self,
        src,
        tar,
        metric='euclidean',
        cost=(1, 1, 0.5, 0.5),
        layout='QWERTY',
    ):
        """Return the normalized typo distance between two strings.

        This is typo distance, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        metric : str
            Supported values include: ``euclidean``, ``manhattan``,
            ``log-euclidean``, and ``log-manhattan``
        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and shift, respectively (by
            default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
            significantly less than the cost of an insertion & deletion unless
            a log metric is used.
        layout : str
            Name of the keyboard layout to use (Currently supported:
            ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``)

        Returns
        -------
        float
            Normalized typo distance

        Examples
        --------
        >>> cmp = Typo()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.527046283086
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.565028142929
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.569035609563
        >>> cmp.dist('ATCG', 'TAGC')
        0.625

        """
        if src == tar:
            return 0.0
        ins_cost, del_cost = cost[:2]
        return self.dist_abs(src, tar, metric, cost, layout) / (
            max(len(src) * del_cost, len(tar) * ins_cost)
        )


def typo(src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5), layout='QWERTY'):
    """Return the typo distance between two strings.

    This is a wrapper for :py:meth:`Typo.typo`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    metric : str
        Supported values include: ``euclidean``, ``manhattan``,
        ``log-euclidean``, and ``log-manhattan``
    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and shift, respectively (by default:
        (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless a
        log metric is used.
    layout : str
        Name of the keyboard layout to use (Currently supported:
        ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``)

    Returns
    -------
    float
        Typo distance

    Examples
    --------
    >>> typo('cat', 'hat')
    1.5811388
    >>> typo('Niall', 'Neil')
    2.8251407
    >>> typo('Colin', 'Cuilen')
    3.4142137
    >>> typo('ATCG', 'TAGC')
    2.5

    >>> typo('cat', 'hat', metric='manhattan')
    2.0
    >>> typo('Niall', 'Neil', metric='manhattan')
    3.0
    >>> typo('Colin', 'Cuilen', metric='manhattan')
    3.5
    >>> typo('ATCG', 'TAGC', metric='manhattan')
    2.5

    >>> typo('cat', 'hat', metric='log-manhattan')
    0.804719
    >>> typo('Niall', 'Neil', metric='log-manhattan')
    2.2424533
    >>> typo('Colin', 'Cuilen', metric='log-manhattan')
    2.2424533
    >>> typo('ATCG', 'TAGC', metric='log-manhattan')
    2.3465736

    """
    return Typo().dist_abs(src, tar, metric, cost, layout)


def dist_typo(
    src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5), layout='QWERTY'
):
    """Return the normalized typo distance between two strings.

    This is a wrapper for :py:meth:`Typo.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    metric : str
        Supported values include: ``euclidean``, ``manhattan``,
        ``log-euclidean``, and ``log-manhattan``
    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and shift, respectively (by default:
        (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless a
        log metric is used.
    layout : str
        Name of the keyboard layout to use (Currently supported:
        ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``)

    Returns
    -------
    float
        Normalized typo distance

    Examples
    --------
    >>> round(dist_typo('cat', 'hat'), 12)
    0.527046283086
    >>> round(dist_typo('Niall', 'Neil'), 12)
    0.565028142929
    >>> round(dist_typo('Colin', 'Cuilen'), 12)
    0.569035609563
    >>> dist_typo('ATCG', 'TAGC')
    0.625

    """
    return Typo().dist(src, tar, metric, cost, layout)


def sim_typo(
    src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5), layout='QWERTY'
):
    """Return the normalized typo similarity between two strings.

    This is a wrapper for :py:meth:`Typo.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    metric : str
        Supported values include: ``euclidean``, ``manhattan``,
        ``log-euclidean``, and ``log-manhattan``
    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and shift, respectively (by default:
        (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless a
        log metric is used.
    layout : str
        Name of the keyboard layout to use (Currently supported:
        ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``)

    Returns
    -------
    float
        Normalized typo similarity

    Examples
    --------
    >>> round(sim_typo('cat', 'hat'), 12)
    0.472953716914
    >>> round(sim_typo('Niall', 'Neil'), 12)
    0.434971857071
    >>> round(sim_typo('Colin', 'Cuilen'), 12)
    0.430964390437
    >>> sim_typo('ATCG', 'TAGC')
    0.375

    """
    return Typo().sim(src, tar, metric, cost, layout)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
