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

"""abydos.tests.distance.test_distance_ncd_rle.

This module contains unit tests for abydos.distance.NCDrle
"""

import unittest

from abydos.distance import NCDrle


class CompressionTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.NCDrle
    """

    cmp = NCDrle()

    def test_ncd_rle_dist(self):
        """Test abydos.distance.NCDrle.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertGreater(self.cmp.dist('a', ''), 0)
        self.assertGreater(self.cmp.dist('abcdefg', 'fg'), 0)

        self.assertAlmostEqual(self.cmp.dist('abc', 'abc'), 0)
        self.assertAlmostEqual(self.cmp.dist('abc', 'def'), 1)

        self.assertAlmostEqual(self.cmp.dist('aaa', 'bbaaa'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('abb', 'bbba'), 1 / 3)

    def test_ncd_rle_sim(self):
        """Test abydos.distance.NCDrle.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertLess(self.cmp.sim('a', ''), 1)
        self.assertLess(self.cmp.sim('abcdefg', 'fg'), 1)

        self.assertAlmostEqual(self.cmp.sim('abc', 'abc'), 1)
        self.assertAlmostEqual(self.cmp.sim('abc', 'def'), 0)

        self.assertAlmostEqual(self.cmp.sim('aaa', 'bbaaa'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('abb', 'bbba'), 2 / 3)


if __name__ == '__main__':
    unittest.main()
