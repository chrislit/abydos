# Copyright 2014-2022 by Christopher C. Little.
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

from unicodedata import normalize as unicode_normalize

from ._fingerprint import _Fingerprint

__all__ = ['SkeletonKey']


class SkeletonKey(_Fingerprint):
    """Skeleton Key.

    The skeleton key of a word is defined in :cite:`Pollock:1984`.

    .. versionadded:: 0.3.6
    """

    _vowels = set('AEIOU')
    _letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def fingerprint(self, word: str) -> str:
        """Return the skeleton key.

        Parameters
        ----------
        word : str
            The word to transform into its skeleton key

        Returns
        -------
        str
            The skeleton key

        Examples
        --------
        >>> sk = SkeletonKey()
        >>> sk.fingerprint('The quick brown fox jumped over the lazy dog.')
        'THQCKBRWNFXJMPDVLZYGEUIOA'
        >>> sk.fingerprint('Christopher')
        'CHRSTPIOE'
        >>> sk.fingerprint('Niall')
        'NLIA'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = unicode_normalize('NFKD', word.upper())
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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
