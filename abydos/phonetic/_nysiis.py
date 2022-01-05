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

"""abydos.phonetic._nysiis.

New York State Identification and Intelligence System (NYSIIS) phonetic
encoding
"""

from ._phonetic import _Phonetic

__all__ = ['NYSIIS']


class NYSIIS(_Phonetic):
    """NYSIIS Code.

    The New York State Identification and Intelligence System algorithm is
    defined in :cite:`Taft:1970`.

    The modified version of this algorithm is described in Appendix B of
    :cite:`Lynch:1977`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, max_length: int = 6, modified: bool = False) -> None:
        """Initialize AlphaSIS instance.

        Parameters
        ----------
        max_length : int
            The maximum length (default 6) of the code to return
        modified : bool
            Indicates whether to use USDA modified NYSIIS


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length
        # Require a max_length of at least 6
        if self._max_length > -1:
            self._max_length = max(6, self._max_length)

        self._modified = modified

    def encode(self, word: str) -> str:
        """Return the NYSIIS code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The NYSIIS value

        Examples
        --------
        >>> pe = NYSIIS()
        >>> pe.encode('Christopher')
        'CRASTA'
        >>> pe.encode('Niall')
        'NAL'
        >>> pe.encode('Smith')
        'SNAT'
        >>> pe.encode('Schmidt')
        'SNAD'

        >>> NYSIIS(max_length=-1).encode('Christopher')
        'CRASTAFAR'

        >>> pe_8m = NYSIIS(max_length=8, modified=True)
        >>> pe_8m.encode('Christopher')
        'CRASTAFA'
        >>> pe_8m.encode('Niall')
        'NAL'
        >>> pe_8m.encode('Smith')
        'SNAT'
        >>> pe_8m.encode('Schmidt')
        'SNAD'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """

        word = ''.join(c for c in word.upper() if c.isalpha())

        # exit early if there are no alphas
        if not word:
            return ''

        original_first_char = word[0]

        if word[:3] == 'MAC':
            word = f'MCC{word[3:]}'
        elif word[:2] == 'KN':
            word = f'NN{word[2:]}'
        elif word[:1] == 'K':
            word = f'C{word[1:]}'
        elif word[:2] in {'PH', 'PF'}:
            word = f'FF{word[2:]}'
        elif word[:3] == 'SCH':
            word = f'SSS{word[3:]}'
        elif self._modified:
            if word[:2] == 'WR':
                word = f'RR{word[2:]}'
            elif word[:2] == 'RH':
                word = f'RR{word[2:]}'
            elif word[:2] == 'DG':
                word = f'GG{word[2:]}'
            elif word[:1] in self._uc_v_set:
                word = f'A{word[1:]}'

        if self._modified and word[-1:] in {'S', 'Z'}:
            word = word[:-1]

        if (
            word[-2:] == 'EE'
            or word[-2:] == 'IE'
            or (self._modified and word[-2:] == 'YE')
        ):
            word = f'{word[:-2]}Y'
        elif word[-2:] in {'DT', 'RT', 'RD'}:
            word = f'{word[:-2]}D'
        elif word[-2:] in {'NT', 'ND'}:
            word = word[:-2] + ('N' if self._modified else 'D')
        elif self._modified:
            if word[-2:] == 'IX':
                word = f'{word[:-2]}ICK'
            elif word[-2:] == 'EX':
                word = f'{word[:-2]}ECK'
            elif word[-2:] in {'JR', 'SR'}:
                return 'ERROR'

        key = word[:1]

        skip = 0
        for i in range(1, len(word)):
            if i >= len(word):
                continue
            elif skip:
                skip -= 1
                continue
            elif word[i : i + 2] == 'EV':
                word = f'{word[:i]}AF{word[i + 2:]}'
                skip = 1
            elif word[i] in self._uc_v_set:
                word = f'{word[:i]}A{word[i + 1:]}'
            elif self._modified and i != len(word) - 1 and word[i] == 'Y':
                word = f'{word[:i]}A{word[i + 1:]}'
            elif word[i] == 'Q':
                word = f'{word[:i]}G{word[i + 1:]}'
            elif word[i] == 'Z':
                word = f'{word[:i]}S{word[i + 1:]}'
            elif word[i] == 'M':
                word = f'{word[:i]}N{word[i + 1:]}'
            elif word[i : i + 2] == 'KN':
                word = f'{word[:i]}N{word[i + 2:]}'
            elif word[i] == 'K':
                word = f'{word[:i]}C{word[i + 1:]}'
            elif (
                self._modified
                and i == len(word) - 3
                and word[i : i + 3] == 'SCH'
            ):
                word = f'{word[:i]}SSA'
                skip = 2
            elif word[i : i + 3] == 'SCH':
                word = f'{word[:i]}SSS{word[i + 3:]}'
                skip = 2
            elif (
                self._modified
                and i == len(word) - 2
                and word[i : i + 2] == 'SH'
            ):
                word = f'{word[:i]}SA'
                skip = 1
            elif word[i : i + 2] == 'SH':
                word = f'{word[:i]}SS{word[i + 2:]}'
                skip = 1
            elif word[i : i + 2] == 'PH':
                word = f'{word[:i]}FF{word[i + 2:]}'
                skip = 1
            elif self._modified and word[i : i + 3] == 'GHT':
                word = f'{word[:i]}TTT{word[i + 3:]}'
                skip = 2
            elif self._modified and word[i : i + 2] == 'DG':
                word = f'{word[:i]}GG{word[i + 2:]}'
                skip = 1
            elif self._modified and word[i : i + 2] == 'WR':
                word = f'{word[:i]}RR{word[i + 2:]}'
                skip = 1
            elif word[i] == 'H' and (
                word[i - 1] not in self._uc_v_set
                or word[i + 1 : i + 2] not in self._uc_v_set
            ):
                word = word[:i] + word[i - 1] + word[i + 1 :]
            elif word[i] == 'W' and word[i - 1] in self._uc_v_set:
                word = word[:i] + word[i - 1] + word[i + 1 :]

            if word[i : i + skip + 1] != key[-1:]:
                key += word[i : i + skip + 1]

        key = self._delete_consecutive_repeats(key)

        if key[-1:] == 'S':
            key = key[:-1]
        if key[-2:] == 'AY':
            key = f'{key[:-2]}Y'
        if key[-1:] == 'A':
            key = key[:-1]
        if self._modified and key[:1] == 'A':
            key = original_first_char + key[1:]

        if self._max_length > 0:
            key = key[: self._max_length]

        return key


if __name__ == '__main__':
    import doctest

    doctest.testmod()
