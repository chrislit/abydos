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

"""abydos.fingerprint._lightweight.

The fingerprint.lightweight module implements string fingerprints developed
by Cisłak & Grabowski in :cite:`Cislak:2017`:

    - occurrence fingerprint
    - occurrence halved fingerprint
    - count fingerprint
    - position fingerprint
"""

from __future__ import unicode_literals

from collections import Counter

__all__ = [
    'MOST_COMMON_LETTERS',
    'MOST_COMMON_LETTERS_CG',
    'MOST_COMMON_LETTERS_DE',
    'MOST_COMMON_LETTERS_DE_LC',
    'MOST_COMMON_LETTERS_EN_LC',
    'count_fingerprint',
    'occurrence_fingerprint',
    'occurrence_halved_fingerprint',
    'position_fingerprint',
]

# fmt: off
# most common letters, as defined in Cisłak & Grabowski
MOST_COMMON_LETTERS_CG = ('e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd',
                          'l', 'c', 'u', 'm', 'w', 'f')

# most common letters (case-folded to lowercase), as shown in Google Books
# English n-grams, among letters a-z & digits 0-9
MOST_COMMON_LETTERS_EN_LC = ('e', 't', 'a', 'i', 'o', 'n', 's', 'r', 'h', 'l',
                             'd', 'c', 'u', 'm', 'f', 'p', 'g', 'y', 'w', 'b',
                             'v', 'k', 'x', 'j', 'q', 'z', '1', '2', '0', '9',
                             '3', '4', '8', '5', '6', '7')

# most common letters, as shown in Google Books English n-grams, among letters
# A-Z, a-z & digits 0-9
MOST_COMMON_LETTERS = ('e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd',
                       'c', 'u', 'm', 'f', 'p', 'g', 'y', 'w', 'b', 'v', 'k',
                       'T', 'I', 'A', 'S', 'C', 'x', 'M', 'P', 'E', 'B', 'H',
                       'R', 'N', 'D', 'L', 'F', 'W', 'O', 'q', 'G', 'z', 'j',
                       'J', 'U', 'V', 'K', 'Y', '1', '2', '0', 'X', '9', 'Q',
                       '3', 'Z', '4', '8', '5', '6', '7',)

# most common letters (case-folded to lowercase), as shown in Google Books
# German n-grams, among letters (a-z and umlauted vowels & eszett) & digits 0-9
MOST_COMMON_LETTERS_DE = ('e', 'n', 'i', 'r', 's', 't', 'a', 'd', 'h', 'u',
                          'l', 'g', 'c', 'o', 'm', 'b', 'f', 'w', 'k', 'z',
                          'v', 'p', 'ü', 'ä', 'ß', 'ö', 'j', 'y', 'x', 'q',
                          '1', '2', '3', '4', '0', '5', '6', '9', '8', '7')

# most common letters (case-folded to lowercase), as shown in Google Books
# German n-grams, among letters (A-Z, a-z, umlauted vowels & eszett) & digits
# 0-9
MOST_COMMON_LETTERS_DE_LC = ('e', 'n', 'i', 'r', 's', 't', 'a', 'd', 'h', 'u',
                             'l', 'c', 'g', 'o', 'm', 'b', 'f', 'w', 'k', 'z',
                             'v', 'p', 'ü', 'ä', 'S', 'A', 'D', 'B', 'E', 'G',
                             'M', 'ß', 'V', 'K', 'ö', 'W', 'F', 'P', 'R', 'I',
                             'H', 'L', 'T', 'N', 'Z', 'y', 'U', 'j', 'J', 'O',
                             'C', 'x', 'q', 'Ü', 'Q', 'X', 'Ä', 'Ö', '1', '2',
                             'Y', '3', '4', '0', '5', '6', '9', '8', '7')
# fmt: on


def occurrence_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG
):
    """Return the occurrence fingerprint.

    Based on the occurrence fingerprint from :cite:`Cislak:2017`.

    :param str word: the word to fingerprint
    :param int n_bits: number of bits in the fingerprint returned
    :param list most_common: the most common tokens in the target language,
        ordered by frequency
    :returns: the occurrence fingerprint
    :rtype: int

    >>> bin(occurrence_fingerprint('hat'))
    '0b110000100000000'
    >>> bin(occurrence_fingerprint('niall'))
    '0b10110000100000'
    >>> bin(occurrence_fingerprint('colin'))
    '0b1110000110000'
    >>> bin(occurrence_fingerprint('atcg'))
    '0b110000000010000'
    >>> bin(occurrence_fingerprint('entreatment'))
    '0b1110010010000100'
    """
    word = set(word)
    fingerprint = 0

    for letter in most_common:
        if letter in word:
            fingerprint += 1
        n_bits -= 1
        if n_bits:
            fingerprint <<= 1
        else:
            break

    n_bits -= 1
    if n_bits > 0:
        fingerprint <<= n_bits

    return fingerprint


