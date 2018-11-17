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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._arithmetic import Arithmetic, ac_decode, ac_encode, ac_train
from ._bwt import BWT, bwt_decode, bwt_encode
from ._rle import RLE, rle_decode, rle_encode

__all__ = [
    'Arithmetic',
    'ac_decode',
    'ac_encode',
    'ac_train',
    'BWT',
    'bwt_decode',
    'bwt_encode',
    'RLE',
    'rle_decode',
    'rle_encode',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
