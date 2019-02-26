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

"""abydos.tests.distance.test_distance_unknown_k.

This module contains unit tests for abydos.distance.UnknownK
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import UnknownK


class UnknownKTestCases(unittest.TestCase):
    """Test UnknownK functions.

    abydos.distance.UnknownK
    """

    cmp = UnknownK()
    cmp_no_d = UnknownK(alphabet=0)

    def test_unknown_k_sim(self):
        """Test abydos.distance.UnknownK.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 3.979591836734694)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 2.9885204082)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 2.9885204082)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 2.9885204082)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 2.9885204082)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 6.9375)

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 2.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 3.5
        )

    def test_unknown_k_dist(self):
        """Test abydos.distance.UnknownK.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), -2.979591836734694)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), -1.9885204082)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), -1.9885204082)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), -1.9885204082)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), -1.9885204082)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), -5.9375
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), -1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), -2.5
        )


if __name__ == '__main__':
    unittest.main()