def occurrence_halved_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG
):
    """Return the occurrence halved fingerprint.

    Based on the occurrence halved fingerprint from :cite:`Cislak:2017`.

    :param str word: the word to fingerprint
    :param int n_bits: number of bits in the fingerprint returned
    :param list most_common: the most common tokens in the target language,
        ordered by frequency
    :returns: the occurrence halved fingerprint
    :rtype: int

    >>> bin(occurrence_halved_fingerprint('hat'))
    '0b1010000000010'
    >>> bin(occurrence_halved_fingerprint('niall'))
    '0b10010100000'
    >>> bin(occurrence_halved_fingerprint('colin'))
    '0b1001010000'
    >>> bin(occurrence_halved_fingerprint('atcg'))
    '0b10100000000000'
    >>> bin(occurrence_halved_fingerprint('entreatment'))
    '0b1111010000110000'
    """
    if n_bits % 2:
        n_bits += 1

    w_len = len(word) // 2
    w_1 = set(word[:w_len])
    w_2 = set(word[w_len:])
    fingerprint = 0

    for letter in most_common:
        if n_bits:
            fingerprint <<= 1
            if letter in w_1:
                fingerprint += 1
            fingerprint <<= 1
            if letter in w_2:
                fingerprint += 1
            n_bits -= 2
        else:
            break

    if n_bits > 0:
        fingerprint <<= n_bits

    return fingerprint


def count_fingerprint(word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
    """Return the count fingerprint.

    Based on the count fingerprint from :cite:`Cislak:2017`.

    :param str word: the word to fingerprint
    :param int n_bits: number of bits in the fingerprint returned
    :param list most_common: the most common tokens in the target language,
        ordered by frequency
    :returns: the count fingerprint
    :rtype: int

    >>> bin(count_fingerprint('hat'))
    '0b1010000000001'
    >>> bin(count_fingerprint('niall'))
    '0b10001010000'
    >>> bin(count_fingerprint('colin'))
    '0b101010000'
    >>> bin(count_fingerprint('atcg'))
    '0b1010000000000'
    >>> bin(count_fingerprint('entreatment'))
    '0b1111010000100000'
    """
    if n_bits % 2:
        n_bits += 1

    word = Counter(word)
    fingerprint = 0

    for letter in most_common:
        if n_bits:
            fingerprint <<= 2
            fingerprint += word[letter] & 3
            n_bits -= 2
        else:
            break

    if n_bits:
        fingerprint <<= n_bits

    return fingerprint


def position_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG, bits_per_letter=3
):
    """Return the position fingerprint.

    Based on the position fingerprint from :cite:`Cislak:2017`.

    :param str word: the word to fingerprint
    :param int n_bits: number of bits in the fingerprint returned
    :param list most_common: the most common tokens in the target language,
        ordered by frequency
    :param int bits_per_letter: the bits to assign for letter position
    :returns: the position fingerprint
    :rtype: int

    >>> bin(position_fingerprint('hat'))
    '0b1110100011111111'
    >>> bin(position_fingerprint('niall'))
    '0b1111110101110010'
    >>> bin(position_fingerprint('colin'))
    '0b1111111110010111'
    >>> bin(position_fingerprint('atcg'))
    '0b1110010001111111'
    >>> bin(position_fingerprint('entreatment'))
    '0b101011111111'
    """
    position = {}
    for pos, letter in enumerate(word):
        if letter not in position and letter in most_common:
            position[letter] = min(pos, 2 ** bits_per_letter - 1)

    fingerprint = 0

    for letter in most_common:
        if n_bits:
            fingerprint <<= min(bits_per_letter, n_bits)
            if letter in position:
                fingerprint += min(position[letter], 2 ** n_bits - 1)
            else:
                fingerprint += min(2 ** bits_per_letter - 1, 2 ** n_bits - 1)
            n_bits -= min(bits_per_letter, n_bits)
        else:
            break

    for _ in range(n_bits):
        fingerprint <<= 1
        fingerprint += 1

    return fingerprint


if __name__ == '__main__':
    import doctest

    doctest.testmod()
