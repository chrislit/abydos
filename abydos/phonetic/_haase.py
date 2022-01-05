# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.phonetic._haase.

Haase Phonetik
"""

from itertools import product
from typing import List, Set, Tuple, Union, cast
from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['Haase']


class Haase(_Phonetic):
    """Haase Phonetik.

    Based on the algorithm described at :cite:`Prante:2015`.

    Based on the original :cite:`Haase:2000`.

    .. versionadded:: 0.3.6
    """

    _uc_v_set = set('AEIJOUY')

    _alphabetic = dict(zip((ord(_) for _ in '123456789'), 'PTFKLNRSA'))

    def __init__(self, primary_only: bool = False) -> None:
        """Initialize Haase instance.

        Parameters
        ----------
        primary_only : bool
            If True, only the primary code is returned


        .. versionadded:: 0.4.0

        """
        self._primary_only = primary_only

    def encode_alpha(self, word: str) -> str:
        """Return the alphabetic Haase Phonetik code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Haase Phonetik value

        Examples
        --------
        >>> pe = Haase()
        >>> pe.encode_alpha('Joachim')
        'AKAN'
        >>> pe.encode_alpha('Christoph')
        'KRASTAF,SRASTAF'
        >>> pe.encode_alpha('Jörg')
        'ARK'
        >>> pe.encode_alpha('Smith')
        'SNAT'
        >>> pe.encode_alpha('Schmidt')
        'SNAT,KNAT'


        .. versionadded:: 0.4.0
        .. versionchanged:: 0.6.0
            Made return a str only (comma-separated)

        """
        return self.encode(word).translate(self._alphabetic)

    def encode(self, word: str) -> str:
        """Return the Haase Phonetik (numeric output) code for a word.

        While the output code is numeric, it is nevertheless a str.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Haase Phonetik value as a numeric string

        Examples
        --------
        >>> pe = Haase()
        >>> pe.encode('Joachim')
        '9496'
        >>> pe.encode('Christoph')
        '4798293,8798293'
        >>> pe.encode('Jörg')
        '974'
        >>> pe.encode('Smith')
        '8692'
        >>> pe.encode('Schmidt')
        '8692,4692'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class
        .. versionchanged:: 0.6.0
            Made return a str only (comma-separated)

        """

        def _after(word: str, pos: int, letters: Set[str]) -> bool:
            """Return True if word[pos] follows one of the supplied letters.

            Parameters
            ----------
            word : str
                Word to modify
            pos : int
                Position to examine
            letters : set
                Letters to check for

            Returns
            -------
            bool
                True if word[pos] follows one of letters

            .. versionadded:: 0.3.0

            """
            if pos > 0 and word[pos - 1] in letters:
                return True
            return False

        def _before(word: str, pos: int, letters: Set[str]) -> bool:
            """Return True if word[pos] precedes one of the supplied letters.

            Parameters
            ----------
            word : str
                Word to modify
            pos : int
                Position to examine
            letters : set
                Letters to check for

            Returns
            -------
            bool
                True if word[pos] precedes one of letters

            .. versionadded:: 0.3.0

            """
            if pos + 1 < len(word) and word[pos + 1] in letters:
                return True
            return False

        word = unicode_normalize('NFKD', word.upper())

        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = ''.join(c for c in word if c in self._uc_set)

        variants = []  # type: List[Union[str, Tuple[str, ...]]]
        if self._primary_only:
            variants = [word]
        else:
            pos = 0
            if word[:2] == 'CH':
                variants.append(('CH', 'SCH'))
                pos += 2
            len_3_vars = {
                'OWN': 'AUN',
                'WSK': 'RSK',
                'SCH': 'CH',
                'GLI': 'LI',
                'AUX': 'O',
                'EUX': 'O',
            }
            while pos < len(word):
                if word[pos : pos + 4] == 'ILLE':
                    variants.append(('ILLE', 'I'))
                    pos += 4
                elif word[pos : pos + 3] in len_3_vars:
                    variants.append(
                        (word[pos : pos + 3], len_3_vars[word[pos : pos + 3]])
                    )
                    pos += 3
                elif word[pos : pos + 2] == 'RB':
                    variants.append(('RB', 'RW'))
                    pos += 2
                elif len(word[pos:]) == 3 and word[pos:] == 'EAU':
                    variants.append(('EAU', 'O'))
                    pos += 3
                elif len(word[pos:]) == 1 and word[pos:] in {'A', 'O'}:
                    if word[pos:] == 'O':
                        variants.append(('O', 'OW'))
                    else:
                        variants.append(('A', 'AR'))
                    pos += 1
                else:
                    variants.append((word[pos],))
                    pos += 1

            variants = [''.join(letters) for letters in product(*variants)]

        def _haase_code(word: str) -> str:
            sdx = ''
            for i in range(len(word)):
                if word[i] in self._uc_v_set:
                    sdx += '9'
                elif word[i] == 'B':
                    sdx += '1'
                elif word[i] == 'P':
                    if _before(word, i, {'H'}):
                        sdx += '3'
                    else:
                        sdx += '1'
                elif word[i] in {'D', 'T'}:
                    if _before(word, i, {'C', 'S', 'Z'}):
                        sdx += '8'
                    else:
                        sdx += '2'
                elif word[i] in {'F', 'V', 'W'}:
                    sdx += '3'
                elif word[i] in {'G', 'K', 'Q'}:
                    sdx += '4'
                elif word[i] == 'C':
                    if _after(word, i, {'S', 'Z'}):
                        sdx += '8'
                    elif i == 0:
                        if _before(
                            word,
                            i,
                            {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'},
                        ):
                            sdx += '4'
                        else:
                            sdx += '8'
                    elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                        sdx += '4'
                    else:
                        sdx += '8'
                elif word[i] == 'X':
                    if _after(word, i, {'C', 'K', 'Q'}):
                        sdx += '8'
                    else:
                        sdx += '48'
                elif word[i] == 'L':
                    sdx += '5'
                elif word[i] in {'M', 'N'}:
                    sdx += '6'
                elif word[i] == 'R':
                    sdx += '7'
                elif word[i] in {'S', 'Z'}:
                    sdx += '8'

            sdx = self._delete_consecutive_repeats(sdx)

            return sdx

        encoded = [_haase_code(word) for word in cast(List[str], variants)]
        if len(encoded) > 1:
            encoded_set = set()  # type: Set[str]
            encoded_single = []
            for code in encoded:
                if code not in encoded_set:
                    encoded_set.add(code)
                    encoded_single.append(code)
            return ','.join(encoded_single)

        return encoded[0]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
