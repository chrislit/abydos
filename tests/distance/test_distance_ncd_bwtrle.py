# -*- coding: utf-8 -*-

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

"""abydos.tests.distance.test_distance_ncd_bwtrle.

This module contains unit tests for abydos.distance.NCDbwtrle
"""

import unittest

from abydos.distance import NCDbwtrle, dist_ncd_bwtrle, sim_ncd_bwtrle


class NCDbwtrleTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.NCDbwtrle
    """

    cmp = NCDbwtrle()

    def test_ncd_bwtrle_dist(self):
        """Test abydos.distance.NCDbwtrle.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertGreater(self.cmp.dist('a', ''), 0)
        self.assertGreater(self.cmp.dist('abcdefg', 'fg'), 0)

        self.assertAlmostEqual(self.cmp.dist('abc', 'abc'), 0)
        self.assertAlmostEqual(self.cmp.dist('abc', 'def'), 0.75)

        self.assertAlmostEqual(
            self.cmp.dist('banana', 'banane'), 0.57142857142
        )
        self.assertAlmostEqual(self.cmp.dist('bananas', 'bananen'), 0.5)

        # Test wrapper
        self.assertAlmostEqual(
            dist_ncd_bwtrle('banana', 'banane'), 0.57142857142
        )

    def test_ncd_bwtrle_sim(self):
        """Test abydos.distance.NCDbwtrle.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertLess(self.cmp.sim('a', ''), 1)
        self.assertLess(self.cmp.sim('abcdefg', 'fg'), 1)

        self.assertAlmostEqual(self.cmp.sim('abc', 'abc'), 1)
        self.assertAlmostEqual(self.cmp.sim('abc', 'def'), 0.25)

        self.assertAlmostEqual(self.cmp.sim('banana', 'banane'), 0.42857142857)
        self.assertAlmostEqual(self.cmp.sim('bananas', 'bananen'), 0.5)

        # Test wrapper
        self.assertAlmostEqual(
            sim_ncd_bwtrle('banana', 'banane'), 0.42857142857
        )


if __name__ == '__main__':
    unittest.main()
