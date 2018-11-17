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

"""abydos.fingerprint._position.

Cisłak & Grabowski's position fingerprint
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._fingerprint import MOST_COMMON_LETTERS_CG, _Fingerprint

__all__ = ['Position', 'position_fingerprint']


class Position(_Fingerprint):
    """Position Fingerprint.

    Based on the position fingerprint from :cite:`Cislak:2017`.
    """

    def fingerprint(
        self,
        word,
        n_bits=16,
        most_common=MOST_COMMON_LETTERS_CG,
        bits_per_letter=3,
    ):
        """Return the position fingerprint.

        Parameters
        ----------
        word : str
            The word to fingerprint
        n_bits : int
            Number of bits in the fingerprint returned
        most_common : list
            The most common tokens in the target language, ordered by frequency
        bits_per_letter : int
            The bits to assign for letter position

        Returns
        -------
        int
            The position fingerprint

        Examples
        --------
        >>> bin(position_fingerprint('hat'))
        '0b1110100011111111'
        >>> bin(position_fingerprint('niall'))
        '0b1111110101110010'
        >>> bin(position_fingerprint('colin'))
        '0b1111111110010111'
        >>> bin(position_fingerprint('atcg'))
        '0b1110010001111111'
        >>> bin(position_fingerprint('entreatment'))
        '0b101011111111'

        """
        position = {}
        for pos, letter in enumerate(word):
            if letter not in position and letter in most_common:
                position[letter] = min(pos, 2 ** bits_per_letter - 1)

        fingerprint = 0

        for letter in most_common:
            if n_bits:
                fingerprint <<= min(bits_per_letter, n_bits)
                if letter in position:
                    fingerprint += min(position[letter], 2 ** n_bits - 1)
                else:
                    fingerprint += min(
                        2 ** bits_per_letter - 1, 2 ** n_bits - 1
                    )
                n_bits -= min(bits_per_letter, n_bits)
            else:
                break

        for _ in range(n_bits):
            fingerprint <<= 1
            fingerprint += 1

        return fingerprint


def position_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG, bits_per_letter=3
):
    """Return the position fingerprint.

    This is a wrapper for :py:meth:`Position.fingerprint`.

    Parameters
    ----------
    word : str
        The word to fingerprint
    n_bits : int
        Number of bits in the fingerprint returned
    most_common : list
        The most common tokens in the target language, ordered by frequency
    bits_per_letter : int
        The bits to assign for letter position

    Returns
    -------
    int
        The position fingerprint

    Examples
    --------
    >>> bin(position_fingerprint('hat'))
    '0b1110100011111111'
    >>> bin(position_fingerprint('niall'))
    '0b1111110101110010'
    >>> bin(position_fingerprint('colin'))
    '0b1111111110010111'
    >>> bin(position_fingerprint('atcg'))
    '0b1110010001111111'
    >>> bin(position_fingerprint('entreatment'))
    '0b101011111111'

    """
    return Position().fingerprint(word, n_bits, most_common, bits_per_letter)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
