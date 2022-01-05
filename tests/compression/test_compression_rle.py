# Copyright 2014-2022 by Christopher C. Little.
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

This module contains unit tests for abydos.compression.RLE
"""

import unittest

from abydos.compression import BWT, RLE


class RLETestCases(unittest.TestCase):
    """Test abydos.compression.RLE.encode & .decode."""

    rle = RLE()
    bwt = BWT()

    bws = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'

    def test_rle_encode(self):
        """Test abydos.compression.RLE.encode."""
        self.assertEqual(self.rle.encode(''), '')
        self.assertEqual(self.rle.encode(self.bwt.encode('')), '\x00')
        self.assertEqual(self.rle.encode('banana'), 'banana')
        self.assertEqual(
            self.rle.encode(self.bwt.encode('banana')), 'annb\x00aa'
        )
        self.assertEqual(self.rle.encode(self.bws), '12WB12W3B24WB14W')
        self.assertEqual(
            self.rle.encode(self.bwt.encode(self.bws)), 'WWBWWB45WB\x003WB10WB'
        )
        self.assertEqual(self.rle.encode('Schifffahrt'), 'Schi3fahrt')

    def test_rle_decode(self):
        """Test abydos.compression.RLE.decode."""
        self.assertEqual(self.rle.decode(''), '')
        self.assertEqual(self.bwt.decode(self.rle.decode('\x00')), '')
        self.assertEqual(self.rle.decode('banana'), 'banana')
        self.assertEqual(
            self.bwt.decode(self.rle.decode('annb\x00aa')), 'banana'
        )
        self.assertEqual(self.rle.decode('12WB12W3B24WB14W'), self.bws)
        self.assertEqual(self.rle.decode('12W1B12W3B24W1B14W'), self.bws)
        self.assertEqual(
            self.bwt.decode(self.rle.decode('WWBWWB45WB\x003WB10WB')), self.bws
        )
        self.assertEqual(self.rle.decode('Schi3fahrt'), 'Schifffahrt')

    def test_rle_roundtripping(self):
        """Test abydos.compression.RLE.encode & .decode roundtripping."""
        self.assertEqual(self.rle.decode(self.rle.encode('')), '')
        self.assertEqual(
            self.bwt.decode(
                self.rle.decode(self.rle.encode(self.bwt.encode('')))
            ),
            '',
        )
        self.assertEqual(self.rle.decode(self.rle.encode('banana')), 'banana')
        self.assertEqual(
            self.bwt.decode(
                self.rle.decode(self.rle.encode(self.bwt.encode('banana')))
            ),
            'banana',
        )
        self.assertEqual(self.rle.decode(self.rle.encode(self.bws)), self.bws)
        self.assertEqual(
            self.bwt.decode(
                self.rle.decode(self.rle.encode(self.bwt.encode(self.bws)))
            ),
            self.bws,
        )
        self.assertEqual(
            self.rle.decode(self.rle.encode('Schifffahrt')), 'Schifffahrt'
        )
        self.assertEqual(
            self.bwt.decode(
                self.rle.decode(
                    self.rle.encode(self.bwt.encode('Schifffahrt'))
                )
            ),
            'Schifffahrt',
        )


if __name__ == '__main__':
    unittest.main()
