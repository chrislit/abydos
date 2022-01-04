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

"""abydos.fingerprint._count.

Cisłak & Grabowski's count fingerprint
"""

from collections import Counter
from typing import Tuple

from ._fingerprint import MOST_COMMON_LETTERS_CG, _Fingerprint

__all__ = ['Count']


class Count(_Fingerprint):
    """Count Fingerprint.

    Based on the count fingerprint from :cite:`Cislak:2017`.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self,
        n_bits: int = 16,
        most_common: Tuple[str, ...] = MOST_COMMON_LETTERS_CG,
    ) -> None:
        """Initialize Count instance.

        Parameters
        ----------
        n_bits : int
            Number of bits in the fingerprint returned
        most_common : list
            The most common tokens in the target language, ordered by frequency


        .. versionadded:: 0.4.0

        """
        super().__init__()
        self._n_bits = n_bits
        self._most_common = most_common

    def fingerprint(self, word: str) -> str:
        """Return the count fingerprint.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        str
            The count fingerprint

        Examples
        --------
        >>> cf = Count()
        >>> cf.fingerprint('hat')
        '0001010000000001'
        >>> cf.fingerprint('niall')
        '0000010001010000'
        >>> cf.fingerprint('colin')
        '0000000101010000'
        >>> cf.fingerprint('atcg')
        '0001010000000000'
        >>> cf.fingerprint('entreatment')
        '1111010000100000'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class
        .. versionchanged:: 0.6.0
            Changed to return a str and added fingerprint_int method

        """
        return ('{:0' + str(self._n_bits) + 'b}').format(
            self.fingerprint_int(word)
        )

    def fingerprint_int(self, word: str) -> int:
        """Return the count fingerprint.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        int
            The count fingerprint as an int

        Examples
        --------
        >>> cf = Count()
        >>> cf.fingerprint_int('hat')
        5121
        >>> cf.fingerprint_int('niall')
        1104
        >>> cf.fingerprint_int('colin')
        336
        >>> cf.fingerprint_int('atcg')
        5120
        >>> cf.fingerprint_int('entreatment')
        62496


        .. versionadded:: 0.6.0

        """
        n_bits = self._n_bits
        if n_bits % 2:
            n_bits += 1

        letter_counts = Counter(word)
        fingerprint = 0

        for letter in self._most_common:
            if n_bits:
                fingerprint <<= 2
                fingerprint += letter_counts[letter] & 3
                n_bits -= 2
            else:
                break

        if n_bits:
            fingerprint <<= n_bits

        return fingerprint


if __name__ == '__main__':
    import doctest

    doctest.testmod()
