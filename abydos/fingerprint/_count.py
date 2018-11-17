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

"""abydos.fingerprint._count.

Cisłak & Grabowski's count fingerprint
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter

from ._fingerprint import MOST_COMMON_LETTERS_CG, _Fingerprint

__all__ = ['Count', 'count_fingerprint']


class Count(_Fingerprint):
    """Count Fingerprint.

    Based on the count fingerprint from :cite:`Cislak:2017`.
    """

    def fingerprint(self, word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
        """Return the count fingerprint.

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
            The count fingerprint

        Examples
        --------
        >>> cf = Count()
        >>> bin(cf.fingerprint('hat'))
        '0b1010000000001'
        >>> bin(cf.fingerprint('niall'))
        '0b10001010000'
        >>> bin(cf.fingerprint('colin'))
        '0b101010000'
        >>> bin(cf.fingerprint('atcg'))
        '0b1010000000000'
        >>> bin(cf.fingerprint('entreatment'))
        '0b1111010000100000'

        """
        if n_bits % 2:
            n_bits += 1

        word = Counter(word)
        fingerprint = 0

        for letter in most_common:
            if n_bits:
                fingerprint <<= 2
                fingerprint += word[letter] & 3
                n_bits -= 2
            else:
                break

        if n_bits:
            fingerprint <<= n_bits

        return fingerprint


def count_fingerprint(word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
    """Return the count fingerprint.

    This is a wrapper for :py:meth:`Count.fingerprint`.

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
        The count fingerprint

    Examples
    --------
    >>> bin(count_fingerprint('hat'))
    '0b1010000000001'
    >>> bin(count_fingerprint('niall'))
    '0b10001010000'
    >>> bin(count_fingerprint('colin'))
    '0b101010000'
    >>> bin(count_fingerprint('atcg'))
    '0b1010000000000'
    >>> bin(count_fingerprint('entreatment'))
    '0b1111010000100000'

    """
    return Count().fingerprint(word, n_bits, most_common)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
