# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.phonetic._phonex.

Phonex
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

__all__ = ['Phonex', 'phonex']


class Phonex(_Phonetic):
    """Phonex code.

    Phonex is an algorithm derived from Soundex, defined in :cite:`Lait:1996`.
    """

    def encode(self, word, max_length=4, zero_pad=True):
        """Return the Phonex code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The Phonex value

        Examples
        --------
        >>> pe = Phonex()
        >>> pe.encode('Christopher')
        'C623'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Schmidt')
        'S253'
        >>> pe.encode('Smith')
        'S530'

        """
        name = unicode_normalize('NFKD', text_type(word.upper()))
        name = name.replace('ß', 'SS')

        # Clamp max_length to [4, 64]
        if max_length != -1:
            max_length = min(max(4, max_length), 64)
        else:
            max_length = 64

        name_code = last = ''

        # Deletions effected by replacing with next letter which
        # will be ignored due to duplicate handling of Soundex code.
        # This is faster than 'moving' all subsequent letters.

        # Remove any trailing Ss
        while name[-1:] == 'S':
            name = name[:-1]

        # Phonetic equivalents of first 2 characters
        # Works since duplicate letters are ignored
        if name[:2] == 'KN':
            name = 'N' + name[2:]  # KN.. == N..
        elif name[:2] == 'PH':
            name = 'F' + name[2:]  # PH.. == F.. (H ignored anyway)
        elif name[:2] == 'WR':
            name = 'R' + name[2:]  # WR.. == R..

        if name:
            # Special case, ignore H first letter (subsequent Hs ignored
            # anyway)
            # Works since duplicate letters are ignored
            if name[0] == 'H':
                name = name[1:]

        if name:
            # Phonetic equivalents of first character
            if name[0] in self._uc_vy_set:
                name = 'A' + name[1:]
            elif name[0] in {'B', 'P'}:
                name = 'B' + name[1:]
            elif name[0] in {'V', 'F'}:
                name = 'F' + name[1:]
            elif name[0] in {'C', 'K', 'Q'}:
                name = 'C' + name[1:]
            elif name[0] in {'G', 'J'}:
                name = 'G' + name[1:]
            elif name[0] in {'S', 'Z'}:
                name = 'S' + name[1:]

            name_code = last = name[0]

        # Modified Soundex code
        for i in range(1, len(name)):
            code = '0'
            if name[i] in {'B', 'F', 'P', 'V'}:
                code = '1'
            elif name[i] in {'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z'}:
                code = '2'
            elif name[i] in {'D', 'T'}:
                if name[i + 1 : i + 2] != 'C':
                    code = '3'
            elif name[i] == 'L':
                if name[i + 1 : i + 2] in self._uc_vy_set or i + 1 == len(
                    name
                ):
                    code = '4'
            elif name[i] in {'M', 'N'}:
                if name[i + 1 : i + 2] in {'D', 'G'}:
                    name = name[: i + 1] + name[i] + name[i + 2 :]
                code = '5'
            elif name[i] == 'R':
                if name[i + 1 : i + 2] in self._uc_vy_set or i + 1 == len(
                    name
                ):
                    code = '6'

            if code != last and code != '0' and i != 0:
                name_code += code

            last = name_code[-1]

        if zero_pad:
            name_code += '0' * max_length
        if not name_code:
            name_code = '0'
        return name_code[:max_length]


def phonex(word, max_length=4, zero_pad=True):
    """Return the Phonex code for a word.

    This is a wrapper for :py:meth:`Phonex.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The Phonex value

    Examples
    --------
    >>> phonex('Christopher')
    'C623'
    >>> phonex('Niall')
    'N400'
    >>> phonex('Schmidt')
    'S253'
    >>> phonex('Smith')
    'S530'

    """
    return Phonex().encode(word, max_length, zero_pad)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
