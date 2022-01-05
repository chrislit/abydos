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

"""abydos.phonetic._fuzzy_soundex.

Fuzzy Soundex
"""

from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['FuzzySoundex']


class FuzzySoundex(_Phonetic):
    """Fuzzy Soundex.

    Fuzzy Soundex is an algorithm derived from Soundex, defined in
    :cite:`Holmes:2002`.

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '0193017-07745501769301-7-9',
        )
    )

    _alphabetic = dict(zip((ord(_) for _ in '01345679'), 'APTLNRKS'))

    def __init__(self, max_length: int = 5, zero_pad: bool = True) -> None:
        """Initialize FuzzySoundex instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string


        .. versionadded:: 0.4.0

        """
        # Clamp max_length to [4, 64]
        if max_length != -1:
            self._max_length = min(max(4, max_length), 64)
        else:
            self._max_length = 64
        self._zero_pad = zero_pad

    def encode_alpha(self, word: str) -> str:
        """Return the alphabetic Fuzzy Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Fuzzy Soundex value

        Examples
        --------
        >>> pe = FuzzySoundex()
        >>> pe.encode_alpha('Christopher')
        'KRSTP'
        >>> pe.encode_alpha('Niall')
        'NL'
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Schmidt')
        'SNT'


        .. versionadded:: 0.4.0

        """
        code = self.encode(word).rstrip('0')
        return code[:1] + code[1:].translate(self._alphabetic)

    def encode(self, word: str) -> str:
        """Return the Fuzzy Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Fuzzy Soundex value

        Examples
        --------
        >>> pe = FuzzySoundex()
        >>> pe.encode('Christopher')
        'K6931'
        >>> pe.encode('Niall')
        'N4000'
        >>> pe.encode('Smith')
        'S5300'
        >>> pe.encode('Smith')
        'S5300'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = unicode_normalize('NFKD', word.upper())

        if not word:
            if self._zero_pad:
                return '0' * self._max_length
            return '0'

        if word[:2] in {'CS', 'CZ', 'TS', 'TZ'}:
            word = f'SS{word[2:]}'
        elif word[:2] == 'GN':
            word = f'NN{word[2:]}'
        elif word[:2] in {'HR', 'WR'}:
            word = f'RR{word[2:]}'
        elif word[:2] == 'HW':
            word = f'WW{word[2:]}'
        elif word[:2] in {'KN', 'NG'}:
            word = f'NN{word[2:]}'

        if word[-2:] == 'CH':
            word = f'{word[:-2]}KK'
        elif word[-2:] == 'NT':
            word = f'{word[:-2]}TT'
        elif word[-2:] == 'RT':
            word = f'{word[:-2]}RR'
        elif word[-3:] == 'RDT':
            word = f'{word[:-3]}RR'

        word = word.replace('CA', 'KA')
        word = word.replace('CC', 'KK')
        word = word.replace('CK', 'KK')
        word = word.replace('CE', 'SE')
        word = word.replace('CHL', 'KL')
        word = word.replace('CL', 'KL')
        word = word.replace('CHR', 'KR')
        word = word.replace('CR', 'KR')
        word = word.replace('CI', 'SI')
        word = word.replace('CO', 'KO')
        word = word.replace('CU', 'KU')
        word = word.replace('CY', 'SY')
        word = word.replace('DG', 'GG')
        word = word.replace('GH', 'HH')
        word = word.replace('MAC', 'MK')
        word = word.replace('MC', 'MK')
        word = word.replace('NST', 'NSS')
        word = word.replace('PF', 'FF')
        word = word.replace('PH', 'FF')
        word = word.replace('SCH', 'SSS')
        word = word.replace('TIO', 'SIO')
        word = word.replace('TIA', 'SIO')
        word = word.replace('TCH', 'CHH')

        sdx = word.translate(self._trans)
        sdx = sdx.replace('-', '')

        # remove repeating characters
        sdx = self._delete_consecutive_repeats(sdx)

        if word[0] in {'H', 'W', 'Y'}:
            sdx = word[0] + sdx
        else:
            sdx = word[0] + sdx[1:]

        sdx = sdx.replace('0', '')

        if self._zero_pad:
            sdx += '0' * self._max_length

        return sdx[: self._max_length]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
