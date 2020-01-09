# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.fingerprint._consonant.

Taft's consonant coding
"""

from itertools import groupby

from ._fingerprint import _Fingerprint

__all__ = ['Consonant']


class Consonant(_Fingerprint):
    """Consonant Coding Fingerprint.

    Based on the consonant coding from :cite:`Taft:1970`, variants 1, 2, 3,
    1-D, 2-D, and 3-D.

    .. versionadded:: 0.4.1
    """

    def __init__(self, variant=1, doubles=True, vowels=None):
        """Initialize Consonant instance.

        Parameters
        ----------
        variant : int
            Selects between Taft's 3 variants, which assign to the vowel set
            one of:

                1. A, E, I, O, & U
                2. A, E, I, O, U, W, & Y
                3. A, E, I, O, U, W, H, & Y

        doubles : bool
            If set to False, multiple consonants in a row are conflated to a
            single instance.
        vowels : list, set, or str
            Setting vowels to a non-None value overrides the variant setting
            and defines the set of letters to be removed from the input.


        .. versionadded:: 0.4.1

        """
        super(_Fingerprint, self).__init__()
        self._vowels = vowels
        self._doubles = doubles

        if self._vowels is None:
            self._vowels = set('AEIOU')
            if variant > 1:
                self._vowels.add('W')
                self._vowels.add('Y')
            if variant > 2:
                self._vowels.add('H')
        else:
            self._vowels = {_.upper() for _ in self._vowels}

    def fingerprint(self, word):
        """Return the consonant coding.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        int
            The consonant coding

        Examples
        --------
        >>> cf = Consonant()
        >>> cf.fingerprint('hat')
        'HT'
        >>> cf.fingerprint('niall')
        'NLL'
        >>> cf.fingerprint('colin')
        'CLN'
        >>> cf.fingerprint('atcg')
        'ATCG'
        >>> cf.fingerprint('entreatment')
        'ENTRTMNT'


        .. versionadded:: 0.4.1

        """
        # uppercase
        word = word.upper()

        # remove repeats if in -D variant
        if not self._doubles:
            word = ''.join(char for char, _ in groupby(word))

        # remove vowels
        word = word[:1] + ''.join(_ for _ in word[1:] if _ not in self._vowels)

        return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
