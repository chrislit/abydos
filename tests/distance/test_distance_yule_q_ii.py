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

"""abydos.tests.distance.test_distance_yule_q_ii.

This module contains unit tests for abydos.distance.YuleQII
"""

import unittest

from abydos.distance import YuleQII


class YuleQIITestCases(unittest.TestCase):
    """Test YuleQII functions.

    abydos.distance.YuleQII
    """

    cmp = YuleQII()
    cmp_no_d = YuleQII(alphabet=0)

    def test_yule_q_ii_dist(self):
        """Test abydos.distance.YuleQII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0038560411)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0022213995
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.0
        )

    def test_yule_q_ii_sim(self):
        """Test abydos.distance.YuleQII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9961439589)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9977786005
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0
        )

    def test_yule_q_ii_dist_abs(self):
        """Test abydos.distance.YuleQII.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 0.0077120823
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 0.0077120823
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 0.0077120823
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 0.0077120823
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 0.004442799
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(self.cmp_no_d.dist_abs('Nigel', 'Niall'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist_abs('Niall', 'Nigel'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist_abs('Colin', 'Coiln'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist_abs('Coiln', 'Colin'), 2.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('ATCAACGAGT', 'AACGATTAG'), 2.0
        )


if __name__ == '__main__':
    unittest.main()
