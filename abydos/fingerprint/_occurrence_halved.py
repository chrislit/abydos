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

"""abydos.fingerprint._occurrence_halved.

Cisłak & Grabowski's occurrence halved fingerprint
"""

from deprecation import deprecated

from ._fingerprint import MOST_COMMON_LETTERS_CG, _Fingerprint
from .. import __version__

__all__ = ['OccurrenceHalved', 'occurrence_halved_fingerprint']


class OccurrenceHalved(_Fingerprint):
    """Occurrence Halved Fingerprint.

    Based on the occurrence halved fingerprint from :cite:`Cislak:2017`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
        """Initialize Count instance.

        Parameters
        ----------
        n_bits : int
            Number of bits in the fingerprint returned
        most_common : list
            The most common tokens in the target language, ordered by frequency


        .. versionadded:: 0.4.0

        """
        super(_Fingerprint, self).__init__()
        self._n_bits = n_bits
        self._most_common = most_common

    def fingerprint(self, word):
        """Return the occurrence halved fingerprint.

        Based on the occurrence halved fingerprint from :cite:`Cislak:2017`.

        Parameters
        ----------
        word : str
            The word to fingerprint
        n_bits : int
            Number of bits in the fingerprint returned
        most_common : list
            The most common tokens in the target language, ordered by frequency

        Returns
        -------
        int
            The occurrence halved fingerprint

        Examples
        --------
        >>> ohf = OccurrenceHalved()
        >>> bin(ohf.fingerprint('hat'))
        '0b1010000000010'
        >>> bin(ohf.fingerprint('niall'))
        '0b10010100000'
        >>> bin(ohf.fingerprint('colin'))
        '0b1001010000'
        >>> bin(ohf.fingerprint('atcg'))
        '0b10100000000000'
        >>> bin(ohf.fingerprint('entreatment'))
        '0b1111010000110000'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        n_bits = self._n_bits
        if n_bits % 2:
            n_bits += 1

        w_len = len(word) // 2
        w_1 = set(word[:w_len])
        w_2 = set(word[w_len:])
        fingerprint = 0

        for letter in self._most_common:
            if n_bits:
                fingerprint <<= 1
                if letter in w_1:
                    fingerprint += 1
                fingerprint <<= 1
                if letter in w_2:
                    fingerprint += 1
                n_bits -= 2
            else:
                break

        if n_bits > 0:
            fingerprint <<= n_bits

        return fingerprint


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the OccurrenceHalved.fingerprint method instead.',
)
def occurrence_halved_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG
):
    """Return the occurrence halved fingerprint.

    This is a wrapper for :py:meth:`OccurrenceHalved.fingerprint`.

    Parameters
    ----------
    word : str
        The word to fingerprint
    n_bits : int
        Number of bits in the fingerprint returned
    most_common : list
        The most common tokens in the target language, ordered by frequency

    Returns
    -------
    int
        The occurrence halved fingerprint

    Examples
    --------
    >>> bin(occurrence_halved_fingerprint('hat'))
    '0b1010000000010'
    >>> bin(occurrence_halved_fingerprint('niall'))
    '0b10010100000'
    >>> bin(occurrence_halved_fingerprint('colin'))
    '0b1001010000'
    >>> bin(occurrence_halved_fingerprint('atcg'))
    '0b10100000000000'
    >>> bin(occurrence_halved_fingerprint('entreatment'))
    '0b1111010000110000'

    .. versionadded:: 0.3.0

    """
    return OccurrenceHalved(n_bits, most_common).fingerprint(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
