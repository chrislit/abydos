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

"""abydos.phonetic._alpha_sis.

The phonetic._alpha_sis module implements IBM's Alpha Search Inquiry System
coding.
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

__all__ = ['alpha_sis']


def alpha_sis(word, max_length=14):
    """Return the IBM Alpha Search Inquiry System code for a word.

    The Alpha Search Inquiry System code is defined in :cite:`IBM:1973`.
    This implementation is based on the description in :cite:`Moore:1977`.

    A collection is necessary since there can be multiple values for a
    single word. But the collection must be ordered since the first value
    is the primary coding.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 14)
    :returns: the Alpha SIS value
    :rtype: tuple

    >>> alpha_sis('Christopher')
    ('06401840000000', '07040184000000', '04018400000000')
    >>> alpha_sis('Niall')
    ('02500000000000',)
    >>> alpha_sis('Smith')
    ('03100000000000',)
    >>> alpha_sis('Schmidt')
    ('06310000000000',)
    """
    _alpha_sis_initials = {
        'GF': '08',
        'GM': '03',
        'GN': '02',
        'KN': '02',
        'PF': '08',
        'PN': '02',
        'PS': '00',
        'WR': '04',
        'A': '1',
        'E': '1',
        'H': '2',
        'I': '1',
        'J': '3',
        'O': '1',
        'U': '1',
        'W': '4',
        'Y': '5',
    }
    _alpha_sis_initials_order = (
        'GF',
        'GM',
        'GN',
        'KN',
        'PF',
        'PN',
        'PS',
        'WR',
        'A',
        'E',
        'H',
        'I',
        'J',
        'O',
        'U',
        'W',
        'Y',
    )
    _alpha_sis_basic = {
        'SCH': '6',
        'CZ': ('70', '6', '0'),
        'CH': ('6', '70', '0'),
        'CK': ('7', '6'),
        'DS': ('0', '10'),
        'DZ': ('0', '10'),
        'TS': ('0', '10'),
        'TZ': ('0', '10'),
        'CI': '0',
        'CY': '0',
        'CE': '0',
        'SH': '6',
        'DG': '7',
        'PH': '8',
        'C': ('7', '6'),
        'K': ('7', '6'),
        'Z': '0',
        'S': '0',
        'D': '1',
        'T': '1',
        'N': '2',
        'M': '3',
        'R': '4',
        'L': '5',
        'J': '6',
        'G': '7',
        'Q': '7',
        'X': '7',
        'F': '8',
        'V': '8',
        'B': '9',
        'P': '9',
    }
    _alpha_sis_basic_order = (
        'SCH',
        'CZ',
        'CH',
        'CK',
        'DS',
        'DZ',
        'TS',
        'TZ',
        'CI',
        'CY',
        'CE',
        'SH',
        'DG',
        'PH',
        'C',
        'K',
        'Z',
        'S',
        'D',
        'T',
        'N',
        'M',
        'R',
        'L',
        'J',
        'C',
        'G',
        'K',
        'Q',
        'X',
        'F',
        'V',
        'B',
        'P',
    )

    alpha = ['']
    pos = 0
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

    # Clamp max_length to [4, 64]
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    # Do special processing for initial substrings
    for k in _alpha_sis_initials_order:
        if word.startswith(k):
            alpha[0] += _alpha_sis_initials[k]
            pos += len(k)
            break

    # Add a '0' if alpha is still empty
    if not alpha[0]:
        alpha[0] += '0'

    # Whether or not any special initial codes were encoded, iterate
    # through the length of the word in the main encoding loop
    while pos < len(word):
        orig_pos = pos
        for k in _alpha_sis_basic_order:
            if word[pos:].startswith(k):
                if isinstance(_alpha_sis_basic[k], tuple):
                    newalpha = []
                    for i in range(len(_alpha_sis_basic[k])):
                        newalpha += [_ + _alpha_sis_basic[k][i] for _ in alpha]
                    alpha = newalpha
                else:
                    alpha = [_ + _alpha_sis_basic[k] for _ in alpha]
                pos += len(k)
                break
        if pos == orig_pos:
            alpha = [_ + '_' for _ in alpha]
            pos += 1

    # Trim doublets and placeholders
    for i in range(len(alpha)):
        pos = 1
        while pos < len(alpha[i]):
            if alpha[i][pos] == alpha[i][pos - 1]:
                alpha[i] = alpha[i][:pos] + alpha[i][pos + 1 :]
            pos += 1
    alpha = (_.replace('_', '') for _ in alpha)

    # Trim codes and return tuple
    alpha = ((_ + ('0' * max_length))[:max_length] for _ in alpha)
    return tuple(alpha)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
