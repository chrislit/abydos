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

"""abydos.fingerprint._string_fingerprint.

string fingerprint
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._fingerprint import _Fingerprint
from .. import __version__

__all__ = ['String', 'str_fingerprint']


class String(_Fingerprint):
    """String Fingerprint.

    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening joiners.
    This fingerprint is described at :cite:`OpenRefine:2012`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, joiner=' '):
        """Initialize String instance.

        Parameters
        ----------
        joiner : str
            The string that will be placed between each word


        .. versionadded:: 0.4.0

        """
        self._joiner = joiner

    def fingerprint(self, phrase):
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


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the String.fingerprint method instead.',
)
def str_fingerprint(phrase, joiner=' '):
    """Return string fingerprint.

    This is a wrapper for :py:meth:`String.fingerprint`.

    Parameters
    ----------
    phrase : str
        The string from which to calculate the fingerprint
    joiner : str
        The string that will be placed between each word

    Returns
    -------
    str
        The fingerprint of the phrase

    Example
    -------
    >>> str_fingerprint('The quick brown fox jumped over the lazy dog.')
    'brown dog fox jumped lazy over quick the'

    .. versionadded:: 0.1.0

    """
    return String(joiner).fingerprint(phrase)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
