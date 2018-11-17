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

"""abydos.phonetic._onca.

Oxford Name Compression Algorithm (ONCA)
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._nysiis import NYSIIS
from ._phonetic import _Phonetic
from ._soundex import Soundex

__all__ = ['ONCA', 'onca']


class ONCA(_Phonetic):
    """Oxford Name Compression Algorithm (ONCA).

    This is the Oxford Name Compression Algorithm, based on :cite:`Gill:1997`.

    I can find no complete description of the "anglicised version of the NYSIIS
    method" identified as the first step in this algorithm, so this is likely
    not a precisely correct implementation, in that it employs the standard
    NYSIIS algorithm.
    """

    _nysiis = NYSIIS()
    _soundex = Soundex()

    def encode(self, word, max_length=4, zero_pad=True):
        """Return the Oxford Name Compression Algorithm (ONCA) code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The maximum length (default 5) of the code to return
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The ONCA code

        Examples
        --------
        >>> pe = ONCA()
        >>> pe.encode('Christopher')
        'C623'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Schmidt')
        'S530'

        """
        # In the most extreme case, 3 characters of NYSIIS input can be
        # compressed to one character of output, so give it triple the
        # max_length.
        return self._soundex.encode(
            self._nysiis.encode(word, max_length=max_length * 3),
            max_length,
            zero_pad=zero_pad,
        )


def onca(word, max_length=4, zero_pad=True):
    """Return the Oxford Name Compression Algorithm (ONCA) code for a word.

    This is a wrapper for :py:meth:`ONCA.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The maximum length (default 5) of the code to return
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The ONCA code

    Examples
    --------
    >>> onca('Christopher')
    'C623'
    >>> onca('Niall')
    'N400'
    >>> onca('Smith')
    'S530'
    >>> onca('Schmidt')
    'S530'

    """
    return ONCA().encode(word, max_length, zero_pad)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
