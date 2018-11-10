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

"""abydos.stemmer._CLEFSwedish.

CLEF Swedish stemmer
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._Stemmer import _Stemmer

__all__ = ['CLEFSwedish', 'clef_swedish']


class CLEFSwedish(_Stemmer):
    """CLEF Swedish stemmer.

    The CLEF Swedish stemmer is defined at :cite:`Savoy:2005`.
    """

    def stem(self, word):
        """Return CLEF Swedish stem.

        Args:
            word (str): The word to stem

        Returns:
            str: Word stem

        Examples:
            >>> clef_swedish('undervisa')
            'undervis'
            >>> clef_swedish('suspension')
            'suspensio'
            >>> clef_swedish('visshet')
            'viss'

        """
        wlen = len(word) - 1

        if wlen > 3 and word[-1] == 's':
            word = word[:-1]
            wlen -= 1

        if wlen > 6:
            if word[-5:] in {'elser', 'heten'}:
                return word[:-5]
        if wlen > 5:
            if word[-4:] in {
                'arne',
                'erna',
                'ande',
                'else',
                'aste',
                'orna',
                'aren',
            }:
                return word[:-4]
        if wlen > 4:
            if word[-3:] in {'are', 'ast', 'het'}:
                return word[:-3]
        if wlen > 3:
            if word[-2:] in {'ar', 'er', 'or', 'en', 'at', 'te', 'et'}:
                return word[:-2]
        if wlen > 2:
            if word[-1] in {'a', 'e', 'n', 't'}:
                return word[:-1]
        return word


def clef_swedish(word):
    """Return CLEF Swedish stem.

    This is a wrapper for :py:meth:`CLEFSwedish.stem`.

    Args:
        word (str): The word to stem

    Returns:
        str: Word stem

    Examples:
        >>> clef_swedish('undervisa')
        'undervis'
        >>> clef_swedish('suspension')
        'suspensio'
        >>> clef_swedish('visshet')
        'viss'

    """
    return CLEFSwedish().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
