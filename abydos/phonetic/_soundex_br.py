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

"""abydos.phonetic._soundex_br.

SoundexBR
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['SoundexBR', 'soundex_br']


class SoundexBR(_Phonetic):
    """SoundexBR.

    This is based on :cite:`Marcelino:2015`.

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012623010202',
        )
    )

    _alphabetic = dict(zip((ord(_) for _ in '0123456'), 'APKTLNR'))

    def __init__(self, max_length=4, zero_pad=True):
        """Initialize SoundexBR instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length
        self._zero_pad = zero_pad

    def encode_alpha(self, word):
        """Return the alphabetic SoundexBR encoding of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic SoundexBR code

        Examples
        --------
        >>> pe = SoundexBR()
        >>> pe.encode_alpha('Oliveira')
        'OLPR'
        >>> pe.encode_alpha('Almeida')
        'ALNT'
        >>> pe.encode_alpha('Barbosa')
        'BRPK'
        >>> pe.encode_alpha('Araújo')
        'ARK'
        >>> pe.encode_alpha('Gonçalves')
        'GNKL'
        >>> pe.encode_alpha('Goncalves')
        'GNKL'


        .. versionadded:: 0.4.0

        """
        code = self.encode(word).rstrip('0')
        return code[:1] + code[1:].translate(self._alphabetic)

    def encode(self, word):
        """Return the SoundexBR encoding of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The SoundexBR code

        Examples
        --------
        >>> pe = SoundexBR()
        >>> pe.encode('Oliveira')
        'O416'
        >>> pe.encode('Almeida')
        'A453'
        >>> pe.encode('Barbosa')
        'B612'
        >>> pe.encode('Araújo')
        'A620'
        >>> pe.encode('Gonçalves')
        'G524'
        >>> pe.encode('Goncalves')
        'G524'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)

        if word[:2] == 'WA':
            first = 'V'
        elif word[:1] == 'K' and word[1:2] in {'A', 'O', 'U'}:
            first = 'C'
        elif word[:1] == 'C' and word[1:2] in {'I', 'E'}:
            first = 'S'
        elif word[:1] == 'G' and word[1:2] in {'E', 'I'}:
            first = 'J'
        elif word[:1] == 'Y':
            first = 'I'
        elif word[:1] == 'H':
            first = word[1:2]
            word = word[1:]
        else:
            first = word[:1]

        sdx = first + word[1:].translate(self._trans)
        sdx = self._delete_consecutive_repeats(sdx)
        sdx = sdx.replace('0', '')

        if self._zero_pad:
            sdx += '0' * self._max_length

        return sdx[: self._max_length]


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the SoundexBR.encode method instead.',
)
def soundex_br(word, max_length=4, zero_pad=True):
    """Return the SoundexBR encoding of a word.

    This is a wrapper for :py:meth:`SoundexBR.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The SoundexBR code

    Examples
    --------
    >>> soundex_br('Oliveira')
    'O416'
    >>> soundex_br('Almeida')
    'A453'
    >>> soundex_br('Barbosa')
    'B612'
    >>> soundex_br('Araújo')
    'A620'
    >>> soundex_br('Gonçalves')
    'G524'
    >>> soundex_br('Goncalves')
    'G524'

    .. versionadded:: 0.3.0

    """
    return SoundexBR(max_length, zero_pad).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
