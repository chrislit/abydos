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

"""abydos.phonetic._lein.

Lein
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._phonetic import _Phonetic

__all__ = ['Lein', 'lein']


class Lein(_Phonetic):
    """Lein code.

    This is Lein name coding, described in :cite:`Moore:1977`.
    """

    _trans = dict(
        zip((ord(_) for _ in 'BCDFGJKLMNPQRSTVXZ'), '451455532245351455')
    )

    _del_trans = {num: None for num in (32, 65, 69, 72, 73, 79, 85, 87, 89)}

    def encode(self, word, max_length=4, zero_pad=True):
        """Return the Lein code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The Lein code

        Examples
        --------
        >>> pe = Lein()
        >>> pe.encode('Christopher')
        'C351'
        >>> pe.encode('Niall')
        'N300'
        >>> pe.encode('Smith')
        'S210'
        >>> pe.encode('Schmidt')
        'S521'

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        code = word[:1]  # Rule 1
        word = word[1:].translate(self._del_trans)  # Rule 2
        word = self._delete_consecutive_repeats(word)  # Rule 3
        code += word.translate(self._trans)  # Rule 4

        if zero_pad:
            code += '0' * max_length  # Rule 4

        return code[:max_length]


def lein(word, max_length=4, zero_pad=True):
    """Return the Lein code for a word.

    This is a wrapper for :py:meth:`Lein.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The Lein code

    Examples
    --------
    >>> lein('Christopher')
    'C351'
    >>> lein('Niall')
    'N300'
    >>> lein('Smith')
    'S210'
    >>> lein('Schmidt')
    'S521'

    """
    return Lein().encode(word, max_length, zero_pad)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
