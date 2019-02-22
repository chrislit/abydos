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

"""abydos.tests.distance.test_distance_batagelj_bren.

This module contains unit tests for abydos.distance.BatageljBren
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import BatageljBren


class BatageljBrenTestCases(unittest.TestCase):
    """Test BatageljBren functions.

    abydos.distance.BatageljBren
    """

    cmp = BatageljBren()
    cmp_no_d = BatageljBren(alphabet=1)

    def test_batagelj_bren_dist(self):
        """Test abydos.distance.BatageljBren.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 4.9375e-06)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 4.9375e-06)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 4.9375e-06)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 4.9375e-06)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 2.8397e-06
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.0
        )

    def test_batagelj_bren_sim(self):
        """Test abydos.distance.BatageljBren.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9999950625)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9999950625)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9999950625)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9999950625)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9999971603
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0
        )

    def test_batagelj_bren_dist_abs(self):
        """Test abydos.distance.BatageljBren.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('a', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('', 'a'), float('inf'))
        self.assertEqual(self.cmp.dist_abs('abc', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('', 'abc'), float('inf'))
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), float('inf'))

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 0.0038709677
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 0.0038709677
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 0.0038709677
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 0.0038709677
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 0.0022263451
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.dist_abs('', ''), float('inf'))
        self.assertEqual(self.cmp_no_d.dist_abs('a', ''), float('inf'))
        self.assertEqual(self.cmp_no_d.dist_abs('', 'a'), float('inf'))
        self.assertEqual(self.cmp_no_d.dist_abs('abc', ''), float('inf'))
        self.assertEqual(self.cmp_no_d.dist_abs('', 'abc'), float('inf'))
        self.assertEqual(self.cmp_no_d.dist_abs('abc', 'abc'), float('inf'))
        self.assertEqual(self.cmp_no_d.dist_abs('abcd', 'efgh'), float('inf'))

        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('Nigel', 'Niall'), float('inf')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('Niall', 'Nigel'), float('inf')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('Colin', 'Coiln'), float('inf')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('Coiln', 'Colin'), float('inf')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('ATCAACGAGT', 'AACGATTAG'), float('inf')
        )


if __name__ == '__main__':
    unittest.main()
