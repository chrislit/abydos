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

r"""abydos.compression.

The compression package defines compression and compression-related functions
for use within Abydos, including implementations of the following:

        - :py:class:`.Arithmetic` for arithmetic coding
        - :py:class:`.BWT` for Burrows-Wheeler Transform
        - :py:class:`.RLE` for Run-Length Encoding


Each class exposes ``encode`` and ``decode`` methods for performing and
reversing its encoding. For example, the Burrows-Wheeler Transform can be
performed by creating a :py:class:`.BWT` object and then calling
:py:meth:`.BWT.encode` on a string:

>>> bwt = BWT()
>>> bwt.encode('^BANANA')
'ANNB^AA\x00'

----

"""

from ._arithmetic import Arithmetic
from ._bwt import BWT
from ._rle import RLE

__all__ = [
    'Arithmetic',
    'BWT',
    'RLE',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
