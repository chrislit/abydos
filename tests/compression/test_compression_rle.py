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

"""abydos.tests.compression.test_compression_rle.

This module contains unit tests for abydos.compression._rle
"""

from __future__ import unicode_literals

import unittest

from abydos.compression import rle_decode, rle_encode


class RLETestCases(unittest.TestCase):
    """Test abydos.compression._rle.rle_encode & .rle_decode."""

    bws = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'

    def test_rle_encode(self):
        """Test abydos.compression._rle.encode."""
        self.assertEqual(rle_encode('', False), '')
        self.assertEqual(rle_encode(''), '\x00')
        self.assertEqual(rle_encode('banana', False), 'banana')
        self.assertEqual(rle_encode('banana'), 'annb\x00aa')
        self.assertEqual(rle_encode(self.bws, False), '12WB12W3B24WB14W')
        self.assertEqual(rle_encode(self.bws), 'WWBWWB45WB\x003WB10WB')
        self.assertEqual(rle_encode('Schifffahrt', False), 'Schi3fahrt')

    def test_rle_decode(self):
        """Test abydos.compression._rle.decode."""
        self.assertEqual(rle_decode('', False), '')
        self.assertEqual(rle_decode('\x00'), '')
        self.assertEqual(rle_decode('banana', False), 'banana')
        self.assertEqual(rle_decode('annb\x00aa'), 'banana')
        self.assertEqual(rle_decode('12WB12W3B24WB14W', False), self.bws)
        self.assertEqual(rle_decode('12W1B12W3B24W1B14W', False), self.bws)
        self.assertEqual(rle_decode('WWBWWB45WB\x003WB10WB'), self.bws)
        self.assertEqual(rle_decode('Schi3fahrt', False), 'Schifffahrt')

    def test_rle_roundtripping(self):
        """Test abydos.compression._rle.encode & .decode roundtripping."""
        self.assertEqual(rle_decode(rle_encode('', False), False), '')
        self.assertEqual(rle_decode(rle_encode('')), '')
        self.assertEqual(
            rle_decode(rle_encode('banana', False), False), 'banana'
        )
        self.assertEqual(rle_decode(rle_encode('banana')), 'banana')
        self.assertEqual(
            rle_decode(rle_encode(self.bws, False), False), self.bws
        )
        self.assertEqual(rle_decode(rle_encode(self.bws)), self.bws)
        self.assertEqual(
            rle_decode(rle_encode('Schifffahrt', False), False), 'Schifffahrt'
        )
        self.assertEqual(rle_decode(rle_encode('Schifffahrt')), 'Schifffahrt')


if __name__ == '__main__':
    unittest.main()
