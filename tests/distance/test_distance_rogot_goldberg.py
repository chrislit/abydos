# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_rogot_goldberg.

This module contains unit tests for abydos.distance.RogotGoldberg
"""

import unittest

from abydos.distance import RogotGoldberg


class RogotGoldbergTestCases(unittest.TestCase):
    """Test RogotGoldberg functions.

    abydos.distance.RogotGoldberg
    """

    cmp = RogotGoldberg()
    cmp_no_d = RogotGoldberg(alphabet=0)

    def test_rogot_goldberg_sim(self):
        """Test abydos.distance.RogotGoldberg.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.49936143039591313)
        self.assertEqual(self.cmp.sim('', 'a'), 0.49936143039591313)
        self.assertEqual(self.cmp.sim('abc', ''), 0.49872122762148335)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.49872122762148335)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7480719794)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.8310708899
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.25)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.3333333333
        )

    def test_rogot_goldberg_dist(self):
        """Test abydos.distance.RogotGoldberg.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.5006385696040869)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5006385696040869)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5012787723785166)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5012787723785166)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.503209242618742)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2519280206)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.1689291101
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.75)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.6666666667
        )


if __name__ == '__main__':
    unittest.main()
