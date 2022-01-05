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

"""abydos.phonetic._daitch_mokotoff.

Daitch-Mokotoff Soundex
"""

from typing import Dict, Tuple, Union, cast
from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['DaitchMokotoff']


class DaitchMokotoff(_Phonetic):
    """Daitch-Mokotoff Soundex.

    Based on Daitch-Mokotoff Soundex :cite:`Mokotoff:1997`, this returns values
    of a word as a set. A collection is necessary since there can be multiple
    values for a single word.

    .. versionadded:: 0.3.6
    """

    _dms_table = {
        'STCH': (2, 4, 4),
        'DRZ': (4, 4, 4),
        'ZH': (4, 4, 4),
        'ZHDZH': (2, 4, 4),
        'DZH': (4, 4, 4),
        'DRS': (4, 4, 4),
        'DZS': (4, 4, 4),
        'SCHTCH': (2, 4, 4),
        'SHTSH': (2, 4, 4),
        'SZCZ': (2, 4, 4),
        'TZS': (4, 4, 4),
        'SZCS': (2, 4, 4),
        'STSH': (2, 4, 4),
        'SHCH': (2, 4, 4),
        'D': (3, 3, 3),
        'H': (5, 5, '_'),
        'TTSCH': (4, 4, 4),
        'THS': (4, 4, 4),
        'L': (8, 8, 8),
        'P': (7, 7, 7),
        'CHS': (5, 54, 54),
        'T': (3, 3, 3),
        'X': (5, 54, 54),
        'OJ': (0, 1, '_'),
        'OI': (0, 1, '_'),
        'SCHTSH': (2, 4, 4),
        'OY': (0, 1, '_'),
        'Y': (1, '_', '_'),
        'TSH': (4, 4, 4),
        'ZDZ': (2, 4, 4),
        'TSZ': (4, 4, 4),
        'SHT': (2, 43, 43),
        'SCHTSCH': (2, 4, 4),
        'TTSZ': (4, 4, 4),
        'TTZ': (4, 4, 4),
        'SCH': (4, 4, 4),
        'TTS': (4, 4, 4),
        'SZD': (2, 43, 43),
        'AI': (0, 1, '_'),
        'PF': (7, 7, 7),
        'TCH': (4, 4, 4),
        'PH': (7, 7, 7),
        'TTCH': (4, 4, 4),
        'SZT': (2, 43, 43),
        'ZDZH': (2, 4, 4),
        'EI': (0, 1, '_'),
        'G': (5, 5, 5),
        'EJ': (0, 1, '_'),
        'ZD': (2, 43, 43),
        'IU': (1, '_', '_'),
        'K': (5, 5, 5),
        'O': (0, '_', '_'),
        'SHTCH': (2, 4, 4),
        'S': (4, 4, 4),
        'TRZ': (4, 4, 4),
        'SHD': (2, 43, 43),
        'DSH': (4, 4, 4),
        'CSZ': (4, 4, 4),
        'EU': (1, 1, '_'),
        'TRS': (4, 4, 4),
        'ZS': (4, 4, 4),
        'STRZ': (2, 4, 4),
        'UY': (0, 1, '_'),
        'STRS': (2, 4, 4),
        'CZS': (4, 4, 4),
        'MN': ('6_6', '6_6', '6_6'),
        'UI': (0, 1, '_'),
        'UJ': (0, 1, '_'),
        'UE': (0, '_', '_'),
        'EY': (0, 1, '_'),
        'W': (7, 7, 7),
        'IA': (1, '_', '_'),
        'FB': (7, 7, 7),
        'STSCH': (2, 4, 4),
        'SCHT': (2, 43, 43),
        'NM': ('6_6', '6_6', '6_6'),
        'SCHD': (2, 43, 43),
        'B': (7, 7, 7),
        'DSZ': (4, 4, 4),
        'F': (7, 7, 7),
        'N': (6, 6, 6),
        'CZ': (4, 4, 4),
        'R': (9, 9, 9),
        'U': (0, '_', '_'),
        'V': (7, 7, 7),
        'CS': (4, 4, 4),
        'Z': (4, 4, 4),
        'SZ': (4, 4, 4),
        'TSCH': (4, 4, 4),
        'KH': (5, 5, 5),
        'ST': (2, 43, 43),
        'KS': (5, 54, 54),
        'SH': (4, 4, 4),
        'SC': (2, 4, 4),
        'SD': (2, 43, 43),
        'DZ': (4, 4, 4),
        'ZHD': (2, 43, 43),
        'DT': (3, 3, 3),
        'ZSH': (4, 4, 4),
        'DS': (4, 4, 4),
        'TZ': (4, 4, 4),
        'TS': (4, 4, 4),
        'TH': (3, 3, 3),
        'TC': (4, 4, 4),
        'A': (0, '_', '_'),
        'E': (0, '_', '_'),
        'I': (0, '_', '_'),
        'AJ': (0, 1, '_'),
        'M': (6, 6, 6),
        'Q': (5, 5, 5),
        'AU': (0, 7, '_'),
        'IO': (1, '_', '_'),
        'AY': (0, 1, '_'),
        'IE': (1, '_', '_'),
        'ZSCH': (4, 4, 4),
        'CH': ((5, 4), (5, 4), (5, 4)),
        'CK': ((5, 45), (5, 45), (5, 45)),
        'C': ((5, 4), (5, 4), (5, 4)),
        'J': ((1, 4), ('_', 4), ('_', 4)),
        'RZ': ((94, 4), (94, 4), (94, 4)),
        'RS': ((94, 4), (94, 4), (94, 4)),
    }

    _dms_order = {
        'A': ('AI', 'AJ', 'AU', 'AY', 'A'),
        'B': ('B',),
        'C': ('CHS', 'CSZ', 'CZS', 'CH', 'CK', 'CS', 'CZ', 'C'),
        'D': ('DRS', 'DRZ', 'DSH', 'DSZ', 'DZH', 'DZS', 'DS', 'DT', 'DZ', 'D'),
        'E': ('EI', 'EJ', 'EU', 'EY', 'E'),
        'F': ('FB', 'F'),
        'G': ('G',),
        'H': ('H',),
        'I': ('IA', 'IE', 'IO', 'IU', 'I'),
        'J': ('J',),
        'K': ('KH', 'KS', 'K'),
        'L': ('L',),
        'M': ('MN', 'M'),
        'N': ('NM', 'N'),
        'O': ('OI', 'OJ', 'OY', 'O'),
        'P': ('PF', 'PH', 'P'),
        'Q': ('Q',),
        'R': ('RS', 'RZ', 'R'),
        'S': (
            'SCHTSCH',
            'SCHTCH',
            'SCHTSH',
            'SHTCH',
            'SHTSH',
            'STSCH',
            'SCHD',
            'SCHT',
            'SHCH',
            'STCH',
            'STRS',
            'STRZ',
            'STSH',
            'SZCS',
            'SZCZ',
            'SCH',
            'SHD',
            'SHT',
            'SZD',
            'SZT',
            'SC',
            'SD',
            'SH',
            'ST',
            'SZ',
            'S',
        ),
        'T': (
            'TTSCH',
            'TSCH',
            'TTCH',
            'TTSZ',
            'TCH',
            'THS',
            'TRS',
            'TRZ',
            'TSH',
            'TSZ',
            'TTS',
            'TTZ',
            'TZS',
            'TC',
            'TH',
            'TS',
            'TZ',
            'T',
        ),
        'U': ('UE', 'UI', 'UJ', 'UY', 'U'),
        'V': ('V',),
        'W': ('W',),
        'X': ('X',),
        'Y': ('Y',),
        'Z': (
            'ZHDZH',
            'ZDZH',
            'ZSCH',
            'ZDZ',
            'ZHD',
            'ZSH',
            'ZD',
            'ZH',
            'ZS',
            'Z',
        ),
    }  # type: Dict[str, Tuple[str, ...]]

    _uc_v_set = set('AEIJOUY')

    _alphabetic = dict(zip((ord(_) for _ in '0123456789'), 'AYﬆTSKNPLR'))
    _alphabetic_non_initials = dict(
        zip((ord(_) for _ in '0123456789'), ' A TSKNPLR')
    )

    def __init__(self, max_length: int = 6, zero_pad: bool = True) -> None:
        """Initialize DaitchMokotoff instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 6; must be between 6
            and 64)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string


        .. versionadded:: 0.4.0

        """
        # Require a max_length of at least 6 and not more than 64
        if max_length != -1:
            self._max_length = min(max(6, max_length), 64)
        else:
            self._max_length = 64
        self._zero_pad = zero_pad

    def encode_alpha(self, word: str) -> str:
        """Return the alphabetic Daitch-Mokotoff Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Daitch-Mokotoff Soundex value

        Examples
        --------
        >>> pe = DaitchMokotoff()
        >>> pe.encode_alpha('Christopher')
        'SRSTPR,KRSTPR'
        >>> pe.encode_alpha('Niall')
        'NL'
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Schmidt')
        'SNT'

        >>> DaitchMokotoff(max_length=20,
        ... zero_pad=False).encode_alpha('The quick brown fox')
        'TKSKPRPNPKS,TKKPRPNPKS'


        .. versionadded:: 0.4.0
        .. versionchanged:: 0.6.0
            Made return a str only (comma-separated)

        """
        alphas = [
            code.rstrip('0').translate(self._alphabetic)
            for code in self.encode(word).split(',')
        ]
        return ','.join(
            code[:1] + code[1:].replace('Y', 'A') for code in alphas
        )

    def encode(self, word: str) -> str:
        """Return the Daitch-Mokotoff Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Daitch-Mokotoff Soundex value

        Examples
        --------
        >>> pe = DaitchMokotoff()
        >>> pe.encode('Christopher')
        '494379,594379'
        >>> pe.encode('Niall')
        '680000'
        >>> pe.encode('Smith')
        '463000'
        >>> pe.encode('Schmidt')
        '463000'

        >>> DaitchMokotoff(max_length=20,
        ... zero_pad=False).encode('The quick brown fox')
        '35457976754,3557976754'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class
        .. versionchanged:: 0.6.0
            Made return a str only (comma-separated)

        """
        dms = ['']  # initialize empty code list

        # uppercase, normalize, decompose, and filter non-A-Z
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)

        # Nothing to convert, return base case
        if not word:
            if self._zero_pad:
                return '0' * self._max_length
            return '0'

        pos = 0
        while pos < len(word):
            # Iterate through _dms_order, which specifies the possible
            # substrings for which codes exist in the Daitch-Mokotoff coding
            for sstr in self._dms_order[word[pos]]:  # pragma: no branch
                if word[pos:].startswith(sstr):
                    # Having determined a valid substring start, retrieve the
                    # code
                    dm_tup = cast(
                        Tuple[
                            Union[
                                int,
                                str,
                                Tuple[Union[int, str], Union[int, str]],
                            ],
                            Union[
                                int,
                                str,
                                Tuple[Union[int, str], Union[int, str]],
                            ],
                            Union[
                                int,
                                str,
                                Tuple[Union[int, str], Union[int, str]],
                            ],
                        ],
                        self._dms_table[sstr],
                    )

                    # Having retried the code (triple), determine the correct
                    # positional variant (first, pre-vocalic, elsewhere)
                    if pos == 0:
                        dm_val = dm_tup[
                            0
                        ]  # type: Union[int, str, Tuple[Union[int, str], Union[int, str]]]  # noqa: E501
                    elif (
                        pos + len(sstr) < len(word)
                        and word[pos + len(sstr)] in self._uc_v_set
                    ):
                        dm_val = dm_tup[1]
                    else:
                        dm_val = dm_tup[2]

                    # Build the code strings
                    if isinstance(dm_val, tuple):
                        dms = [f'{_}{dm_val[0]}' for _ in dms] + [
                            f'{_}{dm_val[1]}' for _ in dms
                        ]
                    else:
                        dms = [f'{_}{dm_val}' for _ in dms]
                    pos += len(sstr)
                    break

        # Filter out double letters and _ placeholders
        dms = [
            ''.join(c for c in self._delete_consecutive_repeats(_) if c != '_')
            for _ in dms
        ]

        # Trim codes and return set
        if self._zero_pad:
            dms = [
                (_ + ('0' * self._max_length))[: self._max_length] for _ in dms
            ]
        else:
            dms = [_[: self._max_length] for _ in dms]
        return ','.join(sorted(set(dms)))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
