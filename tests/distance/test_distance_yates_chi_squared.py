# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_yates_chi_squared.

This module contains unit tests for abydos.distance.YatesChiSquared
"""

import unittest

from abydos.distance import YatesChiSquared


class YatesChiSquaredTestCases(unittest.TestCase):
    """Test YatesChiSquared functions.

    abydos.distance.YatesChiSquared
    """

    cmp = YatesChiSquared()
    cmp_no_d = YatesChiSquared(alphabet=0)
    cmp_4q1 = YatesChiSquared(qval=1, alphabet=6)

    def test_yates_chi_squared_sim(self):
        """Test abydos.distance.YatesChiSquared.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.2024579068)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.2024579068)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.2024579068)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.2024579068)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.415132719
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0
        )

    def test_yates_chi_squared_dist(self):
        """Test abydos.distance.YatesChiSquared.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.7975420932)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.7975420932)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.7975420932)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.7975420932)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.584867281
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.0
        )

    def test_yates_chi_squared_sim_score(self):
        """Test abydos.distance.YatesChiSquared.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 599.3708349769888)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 6.960385076156687)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 133.1878178031
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 133.1878178031
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 133.1878178031
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 133.1878178031
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 296.1470911771
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 1.0)
        self.assertEqual(
            self.cmp_no_d.sim_score('abcd', 'efgh', signed=True), -6.4
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall', signed=True), -0.5625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel', signed=True), -0.5625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln', signed=True), -0.5625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin', signed=True), -0.5625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG', signed=True),
            -0.2651515152,
        )

        self.assertEqual(self.cmp_4q1.sim_score('tab', 'tac'), 0.0)


if __name__ == '__main__':
    unittest.main()
