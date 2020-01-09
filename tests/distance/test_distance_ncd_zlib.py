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

"""abydos.tests.distance.test_distance_ncd_zlib.

This module contains unit tests for abydos.distance.compression
"""

import unittest

from abydos.distance import NCDzlib, dist_ncd_zlib, sim_ncd_zlib


class CompressionTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.NCDzlib
    """

    cmp = NCDzlib()

    def test_ncd_zlib_dist(self):
        """Test abydos.distance.NCDzlib.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertGreater(self.cmp.dist('a', ''), 0)
        self.assertAlmostEqual(self.cmp.dist('abcdefg', 'fg'), 0.5384615384615)

        # Test wrapper
        self.assertAlmostEqual(dist_ncd_zlib('abcdefg', 'fg'), 0.5384615384615)

    def test_ncd_zlib_sim(self):
        """Test abydos.distance.NCDzlib.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertLess(self.cmp.sim('a', ''), 1)
        self.assertAlmostEqual(self.cmp.sim('abcdefg', 'fg'), 0.46153846153846)

        # Test wrapper
        self.assertAlmostEqual(sim_ncd_zlib('abcdefg', 'fg'), 0.46153846153846)


if __name__ == '__main__':
    unittest.main()
