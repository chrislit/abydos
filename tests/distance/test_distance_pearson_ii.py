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

"""abydos.tests.distance.test_distance_pearson_ii.

This module contains unit tests for abydos.distance.PearsonII
"""

import unittest

from abydos.distance import PearsonII


class PearsonIITestCases(unittest.TestCase):
    """Test PearsonII functions.

    abydos.distance.PearsonII
    """

    cmp = PearsonII()
    cmp_no_d = PearsonII(alphabet=0)

    def test_pearson_ii_sim(self):
        """Test abydos.distance.PearsonII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.009076921903905551)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.628544465)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.628544465)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.628544465)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.628544465)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.781408328
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.632455532
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.632455532
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.632455532
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.632455532
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.4435327626
        )

    def test_pearson_ii_dist(self):
        """Test abydos.distance.PearsonII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.9909230780960945)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.371455535)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.371455535)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.371455535)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.371455535)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.218591672
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.367544468
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.367544468
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.367544468
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.367544468
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5564672374
        )

    def test_pearson_ii_sim_score(self):
        """Test abydos.distance.PearsonII.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.7071067811865476)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 0.7071067811865476)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), 0.006418353030552324
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 0.4444480535
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 0.4444480535
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 0.4444480535
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 0.4444480535
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.5525391276
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.7071067811865476)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.sim_score('abc', 'abc'), 0.7071067811865476
        )
        self.assertEqual(
            self.cmp_no_d.sim_score('abcd', 'efgh'), 0.7071067811865476
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), 0.4472135955
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), 0.4472135955
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), 0.4472135955
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), 0.4472135955
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.3136250241
        )


if __name__ == '__main__':
    unittest.main()
