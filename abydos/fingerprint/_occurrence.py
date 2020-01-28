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

from typing import Tuple

from ._fingerprint import MOST_COMMON_LETTERS_CG, _Fingerprint

__all__ = ['Occurrence']


class Occurrence(_Fingerprint):
    """Occurrence Fingerprint.

    Based on the occurrence fingerprint from :cite:`Cislak:2017`.

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
        super(Occurrence, self).__init__()
        self._n_bits = n_bits
        self._most_common = most_common

    def fingerprint(self, word: str) -> str:
        """Return the occurrence fingerprint.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        str
            The occurrence fingerprint

        Examples
        --------
        >>> of = Occurrence()
        >>> of.fingerprint('hat')
        '0110000100000000'
        >>> of.fingerprint('niall')
        '0010110000100000'
        >>> of.fingerprint('colin')
        '0001110000110000'
        >>> of.fingerprint('atcg')
        '0110000000010000'
        >>> of.fingerprint('entreatment')
        '1110010010000100'


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
        """Return the occurrence fingerprint.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        int
            The occurrence fingerprint as an int

        Examples
        --------
        >>> of = Occurrence()
        >>> of.fingerprint_int('hat')
        24832
        >>> of.fingerprint_int('niall')
        11296
        >>> of.fingerprint_int('colin')
        7216
        >>> of.fingerprint_int('atcg')
        24592
        >>> of.fingerprint_int('entreatment')
        58500


        .. versionadded:: 0.6.0

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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
