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

"""abydos.stemmer._clef.

The stemmer._clef module defines CLEF stemmers for:

    - German
    - German plus
    - Swedish
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize

from six import text_type

from ._stemmer import Stemmer

__all__ = [
    'CLEFGerman',
    'CLEFGermanPlus',
    'CLEFSwedish',
    'clef_german',
    'clef_german_plus',
    'clef_swedish',
]


class CLEFGerman(Stemmer):
    """CLEF German stemmer.

    The CLEF German stemmer is defined at :cite:`Savoy:2005`.
    """

    _umlauts = dict(zip((ord(_) for _ in 'äöü'), 'aou'))

    def stem(self, word):
        """Return CLEF German stem.

        Args:
            word (str): The word to stem

        Returns:
            str: Word stem

        Examples:
            >>> stmr = CLEFGerman()
            >>> stmr.stem('lesen')
            'lese'
            >>> stmr.stem('graues')
            'grau'
            >>> stmr.stem('buchstabieren')
            'buchstabier'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))

        # remove umlauts
        word = word.translate(self._umlauts)

        # remove plurals
        wlen = len(word) - 1

        if wlen > 3:
            if wlen > 5:
                if word[-3:] == 'nen':
                    return word[:-3]
            if wlen > 4:
                if word[-2:] in {'en', 'se', 'es', 'er'}:
                    return word[:-2]
            if word[-1] in {'e', 'n', 'r', 's'}:
                return word[:-1]
        return word


def clef_german(word):
    """Return CLEF German stem.

    This is a wrapper for :py:meth:`CLEFGerman.stem`.

    Args:
        word (str): The word to stem

    Returns:
        str: Word stem

    Examples:
        >>> clef_german('lesen')
        'lese'
        >>> clef_german('graues')
        'grau'
        >>> clef_german('buchstabieren')
        'buchstabier'

    """
    return CLEFGerman().stem(word)


class CLEFGermanPlus(Stemmer):
    """CLEF German stemmer plus.

    The CLEF German stemmer plus is defined at :cite:`Savoy:2005`.
    """

    _st_ending = {'b', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 't'}

    _accents = dict(
        zip((ord(_) for _ in 'äàáâöòóôïìíîüùúû'), 'aaaaooooiiiiuuuu')
    )

    def stem(self, word):
        """Return 'CLEF German stemmer plus' stem.

        Args:
            word (str): The word to stem

        Returns:
            str: Word stem

        Examples:
            >>> stmr = CLEFGermanPlus()
            >>> clef_german_plus('lesen')
            'les'
            >>> clef_german_plus('graues')
            'grau'
            >>> clef_german_plus('buchstabieren')
            'buchstabi'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))

        # remove umlauts
        word = word.translate(self._accents)

        # Step 1
        wlen = len(word) - 1
        if wlen > 4 and word[-3:] == 'ern':
            word = word[:-3]
        elif wlen > 3 and word[-2:] in {'em', 'en', 'er', 'es'}:
            word = word[:-2]
        elif wlen > 2 and (
            word[-1] == 'e'
            or (word[-1] == 's' and word[-2] in self._st_ending)
        ):
            word = word[:-1]

        # Step 2
        wlen = len(word) - 1
        if wlen > 4 and word[-3:] == 'est':
            word = word[:-3]
        elif wlen > 3 and (
            word[-2:] in {'er', 'en'}
            or (word[-2:] == 'st' and word[-3] in self._st_ending)
        ):
            word = word[:-2]

        return word


def clef_german_plus(word):
    """Return 'CLEF German stemmer plus' stem.

    This is a wrapper for :py:meth:`CLEFGermanPlus.stem`.

    Args:
        word (str): The word to stem

    Returns:
        str: Word stem

    Examples:
        >>> stmr = CLEFGermanPlus()
        >>> clef_german_plus('lesen')
        'les'
        >>> clef_german_plus('graues')
        'grau'
        >>> clef_german_plus('buchstabieren')
        'buchstabi'

    """
    return CLEFGermanPlus().stem(word)


class CLEFSwedish(Stemmer):
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
