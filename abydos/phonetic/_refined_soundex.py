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

"""abydos.phonetic._refined_soundex.

Refined Soundex
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

__all__ = ['RefinedSoundex', 'refined_soundex']


class RefinedSoundex(_Phonetic):
    """Refined Soundex.

    This is Soundex, but with more character classes. It was defined at
    :cite:`Boyce:1998`.
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01360240043788015936020505',
        )
    )

    def encode(self, word, max_length=-1, zero_pad=False, retain_vowels=False):
        """Return the Refined Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to unlimited)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string
        retain_vowels : bool
            Retain vowels (as 0) in the resulting code

        Returns
        -------
        str
            The Refined Soundex value

        Examples
        --------
        >>> pe = RefinedSoundex()
        >>> pe.encode('Christopher')
        'C393619'
        >>> pe.encode('Niall')
        'N87'
        >>> pe.encode('Smith')
        'S386'
        >>> pe.encode('Schmidt')
        'S386'

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        # apply the Soundex algorithm
        sdx = word[:1] + word.translate(self._trans)
        sdx = self._delete_consecutive_repeats(sdx)
        if not retain_vowels:
            sdx = sdx.replace('0', '')  # Delete vowels, H, W, Y

        if max_length > 0:
            if zero_pad:
                sdx += '0' * max_length
            sdx = sdx[:max_length]

        return sdx


def refined_soundex(word, max_length=-1, zero_pad=False, retain_vowels=False):
    """Return the Refined Soundex code for a word.

    This is a wrapper for :py:meth:`RefinedSoundex.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to unlimited)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string
    retain_vowels : bool
        Retain vowels (as 0) in the resulting code

    Returns
    -------
    str
        The Refined Soundex value

    Examples
    --------
    >>> refined_soundex('Christopher')
    'C393619'
    >>> refined_soundex('Niall')
    'N87'
    >>> refined_soundex('Smith')
    'S386'
    >>> refined_soundex('Schmidt')
    'S386'

    """
    return RefinedSoundex().encode(word, max_length, zero_pad, retain_vowels)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
