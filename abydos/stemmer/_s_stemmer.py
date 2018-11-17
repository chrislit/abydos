# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.stemmer._s_stemmer.

S-stemmer.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._stemmer import _Stemmer

__all__ = ['SStemmer', 's_stemmer']


class SStemmer(_Stemmer):
    """S-stemmer.

    The S stemmer is defined in :cite:`Harman:1991`.
    """

    def stem(self, word):
        """Return the S-stemmed form of a word.

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
        >>> stmr = SStemmer()
        >>> stmr.stem('summaries')
        'summary'
        >>> stmr.stem('summary')
        'summary'
        >>> stmr.stem('towers')
        'tower'
        >>> stmr.stem('reading')
        'reading'
        >>> stmr.stem('census')
        'census'

        """
        lowered = word.lower()
        if lowered[-3:] == 'ies' and lowered[-4:-3] not in {'e', 'a'}:
            return word[:-3] + ('Y' if word[-1:].isupper() else 'y')
        if lowered[-2:] == 'es' and lowered[-3:-2] not in {'a', 'e', 'o'}:
            return word[:-1]
        if lowered[-1:] == 's' and lowered[-2:-1] not in {'u', 's'}:
            return word[:-1]
        return word


def s_stemmer(word):
    """Return the S-stemmed form of a word.

    This is a wrapper for :py:meth:`SStemmer.stem`.

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
    >>> s_stemmer('summaries')
    'summary'
    >>> s_stemmer('summary')
    'summary'
    >>> s_stemmer('towers')
    'tower'
    >>> s_stemmer('reading')
    'reading'
    >>> s_stemmer('census')
    'census'

    """
    return SStemmer().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
