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
from abydos.distance.compression import dist_ncd_arith, dist_ncd_bwtrle, \
    dist_ncd_bz2, dist_ncd_lzma, dist_ncd_rle, dist_ncd_zlib, sim_ncd_arith, \
    sim_ncd_bwtrle, sim_ncd_bz2, sim_ncd_lzma, sim_ncd_rle, sim_ncd_zlib

from .. import NIALL


class CompressionTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.compression.dist_ncd_arith, .dist_ncd_bwtrle,
    .dist_ncd_bz2, .dist_ncd_lzma, .dist_ncd_rle, .dist_ncd_zlib,
    .sim_ncd_arith, .sim_ncd_bwtrle, .sim_ncd_bz2, .sim_ncd_lzma, .sim_ncd_rle,
    & .sim_ncd_zlib
    """

    arith_dict = arithmetic.train(' '.join(NIALL))

    def test_dist_ncd_bz2(self):
        """Test abydos.distance.compression.dist_ncd_bz2."""
        self.assertEqual(dist_ncd_bz2('', ''), 0)
        self.assertGreater(dist_ncd_bz2('a', ''), 0)
        self.assertGreater(dist_ncd_bz2('abcdefg', 'fg'), 0)

    def test_dist_ncd_zlib(self):
        """Test abydos.distance.compression.dist_ncd_zlib."""
        self.assertEqual(dist_ncd_zlib('', ''), 0)
        self.assertGreater(dist_ncd_zlib('a', ''), 0)
        self.assertGreater(dist_ncd_zlib('abcdefg', 'fg'), 0)

    def test_dist_ncd_arith(self):
        """Test abydos.distance.compression.dist_ncd_arith."""
        self.assertEqual(dist_ncd_arith('', ''), 0)
        self.assertEqual(dist_ncd_arith('', '', self.arith_dict), 0)
        self.assertGreater(dist_ncd_arith('a', ''), 0)
        self.assertGreater(dist_ncd_arith('a', '', self.arith_dict), 0)
        self.assertGreater(dist_ncd_arith('abcdefg', 'fg'), 0)

        self.assertAlmostEqual(dist_ncd_arith('Niall', 'Neil',
                                              self.arith_dict),
                               0.608695652173913)
        self.assertAlmostEqual(dist_ncd_arith('Neil', 'Niall',
                                              self.arith_dict),
                               0.608695652173913)
        self.assertAlmostEqual(dist_ncd_arith('Niall', 'Neil'),
                               0.6875)
        self.assertAlmostEqual(dist_ncd_arith('Neil', 'Niall'),
                               0.6875)
        self.assertAlmostEqual(dist_ncd_arith('Njáll', 'Njall',
                                              self.arith_dict),
                               0.714285714285714)
        self.assertAlmostEqual(dist_ncd_arith('Njall', 'Njáll',
                                              self.arith_dict),
                               0.714285714285714)
        self.assertAlmostEqual(dist_ncd_arith('Njáll', 'Njall'), 0.75)
        self.assertAlmostEqual(dist_ncd_arith('Njall', 'Njáll'), 0.75)

    def test_dist_ncd_bwtrle(self):
        """Test abydos.distance..compression.dist_ncd_bwtrle."""
        self.assertEqual(dist_ncd_bwtrle('', ''), 0)
        self.assertGreater(dist_ncd_bwtrle('a', ''), 0)
        self.assertGreater(dist_ncd_bwtrle('abcdefg', 'fg'), 0)

        self.assertAlmostEqual(dist_ncd_bwtrle('abc', 'abc'), 0)
        self.assertAlmostEqual(dist_ncd_bwtrle('abc', 'def'), 0.75)

        self.assertAlmostEqual(dist_ncd_bwtrle('banana', 'banane'),
                               0.57142857142)
        self.assertAlmostEqual(dist_ncd_bwtrle('bananas', 'bananen'), 0.5)

    def test_dist_ncd_rle(self):
        """Test abydos.distance..compression.dist_ncd_rle."""
        self.assertEqual(dist_ncd_rle('', ''), 0)
        self.assertGreater(dist_ncd_rle('a', ''), 0)
        self.assertGreater(dist_ncd_rle('abcdefg', 'fg'), 0)

        self.assertAlmostEqual(dist_ncd_rle('abc', 'abc'), 0)
        self.assertAlmostEqual(dist_ncd_rle('abc', 'def'), 1)

        self.assertAlmostEqual(dist_ncd_rle('aaa', 'bbaaa'), 0.5)
        self.assertAlmostEqual(dist_ncd_rle('abb', 'bbba'), 1/3)

    def test_sim_ncd_bz2(self):
        """Test abydos.distance.compression.sim_ncd_bz2."""
        self.assertEqual(sim_ncd_bz2('', ''), 1)
        self.assertLess(sim_ncd_bz2('a', ''), 1)
        self.assertLess(sim_ncd_bz2('abcdefg', 'fg'), 1)

    def test_sim_ncd_zlib(self):
        """Test abydos.distance.compression.sim_ncd_zlib."""
        self.assertEqual(sim_ncd_zlib('', ''), 1)
        self.assertLess(sim_ncd_zlib('a', ''), 1)
        self.assertLess(sim_ncd_zlib('abcdefg', 'fg'), 1)

    def test_sim_ncd_arith(self):
        """Test abydos.distance.compression.sim_ncd_arith."""
        self.assertEqual(sim_ncd_arith('', ''), 1)
        self.assertEqual(sim_ncd_arith('', '', self.arith_dict), 1)
        self.assertLess(sim_ncd_arith('a', ''), 1)
        self.assertLess(sim_ncd_arith('a', '', self.arith_dict), 1)
        self.assertLess(sim_ncd_arith('abcdefg', 'fg'), 1)

        self.assertAlmostEqual(sim_ncd_arith('Niall', 'Neil', self.arith_dict),
                               0.3913043478260869)
        self.assertAlmostEqual(sim_ncd_arith('Neil', 'Niall', self.arith_dict),
                               0.3913043478260869)
        self.assertAlmostEqual(sim_ncd_arith('Niall', 'Neil'), 0.3125)
        self.assertAlmostEqual(sim_ncd_arith('Neil', 'Niall'), 0.3125)
        self.assertAlmostEqual(sim_ncd_arith('Njáll', 'Njall',
                                             self.arith_dict),
                               0.285714285714285)
        self.assertAlmostEqual(sim_ncd_arith('Njall', 'Njáll',
                                             self.arith_dict),
                               0.285714285714285)
        self.assertAlmostEqual(sim_ncd_arith('Njáll', 'Njall'), 0.25)
        self.assertAlmostEqual(sim_ncd_arith('Njall', 'Njáll'), 0.25)

    def test_sim_ncd_rle(self):
        """Test abydos.distance.sim_ncd_rle."""
        self.assertEqual(sim_ncd_rle('', ''), 1)
        self.assertLess(sim_ncd_rle('a', ''), 1)
        self.assertLess(sim_ncd_rle('abcdefg', 'fg'), 1)

        self.assertAlmostEqual(sim_ncd_rle('abc', 'abc'), 1)
        self.assertAlmostEqual(sim_ncd_rle('abc', 'def'), 0)

        self.assertAlmostEqual(sim_ncd_rle('aaa', 'bbaaa'), 0.5)
        self.assertAlmostEqual(sim_ncd_rle('abb', 'bbba'), 2/3)

    def test_sim_ncd_bwtrle(self):
        """Test abydos.distance.sim_ncd_bwtrle."""
        self.assertEqual(sim_ncd_bwtrle('', ''), 1)
        self.assertLess(sim_ncd_bwtrle('a', ''), 1)
        self.assertLess(sim_ncd_bwtrle('abcdefg', 'fg'), 1)

        self.assertAlmostEqual(sim_ncd_bwtrle('abc', 'abc'), 1)
        self.assertAlmostEqual(sim_ncd_bwtrle('abc', 'def'), 0.25)

        self.assertAlmostEqual(sim_ncd_bwtrle('banana', 'banane'),
                               0.42857142857)
        self.assertAlmostEqual(sim_ncd_bwtrle('bananas', 'bananen'), 0.5)

    def test_sim_ncd_lzma(self):
        """Test abydos.distance.compression.dist_ncd_lzma & .sim_ncd_lzma."""
        if bool(pkgutil.find_loader('lzma')):
            self.assertEqual(sim_ncd_lzma('', ''), 1)
            self.assertLess(sim_ncd_lzma('a', ''), 1)
            self.assertLess(sim_ncd_lzma('abcdefg', 'fg'), 1)

            self.assertEqual(dist_ncd_lzma('', ''), 0)
            self.assertGreater(dist_ncd_lzma('a', ''), 0)
            self.assertGreater(dist_ncd_lzma('abcdefg', 'fg'), 0)
            del sys.modules['lzma']

        self.assertRaises(ValueError, sim_ncd_lzma, 'a', '')


if __name__ == '__main__':
    unittest.main()
