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

"""abydos.phonetic._soundex_br.

SoundexBR
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

__all__ = ['SoundexBR', 'soundex_br']


class SoundexBR(_Phonetic):
    """SoundexBR.

    This is based on :cite:`Marcelino:2015`.
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012623010202',
        )
    )

    def encode(self, word, max_length=4, zero_pad=True):
        """Return the SoundexBR encoding of a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The SoundexBR code

        Examples
        --------
        >>> soundex_br('Oliveira')
        'O416'
        >>> soundex_br('Almeida')
        'A453'
        >>> soundex_br('Barbosa')
        'B612'
        >>> soundex_br('Araújo')
        'A620'
        >>> soundex_br('Gonçalves')
        'G524'
        >>> soundex_br('Goncalves')
        'G524'

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._uc_set)

        if word[:2] == 'WA':
            first = 'V'
        elif word[:1] == 'K' and word[1:2] in {'A', 'O', 'U'}:
            first = 'C'
        elif word[:1] == 'C' and word[1:2] in {'I', 'E'}:
            first = 'S'
        elif word[:1] == 'G' and word[1:2] in {'E', 'I'}:
            first = 'J'
        elif word[:1] == 'Y':
            first = 'I'
        elif word[:1] == 'H':
            first = word[1:2]
            word = word[1:]
        else:
            first = word[:1]

        sdx = first + word[1:].translate(self._trans)
        sdx = self._delete_consecutive_repeats(sdx)
        sdx = sdx.replace('0', '')

        if zero_pad:
            sdx += '0' * max_length

        return sdx[:max_length]


def soundex_br(word, max_length=4, zero_pad=True):
    """Return the SoundexBR encoding of a word.

    This is a wrapper for :py:meth:`SoundexBR.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The SoundexBR code

    Examples
    --------
    >>> soundex_br('Oliveira')
    'O416'
    >>> soundex_br('Almeida')
    'A453'
    >>> soundex_br('Barbosa')
    'B612'
    >>> soundex_br('Araújo')
    'A620'
    >>> soundex_br('Gonçalves')
    'G524'
    >>> soundex_br('Goncalves')
    'G524'

    """
    return SoundexBR().encode(word, max_length, zero_pad)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
