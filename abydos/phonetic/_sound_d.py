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

SoundD phonetic algorithm
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

__all__ = ['SoundD', 'sound_d']


class SoundD(_Phonetic):
    """SoundD code.

    SoundD is defined in :cite:`Varol:2012`.
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012623010202',
        )
    )

    def encode(self, word, max_length=4):
        """Return the SoundD code.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 4)

        Returns
        -------
        str
            The SoundD code

        Examples
        --------
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
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        if word[:2] in {'KN', 'GN', 'PN', 'AC', 'WR'}:
            word = word[1:]
        elif word[:1] == 'X':
            word = 'S' + word[1:]
        elif word[:2] == 'WH':
            word = 'W' + word[2:]

        word = (
            word.replace('DGE', '20').replace('DGI', '20').replace('GH', '0')
        )

        word = word.translate(self._trans)
        word = self._delete_consecutive_repeats(word)
        word = word.replace('0', '')

        if max_length != -1:
            if len(word) < max_length:
                word += '0' * (max_length - len(word))
            else:
                word = word[:max_length]

        return word


def sound_d(word, max_length=4):
    """Return the SoundD code.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)

    Returns
    -------
    str
        The SoundD code

    Examples
    --------
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
    return SoundD().encode(word, max_length)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
