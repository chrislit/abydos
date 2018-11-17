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

"""abydos.phonetic._eudex.

Eudex phonetic hash
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six.moves import range

from ._phonetic import _Phonetic

__all__ = ['Eudex', 'eudex']


class Eudex(_Phonetic):
    """Eudex hash.

    This implementation of eudex phonetic hashing is based on the specification
    (not the reference implementation) at :cite:`Ticki:2016`.

    Further details can be found at :cite:`Ticki:2016b`.
    """

    _trailing_phones = {
        'a': 0,  # a
        'b': 0b01001000,  # b
        'c': 0b00001100,  # c
        'd': 0b00011000,  # d
        'e': 0,  # e
        'f': 0b01000100,  # f
        'g': 0b00001000,  # g
        'h': 0b00000100,  # h
        'i': 1,  # i
        'j': 0b00000101,  # j
        'k': 0b00001001,  # k
        'l': 0b10100000,  # l
        'm': 0b00000010,  # m
        'n': 0b00010010,  # n
        'o': 0,  # o
        'p': 0b01001001,  # p
        'q': 0b10101000,  # q
        'r': 0b10100001,  # r
        's': 0b00010100,  # s
        't': 0b00011101,  # t
        'u': 1,  # u
        'v': 0b01000101,  # v
        'w': 0b00000000,  # w
        'x': 0b10000100,  # x
        'y': 1,  # y
        'z': 0b10010100,  # z
        'ß': 0b00010101,  # ß
        'à': 0,  # à
        'á': 0,  # á
        'â': 0,  # â
        'ã': 0,  # ã
        'ä': 0,  # ä[æ]
        'å': 1,  # å[oː]
        'æ': 0,  # æ[æ]
        'ç': 0b10010101,  # ç[t͡ʃ]
        'è': 1,  # è
        'é': 1,  # é
        'ê': 1,  # ê
        'ë': 1,  # ë
        'ì': 1,  # ì
        'í': 1,  # í
        'î': 1,  # î
        'ï': 1,  # ï
        'ð': 0b00010101,  # ð[ð̠](represented as a non-plosive T)
        'ñ': 0b00010111,  # ñ[nj](represented as a combination of n and j)
        'ò': 0,  # ò
        'ó': 0,  # ó
        'ô': 0,  # ô
        'õ': 0,  # õ
        'ö': 1,  # ö[ø]
        '÷': 0b11111111,  # ÷
        'ø': 1,  # ø[ø]
        'ù': 1,  # ù
        'ú': 1,  # ú
        'û': 1,  # û
        'ü': 1,  # ü
        'ý': 1,  # ý
        'þ': 0b00010101,  # þ[ð̠](represented as a non-plosive T)
        'ÿ': 1,  # ÿ
    }

    _initial_phones = {
        'a': 0b10000100,  # a*
        'b': 0b00100100,  # b
        'c': 0b00000110,  # c
        'd': 0b00001100,  # d
        'e': 0b11011000,  # e*
        'f': 0b00100010,  # f
        'g': 0b00000100,  # g
        'h': 0b00000010,  # h
        'i': 0b11111000,  # i*
        'j': 0b00000011,  # j
        'k': 0b00000101,  # k
        'l': 0b01010000,  # l
        'm': 0b00000001,  # m
        'n': 0b00001001,  # n
        'o': 0b10010100,  # o*
        'p': 0b00100101,  # p
        'q': 0b01010100,  # q
        'r': 0b01010001,  # r
        's': 0b00001010,  # s
        't': 0b00001110,  # t
        'u': 0b11100000,  # u*
        'v': 0b00100011,  # v
        'w': 0b00000000,  # w
        'x': 0b01000010,  # x
        'y': 0b11100100,  # y*
        'z': 0b01001010,  # z
        'ß': 0b00001011,  # ß
        'à': 0b10000101,  # à
        'á': 0b10000101,  # á
        'â': 0b10000000,  # â
        'ã': 0b10000110,  # ã
        'ä': 0b10100110,  # ä [æ]
        'å': 0b11000010,  # å [oː]
        'æ': 0b10100111,  # æ [æ]
        'ç': 0b01010100,  # ç [t͡ʃ]
        'è': 0b11011001,  # è
        'é': 0b11011001,  # é
        'ê': 0b11011001,  # ê
        'ë': 0b11000110,  # ë [ə] or [œ]
        'ì': 0b11111001,  # ì
        'í': 0b11111001,  # í
        'î': 0b11111001,  # î
        'ï': 0b11111001,  # ï
        'ð': 0b00001011,  # ð [ð̠] (represented as a non-plosive T)
        'ñ': 0b00001011,  # ñ [nj] (represented as a combination of n and j)
        'ò': 0b10010101,  # ò
        'ó': 0b10010101,  # ó
        'ô': 0b10010101,  # ô
        'õ': 0b10010101,  # õ
        'ö': 0b11011100,  # ö [œ] or [ø]
        '÷': 0b11111111,  # ÷
        'ø': 0b11011101,  # ø [œ] or [ø]
        'ù': 0b11100001,  # ù
        'ú': 0b11100001,  # ú
        'û': 0b11100001,  # û
        'ü': 0b11100101,  # ü
        'ý': 0b11100101,  # ý
        'þ': 0b00001011,  # þ [ð̠] (represented as a non-plosive T)
        'ÿ': 0b11100101,  # ÿ
    }

    def encode(self, word, max_length=8):
        """Return the eudex phonetic hash of a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length in bits of the code returned (default 8)

        Returns
        -------
        int
            The eudex hash

        Examples
        --------
        >>> pe = Eudex()
        >>> pe.encode('Colin')
        432345564238053650
        >>> pe.encode('Christopher')
        433648490138894409
        >>> pe.encode('Niall')
        648518346341351840
        >>> pe.encode('Smith')
        720575940412906756
        >>> pe.encode('Schmidt')
        720589151732307997

        """
        # Lowercase input & filter unknown characters
        word = ''.join(
            char for char in word.lower() if char in self._initial_phones
        )

        if not word:
            word = '÷'

        # Perform initial eudex coding of each character
        values = [self._initial_phones[word[0]]]
        values += [self._trailing_phones[char] for char in word[1:]]

        # Right-shift by one to determine if second instance should be skipped
        shifted_values = [_ >> 1 for _ in values]
        condensed_values = [values[0]]
        for n in range(1, len(shifted_values)):
            if shifted_values[n] != shifted_values[n - 1]:
                condensed_values.append(values[n])

        # Add padding after first character & trim beyond max_length
        values = (
            [condensed_values[0]]
            + [0] * max(0, max_length - len(condensed_values))
            + condensed_values[1:max_length]
        )

        # Combine individual character values into eudex hash
        hash_value = 0
        for val in values:
            hash_value = (hash_value << 8) | val

        return hash_value


def eudex(word, max_length=8):
    """Return the eudex phonetic hash of a word.

    This is a wrapper for :py:meth:`Eudex.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length in bits of the code returned (default 8)

    Returns
    -------
    int
        The eudex hash

    Examples
    --------
    >>> eudex('Colin')
    432345564238053650
    >>> eudex('Christopher')
    433648490138894409
    >>> eudex('Niall')
    648518346341351840
    >>> eudex('Smith')
    720575940412906756
    >>> eudex('Schmidt')
    720589151732307997

    """
    return Eudex().encode(word, max_length)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
