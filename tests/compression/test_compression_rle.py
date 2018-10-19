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

"""abydos.tests.test_compression_rle.

This module contains unit tests for abydos.compression.rle
"""

from __future__ import unicode_literals

import unittest

from abydos.compression.rle import decode, encode


class RLETestCases(unittest.TestCase):
    """Test abydos.compression.rle.encode & .decode."""

    bws = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'

    def test_rle_encode(self):
        """Test abydos.compression.rle.encode."""
        self.assertEqual(encode('', False), '')
        self.assertEqual(encode(''), '\x00')
        self.assertEqual(encode('banana', False), 'banana')
        self.assertEqual(encode('banana'), 'annb\x00aa')
        self.assertEqual(encode(self.bws, False), '12WB12W3B24WB14W')
        self.assertEqual(encode(self.bws), 'WWBWWB45WB\x003WB10WB')
        self.assertEqual(encode('Schifffahrt', False), 'Schi3fahrt')

    def test_rle_decode(self):
        """Test abydos.compression.rle.decode."""
        self.assertEqual(decode('', False), '')
        self.assertEqual(decode('\x00'), '')
        self.assertEqual(decode('banana', False), 'banana')
        self.assertEqual(decode('annb\x00aa'), 'banana')
        self.assertEqual(decode('12WB12W3B24WB14W', False), self.bws)
        self.assertEqual(decode('12W1B12W3B24W1B14W', False), self.bws)
        self.assertEqual(decode('WWBWWB45WB\x003WB10WB'), self.bws)
        self.assertEqual(decode('Schi3fahrt', False), 'Schifffahrt')

    def test_rle_roundtripping(self):
        """Test abydos.compression.rle.encode & .decode roundtripping."""
        self.assertEqual(decode(encode('', False), False), '')
        self.assertEqual(decode(encode('')), '')
        self.assertEqual(decode(encode('banana', False), False), 'banana')
        self.assertEqual(decode(encode('banana')), 'banana')
        self.assertEqual(decode(encode(self.bws, False), False), self.bws)
        self.assertEqual(decode(encode(self.bws)), self.bws)
        self.assertEqual(decode(encode('Schifffahrt', False), False),
                         'Schifffahrt')
        self.assertEqual(decode(encode('Schifffahrt')), 'Schifffahrt')


if __name__ == '__main__':
    unittest.main()
