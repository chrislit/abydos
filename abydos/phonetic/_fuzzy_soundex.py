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

"""abydos.phonetic._fuzzy_soundex.

Fuzzy Soundex
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

__all__ = ['FuzzySoundex', 'fuzzy_soundex']


class FuzzySoundex(_Phonetic):
    """Fuzzy Soundex.

    Fuzzy Soundex is an algorithm derived from Soundex, defined in
    :cite:`Holmes:2002`.
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '0193017-07745501769301-7-9',
        )
    )

    def encode(self, word, max_length=5, zero_pad=True):
        """Return the Fuzzy Soundex code for a word.

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

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')

        # Clamp max_length to [4, 64]
        if max_length != -1:
            max_length = min(max(4, max_length), 64)
        else:
            max_length = 64

        if not word:
            if zero_pad:
                return '0' * max_length
            return '0'

        if word[:2] in {'CS', 'CZ', 'TS', 'TZ'}:
            word = 'SS' + word[2:]
        elif word[:2] == 'GN':
            word = 'NN' + word[2:]
        elif word[:2] in {'HR', 'WR'}:
            word = 'RR' + word[2:]
        elif word[:2] == 'HW':
            word = 'WW' + word[2:]
        elif word[:2] in {'KN', 'NG'}:
            word = 'NN' + word[2:]

        if word[-2:] == 'CH':
            word = word[:-2] + 'KK'
        elif word[-2:] == 'NT':
            word = word[:-2] + 'TT'
        elif word[-2:] == 'RT':
            word = word[:-2] + 'RR'
        elif word[-3:] == 'RDT':
            word = word[:-3] + 'RR'

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

        if zero_pad:
            sdx += '0' * max_length

        return sdx[:max_length]


def fuzzy_soundex(word, max_length=5, zero_pad=True):
    """Return the Fuzzy Soundex code for a word.

    This is a wrapper for :py:meth:`FuzzySoundex.encode`.

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
        The Fuzzy Soundex value

    Examples
    --------
    >>> fuzzy_soundex('Christopher')
    'K6931'
    >>> fuzzy_soundex('Niall')
    'N4000'
    >>> fuzzy_soundex('Smith')
    'S5300'
    >>> fuzzy_soundex('Smith')
    'S5300'

    """
    return FuzzySoundex().encode(word, max_length, zero_pad)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
