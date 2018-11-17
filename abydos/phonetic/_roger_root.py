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

"""abydos.phonetic._roger_root.

Roger Root phonetic algorithm
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

from ._phonetic import _Phonetic

__all__ = ['RogerRoot', 'roger_root']


class RogerRoot(_Phonetic):
    """Roger Root code.

    This is Roger Root name coding, described in :cite:`Moore:1977`.
    """

    # '*' is used to prevent combining by _delete_consecutive_repeats()
    _init_patterns = {
        4: {'TSCH': '06'},
        3: {'TSH': '06', 'SCH': '06'},
        2: {
            'CE': '0*0',
            'CH': '06',
            'CI': '0*0',
            'CY': '0*0',
            'DG': '07',
            'GF': '08',
            'GM': '03',
            'GN': '02',
            'KN': '02',
            'PF': '08',
            'PH': '08',
            'PN': '02',
            'SH': '06',
            'TS': '0*0',
            'WR': '04',
        },
        1: {
            'A': '1',
            'B': '09',
            'C': '07',
            'D': '01',
            'E': '1',
            'F': '08',
            'G': '07',
            'H': '2',
            'I': '1',
            'J': '3',
            'K': '07',
            'L': '05',
            'M': '03',
            'N': '02',
            'O': '1',
            'P': '09',
            'Q': '07',
            'R': '04',
            'S': '0*0',
            'T': '01',
            'U': '1',
            'V': '08',
            'W': '4',
            'X': '07',
            'Y': '5',
            'Z': '0*0',
        },
    }

    _med_patterns = {
        4: {'TSCH': '6'},
        3: {'TSH': '6', 'SCH': '6'},
        2: {
            'CE': '0',
            'CH': '6',
            'CI': '0',
            'CY': '0',
            'DG': '7',
            'PH': '8',
            'SH': '6',
            'TS': '0',
        },
        1: {
            'B': '9',
            'C': '7',
            'D': '1',
            'F': '8',
            'G': '7',
            'J': '6',
            'K': '7',
            'L': '5',
            'M': '3',
            'N': '2',
            'P': '9',
            'Q': '7',
            'R': '4',
            'S': '0',
            'T': '1',
            'V': '8',
            'X': '7',
            'Z': '0',
            'A': '*',
            'E': '*',
            'H': '*',
            'I': '*',
            'O': '*',
            'U': '*',
            'W': '*',
            'Y': '*',
        },
    }

    def encode(self, word, max_length=5, zero_pad=True):
        """Return the Roger Root code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The maximum length (default 5) of the code to return
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The Roger Root code

        Examples
        --------
        >>> roger_root('Christopher')
        '06401'
        >>> roger_root('Niall')
        '02500'
        >>> roger_root('Smith')
        '00310'
        >>> roger_root('Schmidt')
        '06310'

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        code = ''
        pos = 0

        # Do first digit(s) first
        for num in range(4, 0, -1):
            if word[:num] in self._init_patterns[num]:
                code = self._init_patterns[num][word[:num]]
                pos += num
                break

        # Then code subsequent digits
        while pos < len(word):
            for num in range(4, 0, -1):  # pragma: no branch
                if word[pos : pos + num] in self._med_patterns[num]:
                    code += self._med_patterns[num][word[pos : pos + num]]
                    pos += num
                    break

        code = self._delete_consecutive_repeats(code)
        code = code.replace('*', '')

        if zero_pad:
            code += '0' * max_length

        return code[:max_length]


def roger_root(word, max_length=5, zero_pad=True):
    """Return the Roger Root code for a word.

    This is a wrapper for :py:meth:`RogerRoot.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The maximum length (default 5) of the code to return
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The Roger Root code

    Examples
    --------
    >>> roger_root('Christopher')
    '06401'
    >>> roger_root('Niall')
    '02500'
    >>> roger_root('Smith')
    '00310'
    >>> roger_root('Schmidt')
    '06310'

    """
    return RogerRoot().encode(word, max_length, zero_pad)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
