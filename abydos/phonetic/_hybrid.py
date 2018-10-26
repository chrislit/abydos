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

"""abydos.phonetic._hybrid.

The phonetic._hybrid module implements hybrid phonetic algorithms:

    - Oxford Name Compression Algorithm (ONCA)
    - MetaSoundex
"""

from __future__ import unicode_literals

from ._es import phonetic_spanish, spanish_metaphone
from ._metaphone import metaphone
from ._nysiis import nysiis
from ._soundex import soundex

__all__ = ['metasoundex', 'onca']


def onca(word, max_length=4, zero_pad=True):
    """Return the Oxford Name Compression Algorithm (ONCA) code for a word.

    This is the Oxford Name Compression Algorithm, based on :cite:`Gill:1997`.

    I can find no complete description of the "anglicised version of the NYSIIS
    method" identified as the first step in this algorithm, so this is likely
    not a precisely correct implementation, in that it employs the standard
    NYSIIS algorithm.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 5) of the code to return
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the ONCA code
    :rtype: str

    >>> onca('Christopher')
    'C623'
    >>> onca('Niall')
    'N400'
    >>> onca('Smith')
    'S530'
    >>> onca('Schmidt')
    'S530'
    """
    # In the most extreme case, 3 characters of NYSIIS input can be compressed
    # to one character of output, so give it triple the max_length.
    return soundex(
        nysiis(word, max_length=max_length * 3), max_length, zero_pad=zero_pad
    )


def metasoundex(word, lang='en'):
    """Return the MetaSoundex code for a word.

    This is based on :cite:`Koneru:2017`. Only English ('en') and Spanish
    ('es') languages are supported, as in the original.

    :param str word: the word to transform
    :param str lang: either 'en' for English or 'es' for Spanish
    :returns: the MetaSoundex code
    :rtype: str

    >>> metasoundex('Smith')
    '4500'
    >>> metasoundex('Waters')
    '7362'
    >>> metasoundex('James')
    '1520'
    >>> metasoundex('Schmidt')
    '4530'
    >>> metasoundex('Ashcroft')
    '0261'
    >>> metasoundex('Perez', lang='es')
    '094'
    >>> metasoundex('Martinez', lang='es')
    '69364'
    >>> metasoundex('Gutierrez', lang='es')
    '83994'
    >>> metasoundex('Santiago', lang='es')
    '4638'
    >>> metasoundex('Nicolás', lang='es')
    '6754'
    """
    _metasoundex_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '07430755015866075943077514',
        )
    )

    if lang == 'es':
        return phonetic_spanish(spanish_metaphone(word))

    word = soundex(metaphone(word))
    word = word[0].translate(_metasoundex_translation) + word[1:]

    return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
