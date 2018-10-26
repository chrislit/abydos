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

"""abydos.phonetic._russell.

The phonetic._russell module implements Robert C. Russell's Index.
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._util import _delete_consecutive_repeats

__all__ = [
    'russell_index',
    'russell_index_alpha',
    'russell_index_num_to_alpha',
]


def russell_index(word):
    """Return the Russell Index (integer output) of a word.

    This follows Robert C. Russell's Index algorithm, as described in
    :cite:`Russell:1917`.

    :param str word: the word to transform
    :returns: the Russell Index value
    :rtype: int

    >>> russell_index('Christopher')
    3813428
    >>> russell_index('Niall')
    715
    >>> russell_index('Smith')
    3614
    >>> russell_index('Schmidt')
    3614
    """
    _russell_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGIKLMNOPQRSTUVXYZ'),
            '12341231356712383412313',
        )
    )

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = word.replace('GH', '')  # discard gh (rule 3)
    word = word.rstrip('SZ')  # discard /[sz]$/ (rule 3)

    # translate according to Russell's mapping
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
            'I',
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
            'X',
            'Y',
            'Z',
        }
    )
    sdx = word.translate(_russell_translation)

    # remove any 1s after the first occurrence
    one = sdx.find('1') + 1
    if one:
        sdx = sdx[:one] + ''.join(c for c in sdx[one:] if c != '1')

    # remove repeating characters
    sdx = _delete_consecutive_repeats(sdx)

    # return as an int
    return int(sdx) if sdx else float('NaN')


def russell_index_num_to_alpha(num):
    """Convert the Russell Index integer to an alphabetic string.

    This follows Robert C. Russell's Index algorithm, as described in
    :cite:`Russell:1917`.

    :param int num: a Russell Index integer value
    :returns: the Russell Index as an alphabetic string
    :rtype: str

    >>> russell_index_num_to_alpha(3813428)
    'CRACDBR'
    >>> russell_index_num_to_alpha(715)
    'NAL'
    >>> russell_index_num_to_alpha(3614)
    'CMAD'
    """
    _russell_num_translation = dict(
        zip((ord(_) for _ in '12345678'), 'ABCDLMNR')
    )
    num = ''.join(
        c
        for c in text_type(num)
        if c in {'1', '2', '3', '4', '5', '6', '7', '8'}
    )
    if num:
        return num.translate(_russell_num_translation)
    return ''


def russell_index_alpha(word):
    """Return the Russell Index (alphabetic output) for the word.

    This follows Robert C. Russell's Index algorithm, as described in
    :cite:`Russell:1917`.

    :param str word: the word to transform
    :returns: the Russell Index value as an alphabetic string
    :rtype: str

    >>> russell_index_alpha('Christopher')
    'CRACDBR'
    >>> russell_index_alpha('Niall')
    'NAL'
    >>> russell_index_alpha('Smith')
    'CMAD'
    >>> russell_index_alpha('Schmidt')
    'CMAD'
    """
    if word:
        return russell_index_num_to_alpha(russell_index(word))
    return ''


if __name__ == '__main__':
    import doctest

    doctest.testmod()
