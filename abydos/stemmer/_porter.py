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

"""abydos.stemmer._porter.

Porter stemmer
"""

from unicodedata import normalize

from deprecation import deprecated

from ._stemmer import _Stemmer
from .. import __version__

__all__ = ['Porter', 'porter']


class Porter(_Stemmer):
    """Porter stemmer.

    The Porter stemmer is described in :cite:`Porter:1980`.

    .. versionadded:: 0.3.6
    """

    _vowels = {'a', 'e', 'i', 'o', 'u', 'y'}

    def _m_degree(self, term):
        """Return Porter helper function _m_degree value.

        m-degree is equal to the number of V to C transitions

        Parameters
        ----------
        term : str
            The word for which to calculate the m-degree

        Returns
        -------
        int
            The m-degree as defined in the Porter stemmer definition


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        mdeg = 0
        last_was_vowel = False
        for letter in term:
            if letter in self._vowels:
                last_was_vowel = True
            else:
                if last_was_vowel:
                    mdeg += 1
                last_was_vowel = False
        return mdeg

    def _has_vowel(self, term):
        """Return Porter helper function _has_vowel value.

        Parameters
        ----------
        term : str
            The word to scan for vowels

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

    def _ends_in_doubled_cons(self, term):
        """Return Porter helper function _ends_in_doubled_cons value.

        Parameters
        ----------
        term : str
            The word to check for a final doubled consonant

        Returns
        -------
        bool
            True iff the stem ends in a doubled consonant (as defined in the
            Porter stemmer definition)


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return (
            len(term) > 1
            and term[-1] not in self._vowels
            and term[-2] == term[-1]
        )

    def _ends_in_cvc(self, term):
        """Return Porter helper function _ends_in_cvc value.

        Parameters
        ----------
        term : str
            The word to scan for cvc

        Returns
        -------
        bool
            True iff the stem ends in cvc (as defined in the Porter stemmer
            definition)


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return len(term) > 2 and (
            term[-1] not in self._vowels
            and term[-2] in self._vowels
            and term[-3] not in self._vowels
            and term[-1] not in tuple('wxY')
        )

    def __init__(self, early_english=False):
        """Initialize Porter instance.

        Parameters
        ----------
        early_english : bool
            Set to True in order to remove -eth & -est (2nd & 3rd person
            singular verbal agreement suffixes)


        .. versionadded:: 0.4.0

        """
        self._early_english = early_english

    def stem(self, word):
        """Return Porter stem.

        Parameters
        ----------
        word : str
            The word to stem

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = Porter()
        >>> stmr.stem('reading')
        'read'
        >>> stmr.stem('suspension')
        'suspens'
        >>> stmr.stem('elusiveness')
        'elus'

        >>> stmr = Porter(early_english=True)
        >>> stmr.stem('eateth')
        'eat'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', word.lower())

        # Return word if stem is shorter than 2
        if len(word) < 3:
            return word

        # Re-map consonantal y to Y (Y will be C, y will be V)
        if word[0] == 'y':
            word = 'Y' + word[1:]
        for i in range(1, len(word)):
            if word[i] == 'y' and word[i - 1] in self._vowels:
                word = word[:i] + 'Y' + word[i + 1 :]

        # Step 1a
        if word[-1] == 's':
            if word[-4:] == 'sses':
                word = word[:-2]
            elif word[-3:] == 'ies':
                word = word[:-2]
            elif word[-2:] == 'ss':
                pass
            else:
                word = word[:-1]

        # Step 1b
        step1b_flag = False
        if word[-3:] == 'eed':
            if self._m_degree(word[:-3]) > 0:
                word = word[:-1]
        elif word[-2:] == 'ed':
            if self._has_vowel(word[:-2]):
                word = word[:-2]
                step1b_flag = True
        elif word[-3:] == 'ing':
            if self._has_vowel(word[:-3]):
                word = word[:-3]
                step1b_flag = True
        elif self._early_english:
            if word[-3:] == 'est':
                if self._has_vowel(word[:-3]):
                    word = word[:-3]
                    step1b_flag = True
            elif word[-3:] == 'eth':
                if self._has_vowel(word[:-3]):
                    word = word[:-3]
                    step1b_flag = True

        if step1b_flag:
            if word[-2:] in {'at', 'bl', 'iz'}:
                word += 'e'
            elif self._ends_in_doubled_cons(word) and word[-1] not in {
                'l',
                's',
                'z',
            }:
                word = word[:-1]
            elif self._m_degree(word) == 1 and self._ends_in_cvc(word):
                word += 'e'

        # Step 1c
        if word[-1] in {'Y', 'y'} and self._has_vowel(word[:-1]):
            word = word[:-1] + 'i'

        # Step 2
        if len(word) > 1:
            if word[-2] == 'a':
                if word[-7:] == 'ational':
                    if self._m_degree(word[:-7]) > 0:
                        word = word[:-5] + 'e'
                elif word[-6:] == 'tional':
                    if self._m_degree(word[:-6]) > 0:
                        word = word[:-2]
            elif word[-2] == 'c':
                if word[-4:] in {'enci', 'anci'}:
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-1] + 'e'
            elif word[-2] == 'e':
                if word[-4:] == 'izer':
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-1]
            elif word[-2] == 'g':
                if word[-4:] == 'logi':
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-1]
            elif word[-2] == 'l':
                if word[-3:] == 'bli':
                    if self._m_degree(word[:-3]) > 0:
                        word = word[:-1] + 'e'
                elif word[-4:] == 'alli':
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-2]
                elif word[-5:] == 'entli':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-2]
                elif word[-3:] == 'eli':
                    if self._m_degree(word[:-3]) > 0:
                        word = word[:-2]
                elif word[-5:] == 'ousli':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-2]
            elif word[-2] == 'o':
                if word[-7:] == 'ization':
                    if self._m_degree(word[:-7]) > 0:
                        word = word[:-5] + 'e'
                elif word[-5:] == 'ation':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-3] + 'e'
                elif word[-4:] == 'ator':
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-2] + 'e'
            elif word[-2] == 's':
                if word[-5:] == 'alism':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-3]
                elif word[-7:] in {'iveness', 'fulness', 'ousness'}:
                    if self._m_degree(word[:-7]) > 0:
                        word = word[:-4]
            elif word[-2] == 't':
                if word[-5:] == 'aliti':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-3]
                elif word[-5:] == 'iviti':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-3] + 'e'
                elif word[-6:] == 'biliti':
                    if self._m_degree(word[:-6]) > 0:
                        word = word[:-5] + 'le'

        # Step 3
        if word[-5:] in 'icate':
            if self._m_degree(word[:-5]) > 0:
                word = word[:-3]
        elif word[-5:] == 'ative':
            if self._m_degree(word[:-5]) > 0:
                word = word[:-5]
        elif word[-5:] in {'alize', 'iciti'}:
            if self._m_degree(word[:-5]) > 0:
                word = word[:-3]
        elif word[-4:] == 'ical':
            if self._m_degree(word[:-4]) > 0:
                word = word[:-2]
        elif word[-3:] == 'ful':
            if self._m_degree(word[:-3]) > 0:
                word = word[:-3]
        elif word[-4:] == 'ness':
            if self._m_degree(word[:-4]) > 0:
                word = word[:-4]

        # Step 4
        if word[-2:] == 'al':
            if self._m_degree(word[:-2]) > 1:
                word = word[:-2]
        elif word[-4:] in {'ance', 'ence'}:
            if self._m_degree(word[:-4]) > 1:
                word = word[:-4]
        elif word[-2:] in {'er', 'ic'}:
            if self._m_degree(word[:-2]) > 1:
                word = word[:-2]
        elif word[-4:] in {'able', 'ible'}:
            if self._m_degree(word[:-4]) > 1:
                word = word[:-4]
        elif word[-3:] == 'ant':
            if self._m_degree(word[:-3]) > 1:
                word = word[:-3]
        elif word[-5:] == 'ement':
            if self._m_degree(word[:-5]) > 1:
                word = word[:-5]
        elif word[-4:] == 'ment':
            if self._m_degree(word[:-4]) > 1:
                word = word[:-4]
        elif word[-3:] == 'ent':
            if self._m_degree(word[:-3]) > 1:
                word = word[:-3]
        elif word[-4:] in {'sion', 'tion'}:
            if self._m_degree(word[:-3]) > 1:
                word = word[:-3]
        elif word[-2:] == 'ou':
            if self._m_degree(word[:-2]) > 1:
                word = word[:-2]
        elif word[-3:] in {'ism', 'ate', 'iti', 'ous', 'ive', 'ize'}:
            if self._m_degree(word[:-3]) > 1:
                word = word[:-3]

        # Step 5a
        if word[-1] == 'e':
            if self._m_degree(word[:-1]) > 1:
                word = word[:-1]
            elif self._m_degree(word[:-1]) == 1 and not self._ends_in_cvc(
                word[:-1]
            ):
                word = word[:-1]

        # Step 5b
        if word[-2:] == 'll' and self._m_degree(word) > 1:
            word = word[:-1]

        # Change 'Y' back to 'y' if it survived stemming
        for i in range(len(word)):
            if word[i] == 'Y':
                word = word[:i] + 'y' + word[i + 1 :]

        return word


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Porter.stem method instead.',
)
def porter(word, early_english=False):
    """Return Porter stem.

    This is a wrapper for :py:meth:`Porter.stem`.

    Parameters
    ----------
    word : str
        The word to stem
    early_english : bool
        Set to True in order to remove -eth & -est (2nd & 3rd person singular
        verbal agreement suffixes)

    Returns
    -------
    str
        Word stem

    Examples
    --------
    >>> porter('reading')
    'read'
    >>> porter('suspension')
    'suspens'
    >>> porter('elusiveness')
    'elus'

    >>> porter('eateth', early_english=True)
    'eat'

    .. versionadded:: 0.1.0

    """
    return Porter(early_english).stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
