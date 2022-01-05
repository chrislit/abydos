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

"""abydos.tests.distance.test_distance_unknown_k.

This module contains unit tests for abydos.distance.UnknownK
"""

import unittest

from abydos.distance import UnknownK


class UnknownKTestCases(unittest.TestCase):
    """Test UnknownK functions.

    abydos.distance.UnknownK
    """

    cmp = UnknownK()
    cmp_no_d = UnknownK(alphabet=0)

    def test_unknown_k_dist(self):
        """Test abydos.distance.UnknownK.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.9948979591836735)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.9961734694)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.9961734694)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.9961734694)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.9961734694)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.9910714286
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

    def test_unknown_k_sim(self):
        """Test abydos.distance.UnknownK.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.005102040816326481)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0038265306)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0038265306)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0038265306)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0038265306)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0089285714
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

    def test_unknown_k_dist_abs(self):
        """Test abydos.distance.UnknownK.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 784.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 784.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 784.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 784.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 784.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 780.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 784.0)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 781.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 781.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 781.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 781.0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 777.0
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('a', ''), 2.0)
        self.assertEqual(self.cmp_no_d.dist_abs('', 'a'), 2.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abc', ''), 4.0)
        self.assertEqual(self.cmp_no_d.dist_abs('', 'abc'), 4.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abcd', 'efgh'), 10.0)

        self.assertAlmostEqual(self.cmp_no_d.dist_abs('Nigel', 'Niall'), 6.0)
        self.assertAlmostEqual(self.cmp_no_d.dist_abs('Niall', 'Nigel'), 6.0)
        self.assertAlmostEqual(self.cmp_no_d.dist_abs('Colin', 'Coiln'), 6.0)
        self.assertAlmostEqual(self.cmp_no_d.dist_abs('Coiln', 'Colin'), 6.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('ATCAACGAGT', 'AACGATTAG'), 7.0
        )


if __name__ == '__main__':
    unittest.main()
