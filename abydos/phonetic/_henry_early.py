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

"""abydos.phonetic._henry_early.

an early version of Henry Code
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._phonetic import _Phonetic

__all__ = ['HenryEarly', 'henry_early']


class HenryEarly(_Phonetic):
    """Henry code, early version.

    The early version of Henry coding is given in :cite:`Legare:1972`. This is
    different from the later version defined in :cite:`Henry:1976`.
    """

    _uc_c_set = set('BCDFGHJKLMNPQRSTVWXZ')
    _diph = {
        'AI': 'E',
        'AY': 'E',
        'EI': 'E',
        'AU': 'O',
        'OI': 'O',
        'OU': 'O',
        'EU': 'U',
    }
    _simple = {'W': 'V', 'X': 'S', 'Z': 'S'}

    def encode(self, word, max_length=3):
        """Calculate the early version of the Henry code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 3)

        Returns
        -------
        str
            The early Henry code

        Examples
        --------
        >>> henry_early('Marchand')
        'MRC'
        >>> henry_early('Beaulieu')
        'BL'
        >>> henry_early('Beaumont')
        'BM'
        >>> henry_early('Legrand')
        'LGR'
        >>> henry_early('Pelletier')
        'PLT'

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._uc_set)

        if not word:
            return ''

        # Rule Ia seems to be covered entirely in II

        # Rule Ib
        if word[0] in self._uc_vy_set:
            # Ib1
            if (
                word[1:2] in self._uc_c_set - {'M', 'N'}
                and word[2:3] in self._uc_c_set
            ) or (
                word[1:2] in self._uc_c_set and word[2:3] not in self._uc_c_set
            ):
                if word[0] == 'Y':
                    word = 'I' + word[1:]
            # Ib2
            elif word[1:2] in {'M', 'N'} and word[2:3] in self._uc_c_set:
                if word[0] == 'E':
                    word = 'A' + word[1:]
                elif word[0] in {'I', 'U', 'Y'}:
                    word = 'E' + word[1:]
            # Ib3
            elif word[:2] in self._diph:
                word = self._diph[word[:2]] + word[2:]
            # Ib4
            elif word[1:2] in self._uc_vy_set and word[0] == 'Y':
                word = 'I' + word[1:]

        code = ''
        skip = 0

        # Rule II
        for pos, char in enumerate(word):
            nxch = word[pos + 1 : pos + 2]
            prev = word[pos - 1 : pos]

            if skip:
                skip -= 1
            elif char in self._uc_vy_set:
                code += char
            # IIc
            elif char == nxch:
                skip = 1
                code += char
            elif word[pos : pos + 2] in {'CQ', 'DT', 'SC'}:
                continue
            # IIb
            elif char in self._simple:
                code += self._simple[char]
            elif char in {'C', 'G', 'P', 'Q', 'S'}:
                if char == 'C':
                    if nxch in {'A', 'O', 'U', 'L', 'R'}:
                        code += 'K'
                    elif nxch in {'E', 'I', 'Y'}:
                        code += 'S'
                    elif nxch == 'H':
                        if word[pos + 2 : pos + 3] in self._uc_vy_set:
                            code += 'C'
                        else:  # CHR, CHL, etc.
                            code += 'K'
                    else:
                        code += 'C'
                elif char == 'G':
                    if nxch in {'A', 'O', 'U', 'L', 'R'}:
                        code += 'G'
                    elif nxch in {'E', 'I', 'Y'}:
                        code += 'J'
                    elif nxch == 'N':
                        code += 'N'
                elif char == 'P':
                    if nxch != 'H':
                        code += 'P'
                    else:
                        code += 'F'
                elif char == 'Q':
                    if word[pos + 1 : pos + 3] in {'UE', 'UI', 'UY'}:
                        code += 'G'
                    else:  # QUA, QUO, etc.
                        code += 'K'
                else:  # S...
                    if word[pos : pos + 6] == 'SAINTE':
                        code += 'X'
                        skip = 5
                    elif word[pos : pos + 5] == 'SAINT':
                        code += 'X'
                        skip = 4
                    elif word[pos : pos + 3] == 'STE':
                        code += 'X'
                        skip = 2
                    elif word[pos : pos + 2] == 'ST':
                        code += 'X'
                        skip = 1
                    elif nxch in self._uc_c_set:
                        continue
                    else:
                        code += 'S'
            # IId
            elif char == 'H' and prev in self._uc_c_set:
                continue
            elif char in self._uc_c_set - {
                'L',
                'R',
            } and nxch in self._uc_c_set - {'L', 'R'}:
                continue
            elif char == 'L' and nxch in {'M', 'N'}:
                continue
            elif (
                char in {'M', 'N'}
                and prev in self._uc_vy_set
                and nxch in self._uc_c_set
            ):
                continue
            # IIa
            else:
                code += char

        # IIe1
        if code[-4:] in {'AULT', 'EULT', 'OULT'}:
            code = code[:-2]
        # The following are blocked by rules above
        # elif code[-4:-3] in _vows and code[-3:] == 'MPS':
        #    code = code[:-3]
        # elif code[-3:-2] in _vows and code[-2:] in {'MB', 'MP', 'ND',
        #                                             'NS', 'NT'}:
        #    code = code[:-2]
        elif code[-2:-1] == 'R' and code[-1:] in self._uc_c_set:
            code = code[:-1]
        # IIe2
        elif code[-2:-1] in self._uc_vy_set and code[-1:] in {
            'D',
            'M',
            'N',
            'S',
            'T',
        }:
            code = code[:-1]
        elif code[-2:] == 'ER':
            code = code[:-1]

        # Drop non-initial vowels
        code = code[:1] + code[1:].translate(
            {65: '', 69: '', 73: '', 79: '', 85: '', 89: ''}
        )

        if max_length != -1:
            code = code[:max_length]

        return code


def henry_early(word, max_length=3):
    """Calculate the early version of the Henry code for a word.

    This is a wrapper for :py:meth:`HenryEarly.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 3)

    Returns
    -------
    str
        The early Henry code

    Examples
    --------
    >>> henry_early('Marchand')
    'MRC'
    >>> henry_early('Beaulieu')
    'BL'
    >>> henry_early('Beaumont')
    'BM'
    >>> henry_early('Legrand')
    'LGR'
    >>> henry_early('Pelletier')
    'PLT'

    """
    return HenryEarly().encode(word, max_length)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
