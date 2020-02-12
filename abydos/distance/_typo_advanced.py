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

    with open(join(package_path('key_positions'), 'iso_positions.json')) as iso_fp:
        _iso_positions = {key: tuple(value) for key, value in load(iso_fp).items()}

    @staticmethod
    def list_keymaps() -> List[Keymap]:
        keymaps = []
        for fn in listdir(package_path('windows_keymaps')):
            with open(join(package_path('windows_keymaps'), fn)) as fh:
                keymap_json = load(fh)
            keymaps.append(Keymap(fn[:-5], keymap_json['lang']))
        return keymaps

    def get_keymap(self, keymap: str):# -> Dict[FrozenSet[str]: Dict[str, Tuple[float, float]]]:
        try:
            with open(join(package_path('windows_keymaps'), '{}.json'.format(keymap))) as fh:
                keymap_dict = load(fh)
                del keymap_dict['lang']
        except FileNotFoundError:
            raise FileNotFoundError(
                'Keymap file {}.json not found. You can'.format(keymap)
                + ' install keymaps by calling'
                + " abydos.util.download_package('keymaps')")

        def _modifiers_fix(modifiers: str) -> FrozenSet[str]:
            if modifiers == 'none':
                return frozenset()
            else:
                return frozenset(modifiers.split('+'))

        keymap_dict = {_modifiers_fix(mod): map for mod, map in keymap_dict.items()}
        for mod in keymap_dict:
            keymap_dict[mod] = {graph: self._iso_positions[pos] for graph, pos in keymap_dict[mod].items()}
        return keymap_dict

    def __init__(
        self,
        metric: str = 'euclidean',
        cost: Tuple[float, float, float, float] = (1.0, 1.0, 0.5, 0.5),
        layout: str = 'en',
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

        if self._layout == 'auto':
            for kb in ['QWERTY', 'QWERTZ', 'AZERTY']:
                keys = set(chain(*chain(*self._keyboard[kb])))
                letters = set(src) | set(tar)
                if not (letters - keys):
                    keyboard = self._keyboard[kb]
                    break
            else:
                # Fallback to QWERTY
                keyboard = self._keyboard['QWERTY']
        else:
            keyboard = self._keyboard[self._layout]

        kb_array = []
        for kb_mode in keyboard:
            kb_array.append({item for sublist in kb_mode for item in sublist})
        keys = set(chain(*chain(*keyboard)))

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
