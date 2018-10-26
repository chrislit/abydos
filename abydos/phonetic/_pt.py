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

"""abydos.phonetic._pt.

The phonetic._pt module implements phonetic algorithms intended for Portuguese,
including:

    - SoundexBR
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._util import _delete_consecutive_repeats

__all__ = ['soundex_br']


def soundex_br(word, max_length=4, zero_pad=True):
    """Return the SoundexBR encoding of a word.

    This is based on :cite:`Marcelino:2015`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the SoundexBR code
    :rtype: str

    >>> soundex_br('Oliveira')
    'O416'
    >>> soundex_br('Almeida')
    'A453'
    >>> soundex_br('Barbosa')
    'B612'
    >>> soundex_br('Araújo')
    'A620'
    >>> soundex_br('Gonçalves')
    'G524'
    >>> soundex_br('Goncalves')
    'G524'
    """
    _soundex_br_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012623010202',
        )
    )

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = ''.join(
        c
        for c in word
        if c
        in {
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
        }
    )

    if word[:2] == 'WA':
        first = 'V'
    elif word[:1] == 'K' and word[1:2] in {'A', 'O', 'U'}:
        first = 'C'
    elif word[:1] == 'C' and word[1:2] in {'I', 'E'}:
        first = 'S'
    elif word[:1] == 'G' and word[1:2] in {'E', 'I'}:
        first = 'J'
    elif word[:1] == 'Y':
        first = 'I'
    elif word[:1] == 'H':
        first = word[1:2]
        word = word[1:]
    else:
        first = word[:1]

    sdx = first + word[1:].translate(_soundex_br_translation)
    sdx = _delete_consecutive_repeats(sdx)
    sdx = sdx.replace('0', '')

    if zero_pad:
        sdx += '0' * max_length

    return sdx[:max_length]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
