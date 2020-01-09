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

"""abydos.tests.distance.test_distance_yjhhr.

This module contains unit tests for abydos.distance.YJHHR
"""

import unittest

from abydos.distance import YJHHR


class YJHHRTestCases(unittest.TestCase):
    """Test YJHHR functions.

    abydos.distance.YJHHR
    """

    cmp = YJHHR()
    cmp_p3 = YJHHR(pval=3)

    def test_yjhhr_dist(self):
        """Test abydos.distance.YJHHR.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.6666666666)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.6666666666)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.6666666666)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.6666666666)
        self.assertAlmostEqual(self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5)

        # Base cases
        self.assertEqual(self.cmp_p3.dist('', ''), 0.0)
        self.assertEqual(self.cmp_p3.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_p3.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_p3.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_p3.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_p3.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_p3.dist('abcd', 'efgh'), 0.6299605249474369)

        self.assertAlmostEqual(
            self.cmp_p3.dist('Nigel', 'Niall'), 0.4199736833
        )
        self.assertAlmostEqual(
            self.cmp_p3.dist('Niall', 'Nigel'), 0.4199736833
        )
        self.assertAlmostEqual(
            self.cmp_p3.dist('Colin', 'Coiln'), 0.4199736833
        )
        self.assertAlmostEqual(
            self.cmp_p3.dist('Coiln', 'Colin'), 0.4199736833
        )
        self.assertAlmostEqual(
            self.cmp_p3.dist('ATCAACGAGT', 'AACGATTAG'), 0.32128153180538643
        )

    def test_yjhhr_sim(self):
        """Test abydos.distance.YJHHR.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5)

        # Base cases
        self.assertEqual(self.cmp_p3.sim('', ''), 1.0)
        self.assertEqual(self.cmp_p3.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_p3.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_p3.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_p3.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_p3.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_p3.sim('abcd', 'efgh'), 0.37003947505256307)

        self.assertAlmostEqual(self.cmp_p3.sim('Nigel', 'Niall'), 0.5800263167)
        self.assertAlmostEqual(self.cmp_p3.sim('Niall', 'Nigel'), 0.5800263167)
        self.assertAlmostEqual(self.cmp_p3.sim('Colin', 'Coiln'), 0.5800263167)
        self.assertAlmostEqual(self.cmp_p3.sim('Coiln', 'Colin'), 0.5800263167)
        self.assertAlmostEqual(
            self.cmp_p3.sim('ATCAACGAGT', 'AACGATTAG'), 0.6787184681946136
        )

    def test_yjhhr_dist_abs(self):
        """Test abydos.distance.YJHHR.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 2.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 2.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 4.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 4.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 10.0)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 6.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 6.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 6.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 6.0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 7.0
        )

        # Base cases
        self.assertEqual(self.cmp_p3.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp_p3.dist_abs('a', ''), 2.0)
        self.assertEqual(self.cmp_p3.dist_abs('', 'a'), 2.0)
        self.assertEqual(self.cmp_p3.dist_abs('abc', ''), 4.0)
        self.assertEqual(self.cmp_p3.dist_abs('', 'abc'), 4.0)
        self.assertEqual(self.cmp_p3.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_p3.dist_abs('abcd', 'efgh'), 6.29960524947437
        )

        self.assertAlmostEqual(
            self.cmp_p3.dist_abs('Nigel', 'Niall'), 3.77976314968462
        )
        self.assertAlmostEqual(
            self.cmp_p3.dist_abs('Niall', 'Nigel'), 3.77976314968462
        )
        self.assertAlmostEqual(
            self.cmp_p3.dist_abs('Colin', 'Coiln'), 3.77976314968462
        )
        self.assertAlmostEqual(
            self.cmp_p3.dist_abs('Coiln', 'Colin'), 3.77976314968462
        )
        self.assertAlmostEqual(
            self.cmp_p3.dist_abs('ATCAACGAGT', 'AACGATTAG'), 4.49794144527541
        )


if __name__ == '__main__':
    unittest.main()
