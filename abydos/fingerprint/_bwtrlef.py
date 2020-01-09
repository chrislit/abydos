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

"""abydos.fingerprint._bwtrlef.

Burrows-Wheeler transform plus run-length encoding fingerprint
"""

from ._fingerprint import _Fingerprint
from ..compression import BWT as _BWT
from ..compression import RLE as _RLE

__all__ = ['BWTRLEF']


class BWTRLEF(_Fingerprint):
    """Burrows-Wheeler transform plus run-length encoding fingerprint.

    This is a wrapper of the BWT and RLE classes in abydos.compression, which
    provides the same interface as other descendants of _Fingerprint.

    .. versionadded:: 0.4.1
    """

    def __init__(self, terminator='\0'):
        """Initialize BWTRLEF instance.

        Parameters
        ----------
        terminator : str
            A character added to signal the end of the string


        .. versionadded:: 0.4.1

        """
        self._bwt = _BWT(terminator)
        self._rle = _RLE()

    def fingerprint(self, word):
        r"""Return the run-length encoded Burrows-Wheeler transform of a word.

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
        >>> fp = BWTRLEF()
        >>> fp.fingerprint('hat')
        'th\x00a'
        >>> fp.fingerprint('niall')
        'linla\x00'
        >>> fp.fingerprint('colin')
        'n\x00loic'
        >>> fp.fingerprint('atcg')
        'g\x00tca'
        >>> fp.fingerprint('entreatment')
        'term\x00teetnan'


        .. versionadded:: 0.4.1

        """
        return self._rle.encode(self._bwt.encode(word))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
