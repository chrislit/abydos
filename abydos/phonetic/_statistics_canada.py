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

"""abydos.phonetic._statistics_canada.

The phonetic._statistics_canada module implements the Statistics Canada
phonetic encoding.
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._util import _delete_consecutive_repeats

__all__ = ['statistics_canada']


def statistics_canada(word, max_length=4):
    """Return the Statistics Canada code for a word.

    The original description of this algorithm could not be located, and
    may only have been specified in an unpublished TR. The coding does not
    appear to be in use by Statistics Canada any longer. In its place, this is
    an implementation of the "Census modified Statistics Canada name coding
    procedure".

    The modified version of this algorithm is described in Appendix B of
     :cite:`Moore:1977`.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 4) of the code to return
    :returns: the Statistics Canada name code value
    :rtype: str

    >>> statistics_canada('Christopher')
    'CHRS'
    >>> statistics_canada('Niall')
    'NL'
    >>> statistics_canada('Smith')
    'SMTH'
    >>> statistics_canada('Schmidt')
    'SCHM'
    """
    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(
        c
        for c in word
        if c
        in {
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
        }
    )
    if not word:
        return ''

    code = word[1:]
    for vowel in {'A', 'E', 'I', 'O', 'U', 'Y'}:
        code = code.replace(vowel, '')
    code = word[0] + code
    code = _delete_consecutive_repeats(code)
    code = code.replace(' ', '')

    return code[:max_length]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
