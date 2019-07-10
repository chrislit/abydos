# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.fingerprint._bwtrle.

Burrows-Wheeler transform plus run-length encoding fingerprint
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ..compression import BWT as _BWT
from ..compression import RLE as _RLE
from ._fingerprint import _Fingerprint

__all__ = ['BWTRLE_F']


class BWTRLE_F(_Fingerprint):
    """Burrows-Wheeler transform plus run-length encoding fingerprint.

    This is a wrapper of the BWT and RLE classes in Abydos.compression, which
    provides the same interface as other descendants of _Fingerprint.

    .. versionadded:: 0.4.1
    """

    def __init__(self, terminator='\0'):
        """Initialize BWTRLE_F instance.

        Parameters
        ----------
        terminator : str
            A character added to signal the end of the string


        .. versionadded:: 0.4.1

        """
        self._bwt = _BWT(terminator)
        self._rle = _RLE()

    def fingerprint(self, word):
        """Return the run-length encoded Burrows-Wheeler transform of a word.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        str
            The run-length encoded Burrows-Wheeler transform of a word

        Examples
        --------
        >>> fp = BWTRLE_F()
        >>> fp.fingerprint('hat')
        'H38'
        >>> fp.fingerprint('niall')
        'N5355'
        >>> fp.fingerprint('colin')
        'C6556'
        >>> fp.fingerprint('atcg')
        'A834'
        >>> fp.fingerprint('entreatment')
        'E5874386468'


        .. versionadded:: 0.4.1

        """
        return self._rle.encode(self._bwt.encode(word))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
