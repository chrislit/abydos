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

"""abydos.phonetic._parmar_kumbharana.

The phonetic._parmar_kumbharana module implements the Parmar-Kumbharana
phonetic algorithm.
"""

from __future__ import unicode_literals

from six.moves import range

from ._util import _delete_consecutive_repeats

__all__ = ['parmar_kumbharana']


def parmar_kumbharana(word):
    """Return the Parmar-Kumbharana encoding of a word.

    This is based on the phonetic algorithm proposed in :cite:`Parmar:2014`.

    :param str word: the word to transform
    :returns: the Parmar-Kumbharana encoding
    :rtype: str

    >>> parmar_kumbharana('Gough')
    'GF'
    >>> parmar_kumbharana('pneuma')
    'NM'
    >>> parmar_kumbharana('knight')
    'NT'
    >>> parmar_kumbharana('trice')
    'TRS'
    >>> parmar_kumbharana('judge')
    'JJ'
    """
    rule_table = {
        4: {'OUGH': 'F'},
        3: {'DGE': 'J', 'OUL': 'U', 'GHT': 'T'},
        2: {
            'CE': 'S',
            'CI': 'S',
            'CY': 'S',
            'GE': 'J',
            'GI': 'J',
            'GY': 'J',
            'WR': 'R',
            'GN': 'N',
            'KN': 'N',
            'PN': 'N',
            'CK': 'K',
            'SH': 'S',
        },
    }
    vowel_trans = {65: '', 69: '', 73: '', 79: '', 85: '', 89: ''}

    word = word.upper()  # Rule 3
    word = _delete_consecutive_repeats(word)  # Rule 4

    # Rule 5
    i = 0
    while i < len(word):
        for match_len in range(4, 1, -1):
            if word[i : i + match_len] in rule_table[match_len]:
                repl = rule_table[match_len][word[i : i + match_len]]
                word = word[:i] + repl + word[i + match_len :]
                i += len(repl)
                break
        else:
            i += 1

    word = word[:1] + word[1:].translate(vowel_trans)  # Rule 6
    return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
