# Copyright 2018-2020 by Christopher C. Little.
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

from deprecation import deprecated

from ._metaphone import Metaphone
from ._phonetic import _Phonetic
from ._phonetic_spanish import PhoneticSpanish
from ._soundex import Soundex
from ._spanish_metaphone import SpanishMetaphone
from .. import __version__

__all__ = ['MetaSoundex', 'metasoundex']


class MetaSoundex(_Phonetic):
    """MetaSoundex.

    This is based on :cite:`Koneru:2017`. Only English ('en') and Spanish
    ('es') languages are supported, as in the original.

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '07430755015866075943077514',
        )
    )

    def __init__(self, lang='en'):
        """Initialize MetaSoundex instance.

        Parameters
        ----------
        lang : str
            Either ``en`` for English or ``es`` for Spanish


        .. versionadded:: 0.4.0

        """
        self._lang = lang
        if lang == 'en':
            self._sdx = Soundex()
            self._meta = Metaphone()
        else:
            self._sdx = PhoneticSpanish()
            self._meta = SpanishMetaphone()

    def encode_alpha(self, word):
        """Return the MetaSoundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The MetaSoundex code

        Examples
        --------
        >>> pe = MetaSoundex()
        >>> pe.encode_alpha('Smith')
        'SN'
        >>> pe.encode_alpha('Waters')
        'WTRK'
        >>> pe.encode_alpha('James')
        'JNK'
        >>> pe.encode_alpha('Schmidt')
        'SNT'
        >>> pe.encode_alpha('Ashcroft')
        'AKRP'

        >>> pe = MetaSoundex(lang='es')
        >>> pe.encode_alpha('Perez')
        'PRS'
        >>> pe.encode_alpha('Martinez')
        'NRTNS'
        >>> pe.encode_alpha('Gutierrez')
        'GTRRS'
        >>> pe.encode_alpha('Santiago')
        'SNTG'
        >>> pe.encode_alpha('Nicolás')
        'NKLS'


        .. versionadded:: 0.4.0

        """
        word = self._sdx.encode_alpha(self._meta.encode_alpha(word))
        return word

    def encode(self, word):
        """Return the MetaSoundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

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

        >>> pe = MetaSoundex(lang='es')
        >>> pe.encode('Perez')
        '094'
        >>> pe.encode('Martinez')
        '69364'
        >>> pe.encode('Gutierrez')
        '83994'
        >>> pe.encode('Santiago')
        '4638'
        >>> pe.encode('Nicolás')
        '6754'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = self._sdx.encode(self._meta.encode(word))
        if self._lang == 'en':
            word = word[0].translate(self._trans) + word[1:]
        return word


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the MetaSoundex.encode method instead.',
)
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

    .. versionadded:: 0.3.0

    """
    return MetaSoundex(lang).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
