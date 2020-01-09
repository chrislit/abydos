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

"""abydos.tests.distance.test_distance_flexmetric.

This module contains unit tests for abydos.distance.FlexMetric
"""

import unittest

from abydos.distance import FlexMetric


class FlexMetricTestCases(unittest.TestCase):
    """Test FlexMetric functions.

    abydos.distance.FlexMetric
    """

    cmp = FlexMetric()
    cmp_custom = FlexMetric(
        indel_costs=[(set('aeiou'), 0.1), (set('bcdfghjklmnpqrstvwxyz'), 0.9)],
        subst_costs=[(set('aeiou'), 0.1), (set('bcdfghjklmnpqrstvwxyz'), 0.9)],
    )

    def test_flexmetric_dist(self):
        """Test abydos.distance.FlexMetric.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('abc', ''), 0.7999999999999999)
        self.assertAlmostEqual(self.cmp.dist('', 'abc'), 0.7999999999999999)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertAlmostEqual(self.cmp.dist('abcd', 'efgh'), 0.925)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.26)

    def test_flexmetric_sim(self):
        """Test abydos.distance.FlexMetric.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('abc', ''), 0.20000000000000007)
        self.assertAlmostEqual(self.cmp.sim('', 'abc'), 0.20000000000000007)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertAlmostEqual(self.cmp.sim('abcd', 'efgh'), 0.075)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.74)

    def test_flexmetric_dist_abs(self):
        """Test abydos.distance.FlexMetric.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 2.4)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 2.4)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('abcd', 'efgh'), 3.6999999999999997
        )

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 1.5)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 1.5)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 2.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 2.0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 2.6
        )

        self.assertAlmostEqual(self.cmp_custom.dist_abs('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_custom.dist_abs('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_custom.dist_abs('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(self.cmp_custom.dist_abs('Coiln', 'Colin'), 0.2)
        self.assertAlmostEqual(
            self.cmp_custom.dist_abs('ATCAACGAGT', 'AACGATTAG'), 3.7
        )


if __name__ == '__main__':
    unittest.main()
