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

"""abydos.tests.distance.test_distance_mra.

This module contains unit tests for abydos.distance.MRA
"""

import unittest

from abydos.distance import MRA, dist_mra, mra_compare, sim_mra


class MraTestCases(unittest.TestCase):
    """Test MRA functions.

    abydos.distance.MRA
    """

    cmp = MRA()

    def test_mra_dist_abs(self):
        """Test abydos.distance.MRA.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 6)
        self.assertEqual(self.cmp.dist_abs('a', 'a'), 6)
        self.assertEqual(self.cmp.dist_abs('abcdefg', 'abcdefg'), 6)
        self.assertEqual(self.cmp.dist_abs('abcdefg', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', 'abcdefg'), 0)

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEqual(self.cmp.dist_abs('Byrne', 'Boern'), 5)
        self.assertEqual(self.cmp.dist_abs('Smith', 'Smyth'), 5)
        self.assertEqual(self.cmp.dist_abs('Catherine', 'Kathryn'), 4)

        self.assertEqual(self.cmp.dist_abs('ab', 'abcdefgh'), 0)
        self.assertEqual(self.cmp.dist_abs('ab', 'ac'), 5)
        self.assertEqual(self.cmp.dist_abs('abcdefik', 'abcdefgh'), 3)
        self.assertEqual(self.cmp.dist_abs('xyz', 'abc'), 0)

        # Test wrapper
        self.assertEqual(mra_compare('Byrne', 'Boern'), 5)

    def test_mra_sim(self):
        """Test abydos.distance.MRA.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('abcdefg', 'abcdefg'), 1)
        self.assertEqual(self.cmp.sim('abcdefg', ''), 0)
        self.assertEqual(self.cmp.sim('', 'abcdefg'), 0)

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEqual(self.cmp.sim('Byrne', 'Boern'), 5 / 6)
        self.assertEqual(self.cmp.sim('Smith', 'Smyth'), 5 / 6)
        self.assertEqual(self.cmp.sim('Catherine', 'Kathryn'), 4 / 6)

        self.assertEqual(self.cmp.sim('ab', 'abcdefgh'), 0)
        self.assertEqual(self.cmp.sim('ab', 'ac'), 5 / 6)
        self.assertEqual(self.cmp.sim('abcdefik', 'abcdefgh'), 3 / 6)
        self.assertEqual(self.cmp.sim('xyz', 'abc'), 0)

        # Test wrapper
        self.assertEqual(sim_mra('Byrne', 'Boern'), 5 / 6)

    def test_mra_dist(self):
        """Test abydos.distance.MRA.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('abcdefg', 'abcdefg'), 0)
        self.assertEqual(self.cmp.dist('abcdefg', ''), 1)
        self.assertEqual(self.cmp.dist('', 'abcdefg'), 1)

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertAlmostEqual(self.cmp.dist('Byrne', 'Boern'), 1 / 6)
        self.assertAlmostEqual(self.cmp.dist('Smith', 'Smyth'), 1 / 6)
        self.assertAlmostEqual(self.cmp.dist('Catherine', 'Kathryn'), 2 / 6)

        self.assertEqual(self.cmp.dist('ab', 'abcdefgh'), 1)
        self.assertAlmostEqual(self.cmp.dist('ab', 'ac'), 1 / 6)
        self.assertAlmostEqual(self.cmp.dist('abcdefik', 'abcdefgh'), 3 / 6)
        self.assertEqual(self.cmp.dist('xyz', 'abc'), 1)

        # Test wrapper
        self.assertAlmostEqual(dist_mra('Byrne', 'Boern'), 1 / 6)


if __name__ == '__main__':
    unittest.main()
