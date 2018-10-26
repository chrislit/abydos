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

"""abydos.phonetic._nysiis.

The phonetic._nysiis module implements New York State Identification and
Intelligence System (NYSIIS) phonetic encoding.
"""

from __future__ import unicode_literals

from six.moves import range

from ._util import _delete_consecutive_repeats

__all__ = ['nysiis']


def nysiis(word, max_length=6, modified=False):
    """Return the NYSIIS code for a word.

    The New York State Identification and Intelligence System algorithm is
    defined in :cite:`Taft:1970`.

    The modified version of this algorithm is described in Appendix B of
    :cite:`Lynch:1977`.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 6) of the code to return
    :param bool modified: indicates whether to use USDA modified NYSIIS
    :returns: the NYSIIS value
    :rtype: str

    >>> nysiis('Christopher')
    'CRASTA'
    >>> nysiis('Niall')
    'NAL'
    >>> nysiis('Smith')
    'SNAT'
    >>> nysiis('Schmidt')
    'SNAD'

    >>> nysiis('Christopher', max_length=-1)
    'CRASTAFAR'

    >>> nysiis('Christopher', max_length=8, modified=True)
    'CRASTAFA'
    >>> nysiis('Niall', max_length=8, modified=True)
    'NAL'
    >>> nysiis('Smith', max_length=8, modified=True)
    'SNAT'
    >>> nysiis('Schmidt', max_length=8, modified=True)
    'SNAD'
    """
    # Require a max_length of at least 6
    if max_length > -1:
        max_length = max(6, max_length)

    _vowels = {'A', 'E', 'I', 'O', 'U'}

    word = ''.join(c for c in word.upper() if c.isalpha())
    word = word.replace('ß', 'SS')

    # exit early if there are no alphas
    if not word:
        return ''

    original_first_char = word[0]

    if word[:3] == 'MAC':
        word = 'MCC' + word[3:]
    elif word[:2] == 'KN':
        word = 'NN' + word[2:]
    elif word[:1] == 'K':
        word = 'C' + word[1:]
    elif word[:2] in {'PH', 'PF'}:
        word = 'FF' + word[2:]
    elif word[:3] == 'SCH':
        word = 'SSS' + word[3:]
    elif modified:
        if word[:2] == 'WR':
            word = 'RR' + word[2:]
        elif word[:2] == 'RH':
            word = 'RR' + word[2:]
        elif word[:2] == 'DG':
            word = 'GG' + word[2:]
        elif word[:1] in _vowels:
            word = 'A' + word[1:]

    if modified and word[-1:] in {'S', 'Z'}:
        word = word[:-1]

    if (
        word[-2:] == 'EE'
        or word[-2:] == 'IE'
        or (modified and word[-2:] == 'YE')
    ):
        word = word[:-2] + 'Y'
    elif word[-2:] in {'DT', 'RT', 'RD'}:
        word = word[:-2] + 'D'
    elif word[-2:] in {'NT', 'ND'}:
        word = word[:-2] + ('N' if modified else 'D')
    elif modified:
        if word[-2:] == 'IX':
            word = word[:-2] + 'ICK'
        elif word[-2:] == 'EX':
            word = word[:-2] + 'ECK'
        elif word[-2:] in {'JR', 'SR'}:
            return 'ERROR'

    key = word[:1]

    skip = 0
    for i in range(1, len(word)):
        if i >= len(word):
            continue
        elif skip:
            skip -= 1
            continue
        elif word[i : i + 2] == 'EV':
            word = word[:i] + 'AF' + word[i + 2 :]
            skip = 1
        elif word[i] in _vowels:
            word = word[:i] + 'A' + word[i + 1 :]
        elif modified and i != len(word) - 1 and word[i] == 'Y':
            word = word[:i] + 'A' + word[i + 1 :]
        elif word[i] == 'Q':
            word = word[:i] + 'G' + word[i + 1 :]
        elif word[i] == 'Z':
            word = word[:i] + 'S' + word[i + 1 :]
        elif word[i] == 'M':
            word = word[:i] + 'N' + word[i + 1 :]
        elif word[i : i + 2] == 'KN':
            word = word[:i] + 'N' + word[i + 2 :]
        elif word[i] == 'K':
            word = word[:i] + 'C' + word[i + 1 :]
        elif modified and i == len(word) - 3 and word[i : i + 3] == 'SCH':
            word = word[:i] + 'SSA'
            skip = 2
        elif word[i : i + 3] == 'SCH':
            word = word[:i] + 'SSS' + word[i + 3 :]
            skip = 2
        elif modified and i == len(word) - 2 and word[i : i + 2] == 'SH':
            word = word[:i] + 'SA'
            skip = 1
        elif word[i : i + 2] == 'SH':
            word = word[:i] + 'SS' + word[i + 2 :]
            skip = 1
        elif word[i : i + 2] == 'PH':
            word = word[:i] + 'FF' + word[i + 2 :]
            skip = 1
        elif modified and word[i : i + 3] == 'GHT':
            word = word[:i] + 'TTT' + word[i + 3 :]
            skip = 2
        elif modified and word[i : i + 2] == 'DG':
            word = word[:i] + 'GG' + word[i + 2 :]
            skip = 1
        elif modified and word[i : i + 2] == 'WR':
            word = word[:i] + 'RR' + word[i + 2 :]
            skip = 1
        elif word[i] == 'H' and (
            word[i - 1] not in _vowels or word[i + 1 : i + 2] not in _vowels
        ):
            word = word[:i] + word[i - 1] + word[i + 1 :]
        elif word[i] == 'W' and word[i - 1] in _vowels:
            word = word[:i] + word[i - 1] + word[i + 1 :]

        if word[i : i + skip + 1] != key[-1:]:
            key += word[i : i + skip + 1]

    key = _delete_consecutive_repeats(key)

    if key[-1:] == 'S':
        key = key[:-1]
    if key[-2:] == 'AY':
        key = key[:-2] + 'Y'
    if key[-1:] == 'A':
        key = key[:-1]
    if modified and key[:1] == 'A':
        key = original_first_char + key[1:]

    if max_length > 0:
        key = key[:max_length]

    return key


if __name__ == '__main__':
    import doctest

    doctest.testmod()
