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

"""abydos.fingerprint._occurrence.

Cisłak & Grabowski's occurrence fingerprint
"""

from deprecation import deprecated

from ._fingerprint import MOST_COMMON_LETTERS_CG, _Fingerprint
from .. import __version__

__all__ = ['Occurrence', 'occurrence_fingerprint']


class Occurrence(_Fingerprint):
    """Occurrence Fingerprint.

    Based on the occurrence fingerprint from :cite:`Cislak:2017`.

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
        """Return the occurrence fingerprint.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        int
            The occurrence fingerprint

        Examples
        --------
        >>> of = Occurrence()
        >>> bin(of.fingerprint('hat'))
        '0b110000100000000'
        >>> bin(of.fingerprint('niall'))
        '0b10110000100000'
        >>> bin(of.fingerprint('colin'))
        '0b1110000110000'
        >>> bin(of.fingerprint('atcg'))
        '0b110000000010000'
        >>> bin(of.fingerprint('entreatment'))
        '0b1110010010000100'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        n_bits = self._n_bits
        word = set(word)
        fingerprint = 0

        for letter in self._most_common:
            if letter in word:
                fingerprint += 1
            n_bits -= 1
            if n_bits:
                fingerprint <<= 1
            else:
                break

        n_bits -= 1
        if n_bits > 0:
            fingerprint <<= n_bits

        return fingerprint


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Occurrence.fingerprint method instead.',
)
def occurrence_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG
):
    """Return the occurrence fingerprint.

    This is a wrapper for :py:meth:`Occurrence.fingerprint`.

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
        The occurrence fingerprint

    Examples
    --------
    >>> bin(occurrence_fingerprint('hat'))
    '0b110000100000000'
    >>> bin(occurrence_fingerprint('niall'))
    '0b10110000100000'
    >>> bin(occurrence_fingerprint('colin'))
    '0b1110000110000'
    >>> bin(occurrence_fingerprint('atcg'))
    '0b110000000010000'
    >>> bin(occurrence_fingerprint('entreatment'))
    '0b1110010010000100'

    .. versionadded:: 0.3.0

    """
    return Occurrence(n_bits, most_common).fingerprint(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
