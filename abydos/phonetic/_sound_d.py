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

"""abydos.phonetic._sound_d.

The phonetic._sound_d module implements the SoundD phonetic algorithm.
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._util import _delete_consecutive_repeats

__all__ = ['sound_d']


def sound_d(word, max_length=4):
    """Return the SoundD code.

    SoundD is defined in :cite:`Varol:2012`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :returns: the SoundD code
    :rtype: str

    >>> sound_d('Gough')
    '2000'
    >>> sound_d('pneuma')
    '5500'
    >>> sound_d('knight')
    '5300'
    >>> sound_d('trice')
    '3620'
    >>> sound_d('judge')
    '2200'
    """
    _ref_soundd_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012623010202',
        )
    )

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

    if word[:2] in {'KN', 'GN', 'PN', 'AC', 'WR'}:
        word = word[1:]
    elif word[:1] == 'X':
        word = 'S' + word[1:]
    elif word[:2] == 'WH':
        word = 'W' + word[2:]

    word = word.replace('DGE', '20').replace('DGI', '20').replace('GH', '0')

    word = word.translate(_ref_soundd_translation)
    word = _delete_consecutive_repeats(word)
    word = word.replace('0', '')

    if max_length != -1:
        if len(word) < max_length:
            word += '0' * (max_length - len(word))
        else:
            word = word[:max_length]

    return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
