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

"""abydos.phonetic._onca.

Oxford Name Compression Algorithm (ONCA)
"""

from deprecation import deprecated

from ._nysiis import NYSIIS
from ._phonetic import _Phonetic
from ._soundex import Soundex
from .. import __version__

__all__ = ['ONCA', 'onca']


class ONCA(_Phonetic):
    """Oxford Name Compression Algorithm (ONCA).

    This is the Oxford Name Compression Algorithm, based on :cite:`Gill:1997`.

    I can find no complete description of the "anglicised version of the NYSIIS
    method" identified as the first step in this algorithm, so this is likely
    not a precisely correct implementation, in that it employs the standard
    NYSIIS algorithm.

    .. versionadded:: 0.3.6
    """

    def __init__(self, max_length=4, zero_pad=True):
        """Initialize ONCA instance.

        Parameters
        ----------
        max_length : int
            The maximum length (default 5) of the code to return
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string


        .. versionadded:: 0.4.0

        """
        self._nysiis = NYSIIS(max_length=max_length * 3)
        self._soundex = Soundex(max_length=max_length, zero_pad=zero_pad)

    def encode_alpha(self, word):
        """Return the alphabetic ONCA code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic ONCA code

        Examples
        --------
        >>> pe = ONCA()
        >>> pe.encode_alpha('Christopher')
        'CRKT'
        >>> pe.encode_alpha('Niall')
        'NL'
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Schmidt')
        'SNT'


        .. versionadded:: 0.4.0

        """
        return self._soundex.encode_alpha(self._nysiis.encode_alpha(word))

    def encode(self, word):
        """Return the Oxford Name Compression Algorithm (ONCA) code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The ONCA code

        Examples
        --------
        >>> pe = ONCA()
        >>> pe.encode('Christopher')
        'C623'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Schmidt')
        'S530'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # In the most extreme case, 3 characters of NYSIIS input can be
        # compressed to one character of output, so give it triple the
        # max_length.
        return self._soundex.encode(self._nysiis.encode(word))


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the ONCA.encode method instead.',
)
def onca(word, max_length=4, zero_pad=True):
    """Return the Oxford Name Compression Algorithm (ONCA) code for a word.

    This is a wrapper for :py:meth:`ONCA.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The maximum length (default 5) of the code to return
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The ONCA code

    Examples
    --------
    >>> onca('Christopher')
    'C623'
    >>> onca('Niall')
    'N400'
    >>> onca('Smith')
    'S530'
    >>> onca('Schmidt')
    'S530'

    .. versionadded:: 0.3.0

    """
    return ONCA(max_length, zero_pad).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
