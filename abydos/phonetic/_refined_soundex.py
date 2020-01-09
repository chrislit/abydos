# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.phonetic._refined_soundex.

Refined Soundex
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['RefinedSoundex', 'refined_soundex']


class RefinedSoundex(_Phonetic):
    """Refined Soundex.

    This is Soundex, but with more character classes. It was defined at
    :cite:`Boyce:1998`.

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01360240043788015936020505',
        )
    )

    _alphabetic = dict(zip((ord(_) for _ in '123456789'), 'PFKGZTLNR'))

    def __init__(self, max_length=-1, zero_pad=False, retain_vowels=False):
        """Initialize RefinedSoundex instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to unlimited)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string
        retain_vowels : bool
            Retain vowels (as 0) in the resulting code


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length
        self._zero_pad = zero_pad
        self._retain_vowels = retain_vowels

    def encode_alpha(self, word):
        """Return the alphabetic Refined Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Refined Soundex value

        Examples
        --------
        >>> pe = RefinedSoundex()
        >>> pe.encode_alpha('Christopher')
        'CRKTPR'
        >>> pe.encode_alpha('Niall')
        'NL'
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Schmidt')
        'SKNT'


        .. versionadded:: 0.4.0

        """
        code = self.encode(word).rstrip('0')
        return code[:1] + code[1:].translate(self._alphabetic)

    def encode(self, word):
        """Return the Refined Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Refined Soundex value

        Examples
        --------
        >>> pe = RefinedSoundex()
        >>> pe.encode('Christopher')
        'C93619'
        >>> pe.encode('Niall')
        'N7'
        >>> pe.encode('Smith')
        'S86'
        >>> pe.encode('Schmidt')
        'S386'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)

        # apply the Soundex algorithm
        sdx = word[:1] + word[1:].translate(self._trans)
        sdx = self._delete_consecutive_repeats(sdx)
        if not self._retain_vowels:
            sdx = sdx.replace('0', '')  # Delete vowels, H, W, Y

        if self._max_length > 0:
            if self._zero_pad:
                sdx += '0' * self._max_length
            sdx = sdx[: self._max_length]

        return sdx


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the RefinedSoundex.encode method instead.',
)
def refined_soundex(word, max_length=-1, zero_pad=False, retain_vowels=False):
    """Return the Refined Soundex code for a word.

    This is a wrapper for :py:meth:`RefinedSoundex.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to unlimited)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string
    retain_vowels : bool
        Retain vowels (as 0) in the resulting code

    Returns
    -------
    str
        The Refined Soundex value

    Examples
    --------
    >>> refined_soundex('Christopher')
    'C93619'
    >>> refined_soundex('Niall')
    'N7'
    >>> refined_soundex('Smith')
    'S86'
    >>> refined_soundex('Schmidt')
    'S386'

    .. versionadded:: 0.3.0

    """
    return RefinedSoundex(max_length, zero_pad, retain_vowels).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
