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

"""abydos.tests.test_distance.compression.

This module contains unit tests for abydos.distance.compression
"""

from __future__ import division, unicode_literals

import pkgutil
import sys
import unittest

from abydos.compression import arithmetic
from abydos.distance.compression import dist_compression, sim_compression

from .. import NIALL


class CompressionTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.dist_compression & .sim_compression
    """

    arith_dict = arithmetic.train(' '.join(NIALL))

    def test_dist_compression(self):
        """Test abydos.distance.dist_compression."""
        self.assertEqual(dist_compression('', ''), 0)
        self.assertEqual(dist_compression('', '', 'bzip2'), 0)
        self.assertEqual(dist_compression('', '', 'zlib'), 0)
        self.assertEqual(dist_compression('', '', 'arith'), 0)
        self.assertEqual(dist_compression('', '', 'arith', self.arith_dict), 0)
        self.assertEqual(dist_compression('', '', 'rle'), 0)
        self.assertEqual(dist_compression('', '', 'bwtrle'), 0)

        self.assertGreater(dist_compression('a', ''), 0)
        self.assertGreater(dist_compression('a', '', 'bzip2'), 0)
        self.assertGreater(dist_compression('a', '', 'zlib'), 0)
        self.assertGreater(dist_compression('a', '', 'arith'), 0)
        self.assertGreater(dist_compression('a', '', 'arith', self.arith_dict),
                           0)
        self.assertGreater(dist_compression('a', '', 'rle'), 0)
        self.assertGreater(dist_compression('a', '', 'bwtrle'), 0)

        self.assertGreater(dist_compression('abcdefg', 'fg'), 0)
        self.assertGreater(dist_compression('abcdefg', 'fg', 'bzip2'), 0)
        self.assertGreater(dist_compression('abcdefg', 'fg', 'zlib'), 0)
        self.assertGreater(dist_compression('abcdefg', 'fg', 'arith'), 0)
        self.assertGreater(dist_compression('abcdefg', 'fg', 'rle'), 0)
        self.assertGreater(dist_compression('abcdefg', 'fg', 'bwtrle'), 0)

    def test_dist_compression_arith(self):
        """Test abydos.distance.dist_compression (arithmetric compression)."""
        self.assertAlmostEqual(dist_compression('Niall', 'Neil', 'arith',
                                                self.arith_dict),
                               0.608695652173913)
        self.assertAlmostEqual(dist_compression('Neil', 'Niall', 'arith',
                                                self.arith_dict),
                               0.608695652173913)
        self.assertAlmostEqual(dist_compression('Niall', 'Neil', 'arith'),
                               0.6875)
        self.assertAlmostEqual(dist_compression('Neil', 'Niall', 'arith'),
                               0.6875)
        self.assertAlmostEqual(dist_compression('Njáll', 'Njall', 'arith',
                                                self.arith_dict),
                               0.714285714285714)
        self.assertAlmostEqual(dist_compression('Njall', 'Njáll', 'arith',
                                                self.arith_dict),
                               0.714285714285714)
        self.assertAlmostEqual(dist_compression('Njáll', 'Njall', 'arith'),
                               0.75)
        self.assertAlmostEqual(dist_compression('Njall', 'Njáll', 'arith'),
                               0.75)

    def test_dist_compression_rle(self):
        """Test abydos.distance.dist_compression (RLE & BWT+RLE)."""
        self.assertAlmostEqual(dist_compression('abc', 'abc', 'rle'), 0)
        self.assertAlmostEqual(dist_compression('abc', 'def', 'rle'), 1)

        self.assertAlmostEqual(dist_compression('abc', 'abc', 'bwtrle'), 0)
        self.assertAlmostEqual(dist_compression('abc', 'def', 'bwtrle'), 0.75)

        self.assertAlmostEqual(dist_compression('aaa', 'bbaaa', 'rle'), 0.5)
        self.assertAlmostEqual(dist_compression('abb', 'bbba', 'rle'), 1/3)
        self.assertAlmostEqual(dist_compression('banana', 'banane', 'bwtrle'),
                               0.57142857142)
        self.assertAlmostEqual(dist_compression('bananas', 'bananen',
                                                'bwtrle'),
                               0.5)

    def test_sim_compression(self):
        """Test abydos.distance.sim_compression."""
        self.assertEqual(sim_compression('', ''), 1)
        self.assertEqual(sim_compression('', '', 'bzip2'), 1)
        self.assertEqual(sim_compression('', '', 'zlib'), 1)
        self.assertEqual(sim_compression('', '', 'arith'), 1)
        self.assertEqual(sim_compression('', '', 'arith', self.arith_dict), 1)
        self.assertEqual(sim_compression('', '', 'rle'), 1)
        self.assertEqual(sim_compression('', '', 'bwtrle'), 1)

        self.assertLess(sim_compression('a', ''), 1)
        self.assertLess(sim_compression('a', '', 'bzip2'), 1)
        self.assertLess(sim_compression('a', '', 'zlib'), 1)
        self.assertLess(sim_compression('a', '', 'arith'), 1)
        self.assertLess(sim_compression('a', '', 'arith', self.arith_dict), 1)
        self.assertLess(sim_compression('a', '', 'rle'), 1)
        self.assertLess(sim_compression('a', '', 'bwtrle'), 1)

        self.assertLess(sim_compression('abcdefg', 'fg'), 1)
        self.assertLess(sim_compression('abcdefg', 'fg', 'bzip2'), 1)
        self.assertLess(sim_compression('abcdefg', 'fg', 'zlib'), 1)
        self.assertLess(sim_compression('abcdefg', 'fg', 'arith'), 1)
        self.assertLess(sim_compression('abcdefg', 'fg', 'rle'), 1)
        self.assertLess(sim_compression('abcdefg', 'fg', 'bwtrle'), 1)

    def test_sim_compression_arith(self):
        """Test abydos.distance.sim_compression (arithmetric compression)."""
        self.assertAlmostEqual(sim_compression('Niall', 'Neil', 'arith',
                                               self.arith_dict),
                               0.3913043478260869)
        self.assertAlmostEqual(sim_compression('Neil', 'Niall', 'arith',
                                               self.arith_dict),
                               0.3913043478260869)
        self.assertAlmostEqual(sim_compression('Niall', 'Neil', 'arith'),
                               0.3125)
        self.assertAlmostEqual(sim_compression('Neil', 'Niall', 'arith'),
                               0.3125)
        self.assertAlmostEqual(sim_compression('Njáll', 'Njall', 'arith',
                                               self.arith_dict),
                               0.285714285714285)
        self.assertAlmostEqual(sim_compression('Njall', 'Njáll', 'arith',
                                               self.arith_dict),
                               0.285714285714285)
        self.assertAlmostEqual(sim_compression('Njáll', 'Njall', 'arith'),
                               0.25)
        self.assertAlmostEqual(sim_compression('Njall', 'Njáll', 'arith'),
                               0.25)

    def test_sim_compression_rle(self):
        """Test abydos.distance.sim_compression (RLE & BWT+RLE)."""
        self.assertAlmostEqual(sim_compression('abc', 'abc', 'rle'), 1)
        self.assertAlmostEqual(sim_compression('abc', 'def', 'rle'), 0)

        self.assertAlmostEqual(sim_compression('abc', 'abc', 'bwtrle'), 1)
        self.assertAlmostEqual(sim_compression('abc', 'def', 'bwtrle'), 0.25)

        self.assertAlmostEqual(sim_compression('aaa', 'bbaaa', 'rle'), 0.5)
        self.assertAlmostEqual(sim_compression('abb', 'bbba', 'rle'), 2/3)
        self.assertAlmostEqual(sim_compression('banana', 'banane', 'bwtrle'),
                               0.42857142857)
        self.assertAlmostEqual(sim_compression('bananas', 'bananen', 'bwtrle'),
                               0.5)

    def test_lzma(self):
        """Test abydos.distance.sim_compression LZMA-related functions."""
        if bool(pkgutil.find_loader('lzma')):
            self.assertEqual(dist_compression('', '', 'lzma'), 0)
            self.assertGreater(dist_compression('a', '', 'lzma'), 0)
            self.assertGreater(dist_compression('abcdefg', 'fg', 'lzma'), 0)
            self.assertEqual(sim_compression('', '', 'lzma'), 1)
            self.assertLess(sim_compression('a', '', 'lzma'), 1)
            self.assertLess(sim_compression('abcdefg', 'fg', 'lzma'), 1)
            del sys.modules['lzma']

        self.assertRaises(ValueError, dist_compression, 'a', '', 'lzma')


if __name__ == '__main__':
    unittest.main()
