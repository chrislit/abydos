# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._fingerprint import _Fingerprint

__all__ = ['String', 'str_fingerprint']


class String(_Fingerprint):
    """String Fingerprint.

    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening joiners.
    This fingerprint is described at :cite:`OpenRefine:2012`.
    """

    def fingerprint(self, phrase, joiner=' '):
        """Return string fingerprint.

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
        >>> sf = String()
        >>> sf.fingerprint('The quick brown fox jumped over the lazy dog.')
        'brown dog fox jumped lazy over quick the'

        """
        phrase = unicode_normalize('NFKD', text_type(phrase.strip().lower()))
        phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
        phrase = joiner.join(sorted(list(set(phrase.split()))))
        return phrase


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

    """
    return String().fingerprint(phrase, joiner)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
