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

"""abydos.fingerprint._skeleton_key.

skeleton key
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._fingerprint import Fingerprint

__all__ = ['SkeletonKey', 'skeleton_key']


class SkeletonKey(Fingerprint):
    """Skeleton Key.

    The skeleton key of a word is defined in :cite:`Pollock:1984`.
    """

    _vowels = set('AEIOU')
    _letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def fingerprint(self, word):
        """Return the skeleton key.

        Args:
            word (str): The word to transform into its skeleton key

        Returns:
            str: The skeleton key

        Examples:
            >>> sk = SkeletonKey()
            >>> sk.fingerprint('The quick brown fox jumped over the lazy dog.')
            'THQCKBRWNFXJMPDVLZYGEUIOA'
            >>> sk.fingerprint('Christopher')
            'CHRSTPIOE'
            >>> sk.fingerprint('Niall')
            'NLIA'

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._letters)
        start = word[0:1]
        consonant_part = ''
        vowel_part = ''

        # add consonants & vowels to to separate strings
        # (omitting the first char & duplicates)
        for char in word[1:]:
            if char != start:
                if char in self._vowels:
                    if char not in vowel_part:
                        vowel_part += char
                elif char not in consonant_part:
                    consonant_part += char
        # return the first char followed by consonants followed by vowels
        return start + consonant_part + vowel_part


def skeleton_key(word):
    """Return the skeleton key.

    This is a wrapper for :py:meth:`SkeletonKey.fingerprint`.

    Args:
        word (str): The word to transform into its skeleton key

    Returns:
        str: The skeleton key

    Examples:
        >>> skeleton_key('The quick brown fox jumped over the lazy dog.')
        'THQCKBRWNFXJMPDVLZYGEUIOA'
        >>> skeleton_key('Christopher')
        'CHRSTPIOE'
        >>> skeleton_key('Niall')
        'NLIA'

    """
    return SkeletonKey().fingerprint(word)


class OmissionKey(Fingerprint):
    """Omission Key.

    The omission key of a word is defined in :cite:`Pollock:1984`.
    """

    _consonants = tuple('JKQXZVWYBFMGPDHCLNTSR')
    _letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def fingerprint(self, word):
        """Return the omission key.

        Args:
            word (str): The word to transform into its omission key

        Returns:
            str: The omission key

        Examples:
            >>> ok = OmissionKey()
            >>> ok.fingerprint('The quick brown fox jumped over the lazy dog.')
            'JKQXZVWYBFMGPDHCLNTREUIOA'
            >>> ok.fingerprint('Christopher')
            'PHCTSRIOE'
            >>> ok.fingerprint('Niall')
            'LNIA'

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._letters)

        key = ''

        # add consonants in order supplied by _consonants (no duplicates)
        for char in self._consonants:
            if char in word:
                key += char

        # add vowels in order they appeared in the word (no duplicates)
        for char in word:
            if char not in self._consonants and char not in key:
                key += char

        return key


if __name__ == '__main__':
    import doctest

    doctest.testmod()