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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import YatesChiSquared


class YatesChiSquaredTestCases(unittest.TestCase):
    """Test YatesChiSquared functions.

    abydos.distance.YatesChiSquared
    """

    cmp = YatesChiSquared()
    cmp_no_d = YatesChiSquared(alphabet=1)

    def test_yates_chi_squared_sim(self):
        """Test abydos.distance.YatesChiSquared.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 599.3708349769888)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 6.960385076156687)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 133.1878178031)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 133.1878178031)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 133.1878178031)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 133.1878178031)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 296.1470911771
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 6.4)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.5625)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.5625)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.5625)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.5625)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.2651515152
        )

    def test_yates_chi_squared_dist(self):
        """Test abydos.distance.YatesChiSquared.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), -598.3708349769888)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), -5.960385076156687)

        self.assertAlmostEqual(
            self.cmp.dist('Nigel', 'Niall'), -132.1878178031
        )
        self.assertAlmostEqual(
            self.cmp.dist('Niall', 'Nigel'), -132.1878178031
        )
        self.assertAlmostEqual(
            self.cmp.dist('Colin', 'Coiln'), -132.1878178031
        )
        self.assertAlmostEqual(
            self.cmp.dist('Coiln', 'Colin'), -132.1878178031
        )
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), -295.1470911771
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), -5.4)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.4375)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.4375)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.4375)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.4375)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.7348484848
        )


if __name__ == '__main__':
    unittest.main()