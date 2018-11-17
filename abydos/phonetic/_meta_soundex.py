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

"""abydos.phonetic._meta_soundex.

MetaSoundex
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._metaphone import Metaphone
from ._phonetic import _Phonetic
from ._phonetic_spanish import PhoneticSpanish
from ._soundex import Soundex
from ._spanish_metaphone import SpanishMetaphone

__all__ = ['MetaSoundex', 'metasoundex']


class MetaSoundex(_Phonetic):
    """MetaSoundex.

    This is based on :cite:`Koneru:2017`. Only English ('en') and Spanish
    ('es') languages are supported, as in the original.
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '07430755015866075943077514',
        )
    )
    _phonetic_spanish = PhoneticSpanish()
    _spanish_metaphone = SpanishMetaphone()
    _metaphone = Metaphone()
    _soundex = Soundex()

    def encode(self, word, lang='en'):
        """Return the MetaSoundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        lang : str
            Either ``en`` for English or ``es`` for Spanish

        Returns
        -------
        str
            The MetaSoundex code

        Examples
        --------
        >>> pe = MetaSoundex()
        >>> pe.encode('Smith')
        '4500'
        >>> pe.encode('Waters')
        '7362'
        >>> pe.encode('James')
        '1520'
        >>> pe.encode('Schmidt')
        '4530'
        >>> pe.encode('Ashcroft')
        '0261'
        >>> pe.encode('Perez', lang='es')
        '094'
        >>> pe.encode('Martinez', lang='es')
        '69364'
        >>> pe.encode('Gutierrez', lang='es')
        '83994'
        >>> pe.encode('Santiago', lang='es')
        '4638'
        >>> pe.encode('Nicolás', lang='es')
        '6754'

        """
        if lang == 'es':
            return self._phonetic_spanish.encode(
                self._spanish_metaphone.encode(word)
            )

        word = self._soundex.encode(self._metaphone.encode(word))
        word = word[0].translate(self._trans) + word[1:]
        return word


def metasoundex(word, lang='en'):
    """Return the MetaSoundex code for a word.

    This is a wrapper for :py:meth:`MetaSoundex.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    lang : str
        Either ``en`` for English or ``es`` for Spanish

    Returns
    -------
    str
        The MetaSoundex code

    Examples
    --------
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
    return MetaSoundex().encode(word, lang)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
