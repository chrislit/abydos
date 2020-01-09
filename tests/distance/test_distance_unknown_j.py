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

"""abydos.tests.distance.test_distance_unknown_j.

This module contains unit tests for abydos.distance.UnknownJ
"""

import unittest

from abydos.distance import UnknownJ


class UnknownJTestCases(unittest.TestCase):
    """Test UnknownJ functions.

    abydos.distance.UnknownJ
    """

    cmp = UnknownJ()
    cmp_no_d = UnknownJ(alphabet=0)

    def test_unknown_j_sim(self):
        """Test abydos.distance.UnknownJ.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6363636364
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.1785714286
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.1785714286
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.1785714286
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.1785714286
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.1988636364
        )

    def test_unknown_j_dist(self):
        """Test abydos.distance.UnknownJ.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3636363636
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.8214285714
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.8214285714
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.8214285714
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.8214285714
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.8011363636
        )

    def test_unknown_j_sim_score(self):
        """Test abydos.distance.UnknownJ.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 1.005128205128205)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 0.5038560411
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 0.5038560411
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 0.5038560411
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 0.5038560411
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.6454192638
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 5.0)
        self.assertEqual(self.cmp_no_d.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim_score('Nigel', 'Niall'), 1.25)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Niall', 'Nigel'), 1.25)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Colin', 'Coiln'), 1.25)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Coiln', 'Colin'), 1.25)
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), 2.3863636364
        )


if __name__ == '__main__':
    unittest.main()
