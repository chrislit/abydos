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

"""abydos.phonetic._statistics_canada.

Statistics Canada phonetic encoding
"""

from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['StatisticsCanada']


class StatisticsCanada(_Phonetic):
    """Statistics Canada code.

    The original description of this algorithm could not be located, and
    may only have been specified in an unpublished TR. The coding does not
    appear to be in use by Statistics Canada any longer. In its place, this is
    an implementation of the "Census modified Statistics Canada name coding
    procedure".

    The modified version of this algorithm is described in Appendix B of
    :cite:`Moore:1977`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, max_length=4) -> None:
        """Initialize StatisticsCanada instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 4)


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length

    def encode(self, word):
        """Return the Statistics Canada code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Statistics Canada name code value

        Examples
        --------
        >>> pe = StatisticsCanada()
        >>> pe.encode('Christopher')
        'CHRS'
        >>> pe.encode('Niall')
        'NL'
        >>> pe.encode('Smith')
        'SMTH'
        >>> pe.encode('Schmidt')
        'SCHM'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)
        if not word:
            return ''

        code = word[1:]
        for vowel in self._uc_vy_set:
            code = code.replace(vowel, '')
        code = word[0] + code
        code = self._delete_consecutive_repeats(code)
        code = code.replace(' ', '')

        return code[: self._max_length]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
