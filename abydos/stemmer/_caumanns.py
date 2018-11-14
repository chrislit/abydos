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

"""abydos.stemmer._caumanns.

Caumanns German stemmer
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize

from six import text_type
from six.moves import range

from ._stemmer import _Stemmer

__all__ = ['Caumanns', 'caumanns']


class Caumanns(_Stemmer):
    """Caumanns stemmer.

    Jörg Caumanns' stemmer is described in his article in
    :cite:`Caumanns:1999`.

    This implementation is based on the GermanStemFilter described at
    :cite:`Lang:2013`.
    """

    _umlauts = dict(zip((ord(_) for _ in 'äöü'), 'aou'))

    def stem(self, word):
        """Return Caumanns German stem.

        Parameters
        ----------
        word : str
            The word to stem

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = Caumanns()
        >>> stmr.stem('lesen')
        'les'
        >>> stmr.stem('graues')
        'grau'
        >>> stmr.stem('buchstabieren')
        'buchstabier'

        """
        if not word:
            return ''

        upper_initial = word[0].isupper()
        word = normalize('NFC', text_type(word.lower()))

        # # Part 2: Substitution
        # 1. Change umlauts to corresponding vowels & ß to ss
        word = word.translate(self._umlauts)
        word = word.replace('ß', 'ss')

        # 2. Change second of doubled characters to *
        new_word = word[0]
        for i in range(1, len(word)):
            if new_word[i - 1] == word[i]:
                new_word += '*'
            else:
                new_word += word[i]
        word = new_word

        # 3. Replace sch, ch, ei, ie with $, §, %, &
        word = word.replace('sch', '$')
        word = word.replace('ch', '§')
        word = word.replace('ei', '%')
        word = word.replace('ie', '&')
        word = word.replace('ig', '#')
        word = word.replace('st', '!')

        # # Part 1: Recursive Context-Free Stripping
        # 1. Remove the following 7 suffixes recursively
        while len(word) > 3:
            if (len(word) > 4 and word[-2:] in {'em', 'er'}) or (
                len(word) > 5 and word[-2:] == 'nd'
            ):
                word = word[:-2]
            elif (word[-1] in {'e', 's', 'n'}) or (
                not upper_initial and word[-1] in {'t', '!'}
            ):
                word = word[:-1]
            else:
                break

        # Additional optimizations:
        if len(word) > 5 and word[-5:] == 'erin*':
            word = word[:-1]
        if word[-1] == 'z':
            word = word[:-1] + 'x'

        # Reverse substitutions:
        word = word.replace('$', 'sch')
        word = word.replace('§', 'ch')
        word = word.replace('%', 'ei')
        word = word.replace('&', 'ie')
        word = word.replace('#', 'ig')
        word = word.replace('!', 'st')

        # Expand doubled
        word = ''.join(
            [word[0]]
            + [
                word[i - 1] if word[i] == '*' else word[i]
                for i in range(1, len(word))
            ]
        )

        # Finally, convert gege to ge
        if len(word) > 4:
            word = word.replace('gege', 'ge', 1)

        return word


def caumanns(word):
    """Return Caumanns German stem.

    This is a wrapper for :py:meth:`Caumanns.stem`.

    Parameters
    ----------
    word : str
        The word to stem

    Returns
    -------
    str
        Word stem

    Examples
    --------
    >>> caumanns('lesen')
    'les'
    >>> caumanns('graues')
    'grau'
    >>> caumanns('buchstabieren')
    'buchstabier'

    """
    return Caumanns().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
