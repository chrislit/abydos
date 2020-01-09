# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.stemmer._snowball.

Snowball Stemmer base class
"""

from ._stemmer import _Stemmer

__all__ = ['_Snowball']


class _Snowball(_Stemmer):
    """Snowball stemmer base class.

    .. versionadded:: 0.3.6
    """

    _vowels = set('aeiouy')
    _codanonvowels = set("'bcdfghjklmnpqrstvz")

    def _sb_r1(self, term, r1_prefixes=None):
        """Return the R1 region, as defined in the Porter2 specification.

        Parameters
        ----------
        term : str
            The term to examine
        r1_prefixes : set
            Prefixes to consider

        Returns
        -------
        int
            Length of the R1 region


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        vowel_found = False
        if hasattr(r1_prefixes, '__iter__'):
            for prefix in r1_prefixes:
                if term[: len(prefix)] == prefix:
                    return len(prefix)

        for i in range(len(term)):
            if not vowel_found and term[i] in self._vowels:
                vowel_found = True
            elif vowel_found and term[i] not in self._vowels:
                return i + 1
        return len(term)

    def _sb_r2(self, term, r1_prefixes=None):
        """Return the R2 region, as defined in the Porter2 specification.

        Parameters
        ----------
        term : str
            The term to examine
        r1_prefixes : set
            Prefixes to consider

        Returns
        -------
        int
            Length of the R1 region


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        r1_start = self._sb_r1(term, r1_prefixes)
        return r1_start + self._sb_r1(term[r1_start:])

    def _sb_ends_in_short_syllable(self, term):
        """Return True iff term ends in a short syllable.

        (...according to the Porter2 specification.)

        NB: This is akin to the CVC test from the Porter stemmer. The
        description is unfortunately poor/ambiguous.

        Parameters
        ----------
        term : str
            The term to examine

        Returns
        -------
        bool
            True iff term ends in a short syllable


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if not term:
            return False
        if len(term) == 2:
            if term[-2] in self._vowels and term[-1] not in self._vowels:
                return True
        elif len(term) >= 3:
            if (
                term[-3] not in self._vowels
                and term[-2] in self._vowels
                and term[-1] in self._codanonvowels
            ):
                return True
        return False

    def _sb_short_word(self, term, r1_prefixes=None):
        """Return True iff term is a short word.

        (...according to the Porter2 specification.)

        Parameters
        ----------
        term : str
            The term to examine
        r1_prefixes : set
            Prefixes to consider

        Returns
        -------
        bool
            True iff term is a short word


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if self._sb_r1(term, r1_prefixes) == len(
            term
        ) and self._sb_ends_in_short_syllable(term):
            return True
        return False

    def _sb_has_vowel(self, term):
        """Return Porter helper function _sb_has_vowel value.

        Parameters
        ----------
        term : str
            The term to examine

        Returns
        -------
        bool
            True iff a vowel exists in the term (as defined in the Porter
            stemmer definition)


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        for letter in term:
            if letter in self._vowels:
                return True
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod()
