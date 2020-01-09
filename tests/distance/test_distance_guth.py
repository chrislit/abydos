# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_guth.

This module contains unit tests for abydos.distance.Guth
"""

import unittest

from abydos.distance import Guth


class GuthTestCases(unittest.TestCase):
    """Test Guth functions.

    abydos.distance.Guth
    """

    cmp = Guth()

    def test_guth_sim_score(self):
        """Test abydos.distance.Guth.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 1.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('a', 'a'), 1.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        # Testcases from paper
        self.assertEqual(self.cmp.sim_score('Glawyn', 'Glavin'), 1.0)
        self.assertEqual(self.cmp.sim_score('Smears', 'Smares'), 1.0)
        self.assertEqual(self.cmp.sim_score('Giddings', 'Gittins'), 1.0)
        self.assertEqual(self.cmp.sim_score('Bokenham', 'Buckingham'), 0.0)

        # coverage
        self.assertAlmostEqual(
            Guth(qval=2).sim_score('Giddings', 'Gittins'), 0.0
        )

    def test_guth_sim(self):
        """Test abydos.distance.Guth.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        # Testcases from paper
        self.assertAlmostEqual(self.cmp.sim('Glawyn', 'Glavin'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('Smears', 'Smares'), 0.86666666666)
        self.assertAlmostEqual(self.cmp.sim('Giddings', 'Gittins'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('Bokenham', 'Buckingham'), 0.65)

        # coverage
        self.assertAlmostEqual(Guth(qval=2).sim('Giddings', 'Gittins'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('abcfefed', 'abcfed'), 0.7)


if __name__ == '__main__':
    unittest.main()
