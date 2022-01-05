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

"""abydos.tests.distance.test_distance_kuhns_xii.

This module contains unit tests for abydos.distance.KuhnsXII
"""

import unittest

from abydos.distance import KuhnsXII


class KuhnsXIITestCases(unittest.TestCase):
    """Test KuhnsXII functions.

    abydos.distance.KuhnsXII
    """

    cmp = KuhnsXII()
    cmp_no_d = KuhnsXII(alphabet=0)

    def test_kuhns_xii_sim(self):
        """Test abydos.distance.KuhnsXII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.2490322581)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.2490322581)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.2490322581)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.2490322581)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4444628099
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.375)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.375)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.375)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.375)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.4454545455
        )

    def test_kuhns_xii_dist(self):
        """Test abydos.distance.KuhnsXII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.7509677419)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.7509677419)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.7509677419)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.7509677419)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5555371901
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.625)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.625)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.625)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.625)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5545454545
        )

    def test_kuhns_xii_sim_score(self):
        """Test abydos.distance.KuhnsXII.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 195.0)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 64.3333333333
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 64.3333333333
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 64.3333333333
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 64.3333333333
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 48.8909090909
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), -0.25
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), -0.25
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), -0.25
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), -0.25
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), -0.1090909091
        )


if __name__ == '__main__':
    unittest.main()
