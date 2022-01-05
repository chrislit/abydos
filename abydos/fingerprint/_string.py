# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.fingerprint._string_fingerprint.

string fingerprint
"""

from unicodedata import normalize as unicode_normalize

from ._fingerprint import _Fingerprint

__all__ = ['String']


class String(_Fingerprint):
    """String Fingerprint.

    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening joiners.
    This fingerprint is described at :cite:`OpenRefine:2012`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, joiner: str = ' ') -> None:
        """Initialize String instance.

        Parameters
        ----------
        joiner : str
            The string that will be placed between each word


        .. versionadded:: 0.4.0

        """
        super().__init__()
        self._joiner = joiner

    def fingerprint(self, phrase: str) -> str:
        """Return string fingerprint.

        Parameters
        ----------
        phrase : str
            The string from which to calculate the fingerprint

        Returns
        -------
        str
            The fingerprint of the phrase

        Example
        -------
        >>> sf = String()
        >>> sf.fingerprint('The quick brown fox jumped over the lazy dog.')
        'brown dog fox jumped lazy over quick the'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        phrase = unicode_normalize('NFKD', phrase.strip().lower())
        phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
        phrase = self._joiner.join(sorted(set(phrase.split())))
        return phrase


if __name__ == '__main__':
    import doctest

    doctest.testmod()
