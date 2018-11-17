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

"""abydos.fingerprint._fingerprint.

The fingerprint._Fingerprint module implements abstract class Fingerprint
and defines contants for most common letters.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

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
# German n-grams, among letters (A-Z, a-z, umlauted vowels & ) & digits
# 0-9
MOST_COMMON_LETTERS_DE_LC = ('e', 'n', 'i', 'r', 's', 't', 'a', 'd', 'h', 'u',
                             'l', 'c', 'g', 'o', 'm', 'b', 'f', 'w', 'k', 'z',
                             'v', 'p', 'ü', 'ä', 'S', 'A', 'D', 'B', 'E', 'G',
                             'M', 'ß', 'V', 'K', 'ö', 'W', 'F', 'P', 'R', 'I',
                             'H', 'L', 'T', 'N', 'Z', 'y', 'U', 'j', 'J', 'O',
                             'C', 'x', 'q', 'Ü', 'Q', 'X', 'Ä', 'Ö', '1', '2',
                             'Y', '3', '4', '0', '5', '6', '9', '8', '7')
# fmt: on


class _Fingerprint(object):
    """Abstract _Fingerprint class."""

    def fingerprint(self, word):
        """Fingerprint string.

        Parameters
        ----------
        word : str
            Word to fingerprint

        """
        pass


__all__ = [
    MOST_COMMON_LETTERS,
    MOST_COMMON_LETTERS_CG,
    MOST_COMMON_LETTERS_DE,
    MOST_COMMON_LETTERS_DE_LC,
    MOST_COMMON_LETTERS_EN_LC,
]

if __name__ == '__main__':
    import doctest

    doctest.testmod()
