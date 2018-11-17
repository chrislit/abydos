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

"""abydos.phonetic._phonetic_spanish.

Phonetic Spanish
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._phonetic import _Phonetic

__all__ = ['PhoneticSpanish', 'phonetic_spanish']


class PhoneticSpanish(_Phonetic):
    """PhoneticSpanish.

    This follows the coding described in :cite:`Amon:2012` and
    :cite:`delPilarAngeles:2015`.
    """

    _trans = dict(
        zip((ord(_) for _ in 'BCDFGHJKLMNPQRSTVXYZ'), '14328287566079431454')
    )

    _uc_set = set('BCDFGHJKLMNPQRSTVXYZ')

    def encode(self, word, max_length=-1):
        """Return the PhoneticSpanish coding of word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to unlimited)

        Returns
        -------
        str
            The PhoneticSpanish code

        Examples
        --------
        >>> pe = PhoneticSpanish()
        >>> pe.encode('Perez')
        '094'
        >>> pe.encode('Martinez')
        '69364'
        >>> pe.encode('Gutierrez')
        '83994'
        >>> pe.encode('Santiago')
        '4638'
        >>> pe.encode('Nicolás')
        '6454'

        """
        # uppercase, normalize, and decompose, filter to A-Z minus vowels & W
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._uc_set)

        # merge repeated Ls & Rs
        word = word.replace('LL', 'L')
        word = word.replace('R', 'R')

        # apply the Soundex algorithm
        sdx = word.translate(self._trans)

        if max_length > 0:
            sdx = (sdx + ('0' * max_length))[:max_length]

        return sdx


def phonetic_spanish(word, max_length=-1):
    """Return the PhoneticSpanish coding of word.

    This is a wrapper for :py:meth:`PhoneticSpanish.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to unlimited)

    Returns
    -------
    str
        The PhoneticSpanish code

    Examples
    --------
    >>> phonetic_spanish('Perez')
    '094'
    >>> phonetic_spanish('Martinez')
    '69364'
    >>> phonetic_spanish('Gutierrez')
    '83994'
    >>> phonetic_spanish('Santiago')
    '4638'
    >>> phonetic_spanish('Nicolás')
    '6454'

    """
    return PhoneticSpanish().encode(word, max_length)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
