# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.phonetic._waahlin.

Wåhlin phonetic encoding
"""

from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['Waahlin']


class Waahlin(_Phonetic):
    """Wåhlin code.

    Wåhlin's first-letter coding is based on the description in
    :cite:`Erikson:1997`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, encoder=None):
        """Initialize Waahlin instance.

        Parameters
        ----------
        encoder : _Phonetic
            An initialized phonetic algorithm object


        .. versionadded:: 0.4.0

        """
        self._encoder = encoder

    _transforms = {
        3: {'SCH': '*', 'STJ': '*', 'SKJ': '*'},
        2: {
            'AE': 'E',
            'CH': 'K',
            'DJ': 'J',
            'GJ': 'J',
            'HJ': 'J',
            'HV': 'V',
            'HW': 'V',
            'HR': 'R',
            'KJ': '+',
            'LJ': 'J',
            'PH': 'F',
            'QU': 'KV',
            'SJ': '*',
            'TJ': '+',
        },
        1: {'Q': 'K', 'W': 'V', 'Z': 'S', 'Ä': 'E'},
    }

    def _encode_next(self, word):
        if word[:3] == 'STI' and word[3:4] in {'E', 'Ä'}:
            code = '*'
            remainder = word[3:]
        elif word[:3] in self._transforms[3]:
            code = self._transforms[3][word[:3]]
            remainder = word[3:]
        elif word[:2] == 'HI' and word[2:3] in {
            'A',
            'E',
            'I',
            'O',
            'U',
            'Y',
            'Å',
            'Ä',
            'Ö',
        }:
            code = 'J'
            remainder = word[2:]
        elif word[:2] == 'SK' and word[2:3] in {'E', 'I', 'Y', 'Ä', 'Ö'}:
            code = '*'
            remainder = word[2:]
        elif word[:2] in self._transforms[2]:
            code = self._transforms[2][word[:2]]
            remainder = word[2:]
        elif word[:1] == 'C' and word[1:2] in {'E', 'I', 'Y', 'Ä'}:
            code = 'S'
            remainder = word[1:]
        elif word[:1] == 'G' and word[1:2] in {'E', 'I', 'Y', 'Ä', 'Ö'}:
            code = 'J'
            remainder = word[1:]
        elif word[:1] == 'I' and word[1:2] in {
            'A',
            'E',
            'I',
            'O',
            'U',
            'Y',
            'Å',
            'Ä',
            'Ö',
        }:
            code = 'J'
            remainder = word[1:]
        elif word[:1] == 'K' and word[1:2] in {'E', 'I', 'Y', 'Ä', 'Ö'}:
            code = '+'
            remainder = word[1:]
        elif word[:1] in self._transforms[1]:
            code = self._transforms[1][word[:1]]
            remainder = word[1:]
        else:
            code = word[:1]
            remainder = word[1:]

        return code, remainder

    def encode_alpha(self, word):
        """Return the alphabetic Wåhlin code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Wåhlin code value

        Examples
        --------
        >>> pe = Waahlin()
        >>> pe.encode_alpha('Christopher')
        'KRISTOFER'
        >>> pe.encode_alpha('Niall')
        'NJALL'
        >>> pe.encode_alpha('Smith')
        'SMITH'
        >>> pe.encode_alpha('Schmidt')
        'ŠMIDT'


        .. versionadded:: 0.4.0

        """
        return (
            self.encode(word, alphabetic=True)
            .replace('+', 'Ç')
            .replace('*', 'Š')
        )

    def encode(self, word, alphabetic=False):
        """Return the Wåhlin code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        alphabetic : bool
            If True, the encoder will apply its alphabetic form (.encode_alpha
            rather than .encode)

        Returns
        -------
        str
            The Wåhlin code value

        Examples
        --------
        >>> pe = Waahlin()
        >>> pe.encode('Christopher')
        'KRISTOFER'
        >>> pe.encode('Niall')
        'NJALL'
        >>> pe.encode('Smith')
        'SMITH'
        >>> pe.encode('Schmidt')
        '*MIDT'


        .. versionadded:: 0.4.0

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFC', word.upper())
        if not word:
            return ''

        if self._encoder is None:
            code = ''
            while word:
                part, word = self._encode_next(word)
                code += part
            return code

        code, word = self._encode_next(word)
        return code + (
            self._encoder.encode_alpha(word)
            if alphabetic
            else self._encoder.encode(word)
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
