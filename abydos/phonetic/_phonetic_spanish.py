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

"""abydos.phonetic._phonetic_spanish.

Phonetic Spanish
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['PhoneticSpanish', 'phonetic_spanish']


class PhoneticSpanish(_Phonetic):
    """PhoneticSpanish.

    This follows the coding described in :cite:`Amon:2012` and
    :cite:`delPilarAngeles:2015`.

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip((ord(_) for _ in 'BCDFGHJKLMNPQRSTVXYZ'), '14328287566079431454')
    )

    _uc_set = set('BCDFGHJKLMNPQRSTVXYZ')

    _alphabetic = dict(zip((ord(_) for _ in '0123456789'), 'PBFTSLNKGR'))

    def __init__(self, max_length=-1):
        """Initialize PhoneticSpanish instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to unlimited)


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length

    def encode_alpha(self, word):
        """Return the alphabetic PhoneticSpanish coding of word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic PhoneticSpanish code

        Examples
        --------
        >>> pe = PhoneticSpanish()
        >>> pe.encode_alpha('Perez')
        'PRS'
        >>> pe.encode_alpha('Martinez')
        'NRTNS'
        >>> pe.encode_alpha('Gutierrez')
        'GTRRS'
        >>> pe.encode_alpha('Santiago')
        'SNTG'
        >>> pe.encode_alpha('Nicolás')
        'NSLS'


        .. versionadded:: 0.4.0

        """
        return self.encode(word).translate(self._alphabetic)

    def encode(self, word):
        """Return the PhoneticSpanish coding of word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The PhoneticSpanish code

        Examples
        --------
        >>> pe = PhoneticSpanish()
        >>> pe.encode('Perez')
        '094'
        >>> pe.encode('Martinez')
        '69364'
        >>> pe.encode('Gutierrez')
        '83994'
        >>> pe.encode('Santiago')
        '4638'
        >>> pe.encode('Nicolás')
        '6454'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # uppercase, normalize, and decompose, filter to A-Z minus vowels & W
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)

        # merge repeated Ls & Rs
        word = word.replace('LL', 'L')
        word = word.replace('R', 'R')

        # apply the Soundex algorithm
        sdx = word.translate(self._trans)

        if self._max_length > 0:
            sdx = (sdx + ('0' * self._max_length))[: self._max_length]

        return sdx


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the PhoneticSpanish.encode method instead.',
)
def phonetic_spanish(word, max_length=-1):
    """Return the PhoneticSpanish coding of word.

    This is a wrapper for :py:meth:`PhoneticSpanish.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to unlimited)

    Returns
    -------
    str
        The PhoneticSpanish code

    Examples
    --------
    >>> phonetic_spanish('Perez')
    '094'
    >>> phonetic_spanish('Martinez')
    '69364'
    >>> phonetic_spanish('Gutierrez')
    '83994'
    >>> phonetic_spanish('Santiago')
    '4638'
    >>> phonetic_spanish('Nicolás')
    '6454'

    .. versionadded:: 0.3.0

    """
    return PhoneticSpanish(max_length).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
