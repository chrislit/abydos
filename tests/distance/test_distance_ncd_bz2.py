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

"""abydos.tests.distance.test_distance_ncd_bz2.

This module contains unit tests for abydos.distance.NCDbz2
"""

import unittest

from abydos.distance import NCDbz2


class CompressionTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.NCDbz2
    """

    cmp = NCDbz2()

    def test_ncd_bz2_dist(self):
        """Test abydos.distance.NCDbz2.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertGreater(self.cmp.dist('a', ''), 0)
        self.assertAlmostEqual(self.cmp.dist('abcdefg', 'fg'), 0.15625)

    def test_ncd_bz2_sim(self):
        """Test abydos.distance.NCDbz2.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertLess(self.cmp.sim('a', ''), 1)
        self.assertAlmostEqual(self.cmp.sim('abcdefg', 'fg'), 0.84375)


if __name__ == '__main__':
    unittest.main()
