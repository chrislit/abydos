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

"""abydos.phonetic._phonetic.

The phonetic._phonetic module implements abstract class Phonetic.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from itertools import groupby


class _Phonetic(object):
    """Abstract Phonetic class."""

    _uc_set = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    _lc_set = set('abcdefghijklmnopqrstuvwxyz')
    _uc_v_set = set('AEIOU')
    _lc_v_set = set('aeiou')
    _uc_vy_set = set('AEIOUY')
    _lc_vy_set = set('aeiouy')

    def _delete_consecutive_repeats(self, word):
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

        """
        return ''.join(char for char, _ in groupby(word))

    def encode(self, word):
        """Encode phonetically.

        Parameters
        ----------
        word : str
            The word to transform

        """
        pass

    def encode_alpha(self, word):
        """Encode phonetically using alphabetic characters.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The word transformed

        """
        return self.encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
