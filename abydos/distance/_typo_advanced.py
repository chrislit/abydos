# Copyright 2020 by Christopher C. Little.
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

from collections import namedtuple
from itertools import chain
from json import load
from math import log
from os import listdir
from os.path import join
from typing import Any, Dict, FrozenSet, List, Tuple, cast

from numpy import float_ as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance
from ..util import package_path


__all__ = ['TypoAdvanced']

Keymap = namedtuple('Keymap', ('id', 'lang'))


class TypoAdvanced(_Distance):
    """Typo Advanced distance.

    .. versionadded:: 0.6.0
    """

    with open(
        join(package_path('key_positions'), 'iso_positions.json')
    ) as iso_fp:
        _iso_positions = {
            key: tuple(value) for key, value in load(iso_fp).items()
        }

    qwerty = {  # Save the windows-en keymap (mostly) as a base case
        frozenset({}): {
            '`': (0, 0.0),
            '1': (0, 1.0),
            '2': (0, 2.0),
            '3': (0, 3.0),
            '4': (0, 4.0),
            '5': (0, 5.0),
            '6': (0, 6.0),
            '7': (0, 7.0),
            '8': (0, 8.0),
            '9': (0, 9.0),
            '0': (0, 10.0),
            '-': (0, 11.0),
            '=': (0, 12.0),
            'q': (1, 1.5),
            'w': (1, 2.5),
            'e': (1, 3.5),
            'r': (1, 4.5),
            't': (1, 5.5),
            'y': (1, 6.5),
            'u': (1, 7.5),
            'i': (1, 8.5),
            'o': (1, 9.5),
            'p': (1, 10.5),
            '[': (1, 11.5),
            ']': (1, 12.5),
            'a': (2, 1.75),
            's': (2, 2.75),
            'd': (2, 3.75),
            'f': (2, 4.75),
            'g': (2, 5.75),
            'h': (2, 6.75),
            'j': (2, 7.75),
            'k': (2, 8.75),
            'l': (2, 9.75),
            ';': (2, 10.75),
            "'": (2, 11.75),
            '\\': (3, 1.25),
            'z': (3, 2.25),
            'x': (3, 3.25),
            'c': (3, 4.25),
            'v': (3, 5.25),
            'b': (3, 6.25),
            'n': (3, 7.25),
            'm': (3, 8.25),
            ',': (3, 9.25),
            '.': (3, 10.25),
            '/': (3, 11.25),
            ' ': (4, 4.5),
        },
        frozenset({'shift'}): {
            '~': (0, 0.0),
            '!': (0, 1.0),
            '@': (0, 2.0),
            '#': (0, 3.0),
            '$': (0, 4.0),
            '%': (0, 5.0),
            '^': (0, 6.0),
            '&': (0, 7.0),
            '*': (0, 8.0),
            '(': (0, 9.0),
            ')': (0, 10.0),
            '_': (0, 11.0),
            '+': (0, 12.0),
            'Q': (1, 1.5),
            'W': (1, 2.5),
            'E': (1, 3.5),
            'R': (1, 4.5),
            'T': (1, 5.5),
            'Y': (1, 6.5),
            'U': (1, 7.5),
            'I': (1, 8.5),
            'O': (1, 9.5),
            'P': (1, 10.5),
            '{': (1, 11.5),
            '}': (1, 12.5),
            'A': (2, 1.75),
            'S': (2, 2.75),
            'D': (2, 3.75),
            'F': (2, 4.75),
            'G': (2, 5.75),
            'H': (2, 6.75),
            'J': (2, 7.75),
            'K': (2, 8.75),
            'L': (2, 9.75),
            ':': (2, 10.75),
            '"': (2, 11.75),
            '|': (3, 1.25),
            'Z': (3, 2.25),
            'X': (3, 3.25),
            'C': (3, 4.25),
            'V': (3, 5.25),
            'B': (3, 6.25),
            'N': (3, 7.25),
            'M': (3, 8.25),
            '<': (3, 9.25),
            '>': (3, 10.25),
            '?': (3, 11.25),
            ' ': (4, 4.5),
        },
        frozenset({'caps'}): {
            '`': (0, 0.0),
            '1': (0, 1.0),
            '2': (0, 2.0),
            '3': (0, 3.0),
            '4': (0, 4.0),
            '5': (0, 5.0),
            '6': (0, 6.0),
            '7': (0, 7.0),
            '8': (0, 8.0),
            '9': (0, 9.0),
            '0': (0, 10.0),
            '-': (0, 11.0),
            '=': (0, 12.0),
            'Q': (1, 1.5),
            'W': (1, 2.5),
            'E': (1, 3.5),
            'R': (1, 4.5),
            'T': (1, 5.5),
            'Y': (1, 6.5),
            'U': (1, 7.5),
            'I': (1, 8.5),
            'O': (1, 9.5),
            'P': (1, 10.5),
            '[': (1, 11.5),
            ']': (1, 12.5),
            'A': (2, 1.75),
            'S': (2, 2.75),
            'D': (2, 3.75),
            'F': (2, 4.75),
            'G': (2, 5.75),
            'H': (2, 6.75),
            'J': (2, 7.75),
            'K': (2, 8.75),
            'L': (2, 9.75),
            ';': (2, 10.75),
            "'": (2, 11.75),
            '\\': (3, 1.25),
            'Z': (3, 2.25),
            'X': (3, 3.25),
            'C': (3, 4.25),
            'V': (3, 5.25),
            'B': (3, 6.25),
            'N': (3, 7.25),
            'M': (3, 8.25),
            ',': (3, 9.25),
            '.': (3, 10.25),
            '/': (3, 11.25),
            ' ': (4, 4.5),
        },
        frozenset({'caps', 'shift'}): {
            '~': (0, 0.0),
            '!': (0, 1.0),
            '@': (0, 2.0),
            '#': (0, 3.0),
            '$': (0, 4.0),
            '%': (0, 5.0),
            '^': (0, 6.0),
            '&': (0, 7.0),
            '*': (0, 8.0),
            '(': (0, 9.0),
            ')': (0, 10.0),
            '_': (0, 11.0),
            '+': (0, 12.0),
            'q': (1, 1.5),
            'w': (1, 2.5),
            'e': (1, 3.5),
            'r': (1, 4.5),
            't': (1, 5.5),
            'y': (1, 6.5),
            'u': (1, 7.5),
            'i': (1, 8.5),
            'o': (1, 9.5),
            'p': (1, 10.5),
            '{': (1, 11.5),
            '}': (1, 12.5),
            'a': (2, 1.75),
            's': (2, 2.75),
            'd': (2, 3.75),
            'f': (2, 4.75),
            'g': (2, 5.75),
            'h': (2, 6.75),
            'j': (2, 7.75),
            'k': (2, 8.75),
            'l': (2, 9.75),
            ':': (2, 10.75),
            '"': (2, 11.75),
            '|': (3, 1.25),
            'z': (3, 2.25),
            'x': (3, 3.25),
            'c': (3, 4.25),
            'v': (3, 5.25),
            'b': (3, 6.25),
            'n': (3, 7.25),
            'm': (3, 8.25),
            '<': (3, 9.25),
            '>': (3, 10.25),
            '?': (3, 11.25),
            ' ': (4, 4.5),
        },
    }

    @staticmethod
    def list_keymaps() -> List[Keymap]:
        keymaps = []
        for package in (
            'windows_keymaps',
            'osx_keymaps',
            'android_keymaps',
            'chromeos_keymaps',
        ):
            try:
                for fn in listdir(package_path(package)):
                    with open(join(package_path(package), fn)) as fh:
                        keymap_json = load(fh)
                    keymaps.append(Keymap(fn[:-5], keymap_json['lang']))
            except FileNotFoundError:
                pass
        return keymaps

    def get_keymap(
        self, keymap: str
    ):  # -> Dict[FrozenSet[str]: Dict[str, Tuple[float, float]]]:
        if not keymap:
            return self.qwerty

        try:
            with open(
                join(package_path('windows_keymaps'), '{}.json'.format(keymap))
            ) as fh:
                keymap_dict = load(fh)
                del keymap_dict['lang']
        except FileNotFoundError:
            raise FileNotFoundError(
                'Keymap file {}.json not found. You can'.format(keymap)
                + ' install keymaps by calling'
                + " abydos.util.download_package('keymaps')"
            )

        def _modifiers_fix(modifiers: str) -> FrozenSet[str]:
            if modifiers == '':
                return frozenset()
            else:
                return frozenset(modifiers.split('+'))

        keymap_dict = {
            _modifiers_fix(mod): map for mod, map in keymap_dict.items()
        }
        for mod in keymap_dict:
            keymap_dict[mod] = {
                graph: self._iso_positions[pos]
                for graph, pos in keymap_dict[mod].items()
            }
        return keymap_dict

    def __init__(
        self,
        metric: str = 'euclidean',
        cost: Tuple[float, float, float, float] = (1.0, 1.0, 0.5, 0.5),
        layout: str = '',
        failsafe: bool = False,
        **kwargs: Any
    ):
        """Initialize TypoAdvanced instance.

        Parameters
        ----------
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
            ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``, ``auto``). If
            ``auto`` is selected, the class will attempt to determine an
            appropriate keyboard based on the supplied words.
        failsafe : bool
            If True, substitution of an unknown character (one not present on
            the selected keyboard) will incur a cost equal to an insertion plus
            a deletion.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.6.0

        """
        super(TypoAdvanced, self).__init__(**kwargs)
        self._metric = metric
        self._cost = cost
        self._layout = layout
        self._failsafe = failsafe
        self._keymap = self.get_keymap(layout)

    def dist_abs(self, src: str, tar: str) -> float:
        """Return the typo distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Typo Advanced distance

        Raises
        ------
        ValueError
            char not found in any keyboard layouts

        Examples
        --------
        >>> cmp = TypoAdvanced()
        >>> cmp.dist_abs('cat', 'hat')
        1.5811388300841898
        >>> cmp.dist_abs('Niall', 'Neil')
        2.8251407699364424
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3.414213562373095
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.5

        >>> cmp = TypoAdvanced(metric='manhattan')
        >>> cmp.dist_abs('cat', 'hat')
        2.0
        >>> cmp.dist_abs('Niall', 'Neil')
        3.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3.5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.5

        >>> cmp = TypoAdvanced(metric='log-manhattan')
        >>> cmp.dist_abs('cat', 'hat')
        0.8047189562170501
        >>> cmp.dist_abs('Niall', 'Neil')
        2.2424533248940004
        >>> cmp.dist_abs('Colin', 'Cuilen')
        2.242453324894
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.3465735902799727


        .. versionadded:: 0.6.0

        """
        ins_cost, del_cost, sub_cost, shift_cost = self._cost

        if src == tar:
            return 0.0
        if not src:
            return len(tar) * ins_cost
        if not tar:
            return len(src) * del_cost

        keys = set(chain(*chain(*self._keymap.values())))

        def _kb_array_for_char(char: str) -> Tuple[Tuple[str, ...], ...]:
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

            .. versionadded:: 0.6.0

            """
            for i, kb_mode in enumerate(kb_array):
                if char in kb_mode:
                    return keyboard[i]
            raise ValueError(char + ' not found in any keyboard layouts')

        def _substitution_cost(char1: str, char2: str) -> float:
            if self._failsafe and (char1 not in keys or char2 not in keys):
                return ins_cost + del_cost
            cost = sub_cost
            cost *= metric_dict[self._metric](char1, char2) + shift_cost * (
                _kb_array_for_char(char1) != _kb_array_for_char(char2)
            )
            return cost

        def _get_char_coord(
            char: str, kb_array: Tuple[Tuple[str, ...], ...]
        ) -> Tuple[int, int]:
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

            .. versionadded:: 0.6.0

            """
            for row in kb_array:  # pragma: no branch
                if char in row:
                    break
            return kb_array.index(row), row.index(char)

        def _euclidean_keyboard_distance(char1: str, char2: str) -> float:
            row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
            row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
            return ((row1 - row2) ** 2 + (col1 - col2) ** 2) ** 0.5

        def _manhattan_keyboard_distance(char1: str, char2: str) -> float:
            row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
            row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
            return abs(row1 - row2) + abs(col1 - col2)

        def _log_euclidean_keyboard_distance(char1: str, char2: str) -> float:
            return log(1 + _euclidean_keyboard_distance(char1, char2))

        def _log_manhattan_keyboard_distance(char1: str, char2: str) -> float:
            return log(1 + _manhattan_keyboard_distance(char1, char2))

        metric_dict = {
            'euclidean': _euclidean_keyboard_distance,
            'manhattan': _manhattan_keyboard_distance,
            'log-euclidean': _log_euclidean_keyboard_distance,
            'log-manhattan': _log_manhattan_keyboard_distance,
        }

        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float)
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

        return cast(float, d_mat[len(src), len(tar)])

    def dist(self, src: str, tar: str) -> float:
        """Return the normalized typo distance between two strings.

        This is typo distance, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized typo distance

        Examples
        --------
        >>> cmp = TypoAdvanced()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.527046276695
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.565028153987
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.569035593729
        >>> cmp.dist('ATCG', 'TAGC')
        0.625


        .. versionadded:: 0.6.0

        """
        if src == tar:
            return 0.0
        ins_cost, del_cost = self._cost[:2]
        return self.dist_abs(src, tar) / (
            max(len(src) * del_cost, len(tar) * ins_cost)
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
