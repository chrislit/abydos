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

"""abydos.fingerprint._speedcop.

The fingerprint.speedcop module implements string fingerprints developed by
Pollock & Zomora in :cite:`Pollock:1984`:

    - skeleton key
    - omission key
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type

__all__ = ['omission_key', 'skeleton_key']


def skeleton_key(word):
    """Return the skeleton key.

    The skeleton key of a word is defined in :cite:`Pollock:1984`.

    :param str word: the word to transform into its skeleton key
    :returns: the skeleton key
    :rtype: str

    >>> skeleton_key('The quick brown fox jumped over the lazy dog.')
    'THQCKBRWNFXJMPDVLZYGEUIOA'
    >>> skeleton_key('Christopher')
    'CHRSTPIOE'
    >>> skeleton_key('Niall')
    'NLIA'
    """
    _vowels = {'A', 'E', 'I', 'O', 'U'}

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
    start = word[0:1]
    consonant_part = ''
    vowel_part = ''

    # add consonants & vowels to to separate strings
    # (omitting the first char & duplicates)
    for char in word[1:]:
        if char != start:
            if char in _vowels:
                if char not in vowel_part:
                    vowel_part += char
            elif char not in consonant_part:
                consonant_part += char
    # return the first char followed by consonants followed by vowels
    return start + consonant_part + vowel_part


def omission_key(word):
    """Return the omission key.

    The omission key of a word is defined in :cite:`Pollock:1984`.

    :param str word: the word to transform into its omission key
    :returns: the omission key
    :rtype: str

    >>> omission_key('The quick brown fox jumped over the lazy dog.')
    'JKQXZVWYBFMGPDHCLNTREUIOA'
    >>> omission_key('Christopher')
    'PHCTSRIOE'
    >>> omission_key('Niall')
    'LNIA'
    """
    _consonants = (
        'J',
        'K',
        'Q',
        'X',
        'Z',
        'V',
        'W',
        'Y',
        'B',
        'F',
        'M',
        'G',
        'P',
        'D',
        'H',
        'C',
        'L',
        'N',
        'T',
        'S',
        'R',
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

    key = ''

    # add consonants in order supplied by _consonants (no duplicates)
    for char in _consonants:
        if char in word:
            key += char

    # add vowels in order they appeared in the word (no duplicates)
    for char in word:
        if char not in _consonants and char not in key:
            key += char

    return key


if __name__ == '__main__':
    import doctest

    doctest.testmod()
