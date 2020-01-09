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

"""abydos.fingerprint._extract.

Taft's extract letter list coding
"""

from ._fingerprint import _Fingerprint

__all__ = ['Extract']


class Extract(_Fingerprint):
    """Extract Letter List fingerprint.

    Based on the extract letter list coding from :cite:`Taft:1970`,
    for lists 1, 2, 3, & 4.

    .. versionadded:: 0.4.1
    """

    def __init__(self, letter_list=1):
        """Initialize Extract instance.

        Parameters
        ----------
        letter_list : int or iterable
            If an integer (1-4) is supplied, Taft's specified letter lists are
            used. If an iterable is supplied, its values will be used as the
            list of letters to remove (in order).


        .. versionadded:: 0.4.1

        """
        letter_lists = [
            'ETAONRISHDLFCMUGYPWBVKXJQZ',
            'ETASIONRHCDLPMFBUWGYKVJQZX',
            'ETAONISRHLDCUMFYWGPKBVXJQZ',
            'EARNLOISTHDMCBGUWYJKPFVZXQ',
        ]

        super(_Fingerprint, self).__init__()
        self._letter_list = letter_list
        if isinstance(self._letter_list, int) and 1 <= self._letter_list <= 4:
            self._letter_list = list(letter_lists[self._letter_list - 1])
        elif hasattr(self._letter_list, '__iter__'):
            self._letter_list = list(self._letter_list)
        else:
            self._letter_list = list(letter_lists[0])

    def fingerprint(self, word):
        """Return the extract letter list coding.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        int
            The extract letter list coding

        Examples
        --------
        >>> fp = Extract()
        >>> fp.fingerprint('hat')
        'HAT'
        >>> fp.fingerprint('niall')
        'NILL'
        >>> fp.fingerprint('colin')
        'CLIN'
        >>> fp.fingerprint('atcg')
        'ATCG'
        >>> fp.fingerprint('entreatment')
        'NRMN'


        .. versionadded:: 0.4.1

        """
        # uppercase & reverse
        word = word.upper()[::-1]

        for letter in self._letter_list:  # pragma: no branch
            if len(word) < 5:
                break

            count = word.count(letter)
            if count:
                word = word.replace(
                    letter, '', count - (4 - (len(word) - count))
                )

        return word[::-1]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
