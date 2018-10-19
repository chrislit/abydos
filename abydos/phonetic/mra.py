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

"""abydos.phonetic.mra.

The phonetic.mra module implements the MRA personal numeric identifier (PNI).
"""

from __future__ import unicode_literals


from . import _delete_consecutive_repeats

__all__ = ['mra']


def mra(word):
    """Return the MRA personal numeric identifier (PNI) for a word.

    A description of the Western Airlines Surname Match Rating Algorithm can
    be found on page 18 of :cite:`Moore:1977`.

    :param str word: the word to transform
    :returns: the MRA PNI
    :rtype: str

    >>> mra('Christopher')
    'CHRPHR'
    >>> mra('Niall')
    'NL'
    >>> mra('Smith')
    'SMTH'
    >>> mra('Schmidt')
    'SCHMDT'
    """
    if not word:
        return word
    word = word.upper()
    word = word.replace('ß', 'SS')
    word = word[0]+''.join(c for c in word[1:] if
                           c not in {'A', 'E', 'I', 'O', 'U'})
    word = _delete_consecutive_repeats(word)
    if len(word) > 6:
        word = word[:3]+word[-3:]
    return word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
