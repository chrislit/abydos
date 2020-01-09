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

"""abydos.phonetic._lein.

Michigan LEIN (Law Enforcement Information Network) encoding
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['LEIN', 'lein']


class LEIN(_Phonetic):
    """LEIN code.

    This is Michigan LEIN (Law Enforcement Information Network) name coding,
    described in :cite:`Moore:1977`.

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip((ord(_) for _ in 'BCDFGJKLMNPQRSTVXZ'), '451455532245351455')
    )

    _del_trans = {num: None for num in (32, 65, 69, 72, 73, 79, 85, 87, 89)}

    _alphabetic = dict(zip((ord(_) for _ in '12345'), 'TNLPK'))

    def __init__(self, max_length=4, zero_pad=True):
        """Initialize LEIN instance.

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
        """Return the alphabetic LEIN code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic LEIN code

        Examples
        --------
        >>> pe = LEIN()
        >>> pe.encode_alpha('Christopher')
        'CLKT'
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
        """Return the LEIN code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The LEIN code

        Examples
        --------
        >>> pe = LEIN()
        >>> pe.encode('Christopher')
        'C351'
        >>> pe.encode('Niall')
        'N300'
        >>> pe.encode('Smith')
        'S210'
        >>> pe.encode('Schmidt')
        'S521'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)

        code = word[:1]  # Rule 1
        word = word[1:].translate(self._del_trans)  # Rule 2
        word = self._delete_consecutive_repeats(word)  # Rule 3
        code += word.translate(self._trans)  # Rule 4

        if self._zero_pad:
            code += '0' * self._max_length  # Rule 4

        return code[: self._max_length]


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the LEIN.encode method instead.',
)
def lein(word, max_length=4, zero_pad=True):
    """Return the LEIN code for a word.

    This is a wrapper for :py:meth:`LEIN.encode`.

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
        The LEIN code

    Examples
    --------
    >>> lein('Christopher')
    'C351'
    >>> lein('Niall')
    'N300'
    >>> lein('Smith')
    'S210'
    >>> lein('Schmidt')
    'S521'

    .. versionadded:: 0.3.0

    """
    return LEIN(max_length, zero_pad).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
