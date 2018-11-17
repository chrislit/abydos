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

"""abydos.phonetic._koelner.

Kölner Phonetik
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

from ._phonetic import _Phonetic

__all__ = [
    'Koelner',
    'koelner_phonetik',
    'koelner_phonetik_alpha',
    'koelner_phonetik_num_to_alpha',
]


class Koelner(_Phonetic):
    """Kölner Phonetik.

    Based on the algorithm defined by :cite:`Postel:1969`.
    """

    _uc_v_set = set('AEIOUJY')

    _num_trans = dict(zip((ord(_) for _ in '012345678'), 'APTFKLNRS'))
    _num_set = set('012345678')

    def encode(self, word):
        """Return the Kölner Phonetik (numeric output) code for a word.

        While the output code is numeric, it is still a str because 0s can lead
        the code.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Kölner Phonetik value as a numeric string

        Example
        -------
        >>> pe = Koelner()
        >>> pe.encode('Christopher')
        '478237'
        >>> pe.encode('Niall')
        '65'
        >>> pe.encode('Smith')
        '862'
        >>> pe.encode('Schmidt')
        '862'
        >>> pe.encode('Müller')
        '657'
        >>> pe.encode('Zimmermann')
        '86766'

        """

        def _after(word, pos, letters):
            """Return True if word[pos] follows one of the supplied letters.

            Parameters
            ----------
            word : str
                The word to check
            pos : int
                Position within word to check
            letters : str
                Letters to confirm precede word[pos]

            Returns
            -------
            bool
                True if word[pos] follows a value in letters

            """
            return pos > 0 and word[pos - 1] in letters

        def _before(word, pos, letters):
            """Return True if word[pos] precedes one of the supplied letters.

            Parameters
            ----------
            word : str
                The word to check
            pos : int
                Position within word to check
            letters : str
                Letters to confirm follow word[pos]

            Returns
            -------
            bool
                True if word[pos] precedes a value in letters

            """
            return pos + 1 < len(word) and word[pos + 1] in letters

        sdx = ''

        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')

        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = ''.join(c for c in word if c in self._uc_set)

        # Nothing to convert, return base case
        if not word:
            return sdx

        for i in range(len(word)):
            if word[i] in self._uc_v_set:
                sdx += '0'
            elif word[i] == 'B':
                sdx += '1'
            elif word[i] == 'P':
                if _before(word, i, {'H'}):
                    sdx += '3'
                else:
                    sdx += '1'
            elif word[i] in {'D', 'T'}:
                if _before(word, i, {'C', 'S', 'Z'}):
                    sdx += '8'
                else:
                    sdx += '2'
            elif word[i] in {'F', 'V', 'W'}:
                sdx += '3'
            elif word[i] in {'G', 'K', 'Q'}:
                sdx += '4'
            elif word[i] == 'C':
                if _after(word, i, {'S', 'Z'}):
                    sdx += '8'
                elif i == 0:
                    if _before(
                        word, i, {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'}
                    ):
                        sdx += '4'
                    else:
                        sdx += '8'
                elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                    sdx += '4'
                else:
                    sdx += '8'
            elif word[i] == 'X':
                if _after(word, i, {'C', 'K', 'Q'}):
                    sdx += '8'
                else:
                    sdx += '48'
            elif word[i] == 'L':
                sdx += '5'
            elif word[i] in {'M', 'N'}:
                sdx += '6'
            elif word[i] == 'R':
                sdx += '7'
            elif word[i] in {'S', 'Z'}:
                sdx += '8'

        sdx = self._delete_consecutive_repeats(sdx)

        if sdx:
            sdx = sdx[:1] + sdx[1:].replace('0', '')

        return sdx

    def _to_alpha(self, num):
        """Convert a Kölner Phonetik code from numeric to alphabetic.

        Parameters
        ----------
        num : str or int
            A numeric Kölner Phonetik representation

        Returns
        -------
        str
            An alphabetic representation of the same word

        Examples
        --------
        >>> pe = Koelner()
        >>> pe._to_alpha('862')
        'SNT'
        >>> pe._to_alpha('657')
        'NLR'
        >>> pe._to_alpha('86766')
        'SNRNN'

        """
        num = ''.join(c for c in text_type(num) if c in self._num_set)
        return num.translate(self._num_trans)

    def encode_alpha(self, word):
        """Return the Kölner Phonetik (alphabetic output) code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Kölner Phonetik value as an alphabetic string

        Examples
        --------
        >>> pe = Koelner()
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Schmidt')
        'SNT'
        >>> pe.encode_alpha('Müller')
        'NLR'
        >>> pe.encode_alpha('Zimmermann')
        'SNRNN'

        """
        return koelner_phonetik_num_to_alpha(koelner_phonetik(word))


def koelner_phonetik(word):
    """Return the Kölner Phonetik (numeric output) code for a word.

    This is a wrapper for :py:meth:`Koelner.encode`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    str
        The Kölner Phonetik value as a numeric string

    Example
    -------
    >>> koelner_phonetik('Christopher')
    '478237'
    >>> koelner_phonetik('Niall')
    '65'
    >>> koelner_phonetik('Smith')
    '862'
    >>> koelner_phonetik('Schmidt')
    '862'
    >>> koelner_phonetik('Müller')
    '657'
    >>> koelner_phonetik('Zimmermann')
    '86766'

    """
    return Koelner().encode(word)


def koelner_phonetik_num_to_alpha(num):
    """Convert a Kölner Phonetik code from numeric to alphabetic.

    This is a wrapper for :py:meth:`Koelner._to_alpha`.

    Parameters
    ----------
    num : str or int
        A numeric Kölner Phonetik representation

    Returns
    -------
    str
        An alphabetic representation of the same word

    Examples
    --------
    >>> koelner_phonetik_num_to_alpha('862')
    'SNT'
    >>> koelner_phonetik_num_to_alpha('657')
    'NLR'
    >>> koelner_phonetik_num_to_alpha('86766')
    'SNRNN'

    """
    return Koelner()._to_alpha(num)


def koelner_phonetik_alpha(word):
    """Return the Kölner Phonetik (alphabetic output) code for a word.

    This is a wrapper for :py:meth:`Koelner.encode_alpha`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    str
        The Kölner Phonetik value as an alphabetic string

    Examples
    --------
    >>> koelner_phonetik_alpha('Smith')
    'SNT'
    >>> koelner_phonetik_alpha('Schmidt')
    'SNT'
    >>> koelner_phonetik_alpha('Müller')
    'NLR'
    >>> koelner_phonetik_alpha('Zimmermann')
    'SNRNN'

    """
    return Koelner().encode_alpha(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
