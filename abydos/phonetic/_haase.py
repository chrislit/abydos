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

"""abydos.phonetic._haase.

Haase Phonetik
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from itertools import product
from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

from ._phonetic import _Phonetic

__all__ = ['Haase', 'haase_phonetik']


class Haase(_Phonetic):
    """Haase Phonetik.

    Based on the algorithm described at :cite:`Prante:2015`.

    Based on the original :cite:`Haase:2000`.
    """

    _uc_v_set = set('AEIJOUY')

    def encode(self, word, primary_only=False):
        """Return the Haase Phonetik (numeric output) code for a word.

        While the output code is numeric, it is nevertheless a str.

        Parameters
        ----------
        word : str
            The word to transform
        primary_only : bool
            If True, only the primary code is returned

        Returns
        -------
        tuple
            The Haase Phonetik value as a numeric string

        Examples
        --------
        >>> pe = Haase()
        >>> pe.encode('Joachim')
        ('9496',)
        >>> pe.encode('Christoph')
        ('4798293', '8798293')
        >>> pe.encode('Jörg')
        ('974',)
        >>> pe.encode('Smith')
        ('8692',)
        >>> pe.encode('Schmidt')
        ('8692', '4692')

        """

        def _after(word, pos, letters):
            """Return True if word[pos] follows one of the supplied letters.

            Parameters
            ----------
            word : str
                Word to modify
            pos : int
                Position to examine
            letters : set
                Letters to check for

            Returns
            -------
            bool
                True if word[pos] follows one of letters

            """
            if pos > 0 and word[pos - 1] in letters:
                return True
            return False

        def _before(word, pos, letters):
            """Return True if word[pos] precedes one of the supplied letters.

            Parameters
            ----------
            word : str
                Word to modify
            pos : int
                Position to examine
            letters : set
                Letters to check for

            Returns
            -------
            bool
                True if word[pos] precedes one of letters

            """
            if pos + 1 < len(word) and word[pos + 1] in letters:
                return True
            return False

        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')

        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = ''.join(c for c in word if c in self._uc_set)

        variants = []
        if primary_only:
            variants = [word]
        else:
            pos = 0
            if word[:2] == 'CH':
                variants.append(('CH', 'SCH'))
                pos += 2
            len_3_vars = {
                'OWN': 'AUN',
                'WSK': 'RSK',
                'SCH': 'CH',
                'GLI': 'LI',
                'AUX': 'O',
                'EUX': 'O',
            }
            while pos < len(word):
                if word[pos : pos + 4] == 'ILLE':
                    variants.append(('ILLE', 'I'))
                    pos += 4
                elif word[pos : pos + 3] in len_3_vars:
                    variants.append(
                        (word[pos : pos + 3], len_3_vars[word[pos : pos + 3]])
                    )
                    pos += 3
                elif word[pos : pos + 2] == 'RB':
                    variants.append(('RB', 'RW'))
                    pos += 2
                elif len(word[pos:]) == 3 and word[pos:] == 'EAU':
                    variants.append(('EAU', 'O'))
                    pos += 3
                elif len(word[pos:]) == 1 and word[pos:] in {'A', 'O'}:
                    if word[pos:] == 'O':
                        variants.append(('O', 'OW'))
                    else:
                        variants.append(('A', 'AR'))
                    pos += 1
                else:
                    variants.append((word[pos],))
                    pos += 1

            variants = [''.join(letters) for letters in product(*variants)]

        def _haase_code(word):
            sdx = ''
            for i in range(len(word)):
                if word[i] in self._uc_v_set:
                    sdx += '9'
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
                            word,
                            i,
                            {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'},
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

            return sdx

        encoded = tuple(_haase_code(word) for word in variants)
        if len(encoded) > 1:
            encoded_set = set()
            encoded_single = []
            for code in encoded:
                if code not in encoded_set:
                    encoded_set.add(code)
                    encoded_single.append(code)
            return tuple(encoded_single)

        return encoded


def haase_phonetik(word, primary_only=False):
    """Return the Haase Phonetik (numeric output) code for a word.

    This is a wrapper for :py:meth:`Haase.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    primary_only : bool
        If True, only the primary code is returned

    Returns
    -------
    tuple
        The Haase Phonetik value as a numeric string

    Examples
    --------
    >>> haase_phonetik('Joachim')
    ('9496',)
    >>> haase_phonetik('Christoph')
    ('4798293', '8798293')
    >>> haase_phonetik('Jörg')
    ('974',)
    >>> haase_phonetik('Smith')
    ('8692',)
    >>> haase_phonetik('Schmidt')
    ('8692', '4692')

    """
    return Haase().encode(word, primary_only)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
