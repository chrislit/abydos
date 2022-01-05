# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.phonetic._phonetic.

The phonetic._phonetic module implements abstract class Phonetic.
"""

from itertools import groupby

__all__ = ['_Phonetic']


class _Phonetic:
    """Abstract Phonetic class.

    .. versionadded:: 0.3.6
    """

    _uc_set = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    _lc_set = set('abcdefghijklmnopqrstuvwxyz')
    _uc_v_set = set('AEIOU')
    _lc_v_set = set('aeiou')
    _uc_vy_set = set('AEIOUY')
    _lc_vy_set = set('aeiouy')

    def _delete_consecutive_repeats(self, word: str) -> str:
        """Delete consecutive repeated characters in a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            Word with consecutive repeating characters collapsed to a single
            instance

        Examples
        --------
        >>> pe = _Phonetic()
        >>> pe._delete_consecutive_repeats('REDDEE')
        'REDE'
        >>> pe._delete_consecutive_repeats('AEIOU')
        'AEIOU'
        >>> pe._delete_consecutive_repeats('AAACCCTTTGGG')
        'ACTG'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return ''.join(char for char, _ in groupby(word))

    def encode(self, word: str) -> str:
        """Encode phonetically.

        Parameters
        ----------
        word : str
            The word to transform


        .. versionadded:: 0.3.6

        """
        return word

    def encode_alpha(self, word: str) -> str:
        """Encode phonetically using alphabetic characters.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The word transformed


        .. versionadded:: 0.3.6

        """
        return self.encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
