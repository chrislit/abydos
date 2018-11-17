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

"""abydos.fingerprint._occurrence_halved.

Cisłak & Grabowski's occurrence halved fingerprint
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._fingerprint import MOST_COMMON_LETTERS_CG, _Fingerprint

__all__ = ['OccurrenceHalved', 'occurrence_halved_fingerprint']


class OccurrenceHalved(_Fingerprint):
    """Occurrence Halved Fingerprint.

    Based on the occurrence halved fingerprint from :cite:`Cislak:2017`.
    """

    def fingerprint(self, word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
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

        """
        if n_bits % 2:
            n_bits += 1

        w_len = len(word) // 2
        w_1 = set(word[:w_len])
        w_2 = set(word[w_len:])
        fingerprint = 0

        for letter in most_common:
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

    """
    return OccurrenceHalved().fingerprint(word, n_bits, most_common)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
