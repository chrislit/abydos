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

"""abydos.compression.

The compression package defines compression and compression-related functions
for use within Abydos, including implementations of the following:

    - arithmetic coding functions (ac_train, ac_encode, & ac_decode)
    - Burrows-Wheeler transform encoder/decoder (bwt_encode & bwt_decode)
    - Run-Length Encoding encoder/decoder (rle_encode & rle_decode)
"""

from __future__ import unicode_literals

from ._arithmetic import ac_decode, ac_encode, ac_train
from ._bwt import bwt_decode, bwt_encode
from ._rle import rle_decode, rle_encode

__all__ = [
    'bwt_decode',
    'bwt_encode',
    'rle_decode',
    'rle_encode',
    'ac_decode',
    'ac_encode',
    'ac_train',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
