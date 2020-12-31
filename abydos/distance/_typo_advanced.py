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

from itertools import chain
from json import load
from math import log
from os import listdir
from os.path import join
from typing import Any, Dict, FrozenSet, List, NamedTuple, Tuple, cast

from numpy import float_ as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance
from ..util import package_path


__all__ = ['TypoAdvanced']

Keymap = NamedTuple('Keymap', [('id', str), ('lang', str)])


class TypoAdvanced(_Distance):
    """Typo Advanced distance.

    .. versionadded:: 0.6.0
    """

    _iso_positions = {
        'A99': (4, 0.5),
        'A00': (4, 1.5),
        'A01': (4, 2.5),
        'A02': (4, 3.5),
        'A03': (4, 4.5),
        'A04': (4, 5.5),
        'A05': (4, 6.5),
        'A06': (4, 7.5),
        'A07': (4, 8.5),
        'A08': (4, 9.5),
        'A09': (4, 10.5),
        'A10': (4, 11.5),
        'A11': (4, 12.5),
        'A12': (4, 13.5),
        'A13': (4, 14.5),
        'A14': (4, 15.5),
        'B99': (3, 0.25),
        'B00': (3, 1.25),
        'B01': (3, 2.25),
        'B02': (3, 3.25),
        'B03': (3, 4.25),
        'B04': (3, 5.25),
        'B05': (3, 6.25),
        'B06': (3, 7.25),
        'B07': (3, 8.25),
        'B08': (3, 9.25),
        'B09': (3, 10.25),
        'B10': (3, 11.25),
        'B11': (3, 12.25),
        'B12': (3, 13.25),
        'B13': (3, 14.25),
        'B14': (3, 15.25),
        'C99': (2, -0.25),
        'C00': (2, 0.75),
        'C01': (2, 1.75),
        'C02': (2, 2.75),
        'C03': (2, 3.75),
        'C04': (2, 4.75),
        'C05': (2, 5.75),
        'C06': (2, 6.75),
        'C07': (2, 7.75),
        'C08': (2, 8.75),
        'C09': (2, 9.75),
        'C10': (2, 10.75),
        'C11': (2, 11.75),
        'C12': (2, 12.75),
        'C13': (2, 13.75),
        'C14': (2, 14.75),
        'D99': (1, -0.5),
        'D00': (1, 0.5),
        'D01': (1, 1.5),
        'D02': (1, 2.5),
        'D03': (1, 3.5),
        'D04': (1, 4.5),
        'D05': (1, 5.5),
        'D06': (1, 6.5),
        'D07': (1, 7.5),
        'D08': (1, 8.5),
        'D09': (1, 9.5),
        'D10': (1, 10.5),
        'D11': (1, 11.5),
        'D12': (1, 12.5),
        'D13': (1, 13.5),
        'D14': (1, 14.5),
        'E99': (0, -1.0),
        'E00': (0, 0.0),
        'E01': (0, 1.0),
        'E02': (0, 2.0),
        'E03': (0, 3.0),
        'E04': (0, 4.0),
        'E05': (0, 5.0),
        'E06': (0, 6.0),
        'E07': (0, 7.0),
        'E08': (0, 8.0),
        'E09': (0, 9.0),
        'E10': (0, 10.0),
        'E11': (0, 11.0),
        'E12': (0, 12.0),
        'E13': (0, 13.0),
        'E14': (0, 14.0),
    }

    _qwerty = {  # Save the windows-en keymap (mostly) as a base case
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
    }  # type: Dict[FrozenSet[str], Dict[str, Tuple[float, float]]]

    _keymap_packages = (
        'windows_keymaps',
        'osx_keymaps',
        'android_keymaps',
        'chromeos_keymaps',
    )

    @staticmethod
    def list_keymaps() -> List[Keymap]:
        """List installed keymaps.

        Returns
        -------
        List[Keymap]
            A list of all keymaps currently installed on the system

        .. versionadded:: 0.6.0

        """
        keymaps = []
        for package in TypoAdvanced._keymap_packages:  # noqa: SF01
            try:
                for fn in listdir(package_path(package)):
                    with open(join(package_path(package), fn)) as fh:
                        keymap_json = load(fh)
                    keymaps.append(Keymap(fn[:-5], keymap_json['lang']))
            except FileNotFoundError:
                pass
        return keymaps

    def _get_keymap(
        self, keymap: str
    ) -> Dict[FrozenSet[str], Dict[str, Tuple[float, float]]]:
        """Load a keymap from disk.

        Parameters
        ----------
        keymap : str
            The name (id) of the keymap

        Returns
        -------
        Dict[FrozenSet[str] : Dict[str: Tuple[float, float]]]
            A keymap dictionary

        .. versionadded:: 0.6.0

        """
        if not keymap:
            return self._qwerty

        keymap_int = None
        try:
            for package in self._keymap_packages:
                with open(
                    join(package_path(package), '{}.json'.format(keymap))
                ) as fh:
                    keymap_int = load(fh)
                    del keymap_int['lang']
        except FileNotFoundError:
            pass

        if keymap_int is None:
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
            _modifiers_fix(mod): kmap for mod, kmap in keymap_int.items()
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
        self._keymap = self._get_keymap(layout)

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
        1.346291201783626
        >>> cmp.dist_abs('Niall', 'Neil')
        2.8081727482164247
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3.5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.5153882032022077

        >>> cmp = TypoAdvanced(metric='manhattan')
        >>> cmp.dist_abs('cat', 'hat')
        1.75
        >>> cmp.dist_abs('Niall', 'Neil')
        3.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3.5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.625

        >>> cmp = TypoAdvanced(metric='log-manhattan')
        >>> cmp.dist_abs('cat', 'hat')
        0.7520386983881371
        >>> cmp.dist_abs('Niall', 'Neil')
        2.250205418161983
        >>> cmp.dist_abs('Colin', 'Cuilen')
        2.242453324894
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.4054651081081646


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

        def _kb_modes_for_char(char: str) -> List[FrozenSet[str]]:
            """Return the keyboard mode that contains ch.

            Parameters
            ----------
            char : str
                The character to lookup

            Returns
            -------
            list of frozensets
                The keyboard modes containing the character

            Raises
            ------
            ValueError
                char not found in any keyboard layouts

            .. versionadded:: 0.6.0

            """
            kb_modes = []
            for kb_mode in self._keymap.keys():
                if char in self._keymap[kb_mode]:
                    kb_modes.append(kb_mode)
            if kb_modes:
                return kb_modes
            raise ValueError(char + ' not found in any keyboard layouts')

        def _substitution_cost(char1: str, char2: str) -> float:
            if self._failsafe and (char1 not in keys or char2 not in keys):
                return ins_cost + del_cost
            cost = float('inf')

            char1_modes = _kb_modes_for_char(char1)
            char2_modes = _kb_modes_for_char(char2)

            for ch1_mode in char1_modes:
                for ch2_mode in char2_modes:
                    new_cost = sub_cost * metric_dict[self._metric](
                        ch1_mode, char1, ch2_mode, char2
                    )
                    new_cost += shift_cost * len(ch1_mode ^ ch2_mode)
                    if new_cost < cost:
                        cost = new_cost
            return cost

        def _euclidean_keyboard_distance(
            char1_mode: FrozenSet[str],
            char1: str,
            char2_mode: FrozenSet[str],
            char2: str,
        ) -> float:
            row1, col1 = self._keymap[char1_mode][char1]
            row2, col2 = self._keymap[char2_mode][char2]
            return ((row1 - row2) ** 2 + (col1 - col2) ** 2) ** 0.5

        def _manhattan_keyboard_distance(
            char1_mode: FrozenSet[str],
            char1: str,
            char2_mode: FrozenSet[str],
            char2: str,
        ) -> float:
            row1, col1 = self._keymap[char1_mode][char1]
            row2, col2 = self._keymap[char2_mode][char2]
            return abs(row1 - row2) + abs(col1 - col2)

        def _log_euclidean_keyboard_distance(
            char1_mode: FrozenSet[str],
            char1: str,
            char2_mode: FrozenSet[str],
            char2: str,
        ) -> float:
            return log(
                1
                + _euclidean_keyboard_distance(
                    char1_mode, char1, char2_mode, char2
                )
            )

        def _log_manhattan_keyboard_distance(
            char1_mode: FrozenSet[str],
            char1: str,
            char2_mode: FrozenSet[str],
            char2: str,
        ) -> float:
            return log(
                1
                + _manhattan_keyboard_distance(
                    char1_mode, char1, char2_mode, char2
                )
            )

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
        0.448763733928
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.561634549643
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.583333333333
        >>> cmp.dist('ATCG', 'TAGC')
        0.6288470508005519


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
