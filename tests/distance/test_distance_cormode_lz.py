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

"""abydos.tests.distance.test_distance_cormode_lz.

This module contains unit tests for abydos.distance.CormodeLZ
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import CormodeLZ


class CormodeLZTestCases(unittest.TestCase):
    """Test CormodeLZ functions.

    abydos.distance.CormodeLZ
    """

    cmp = CormodeLZ()

    def test_cormode_lz_dist(self):
        """Test abydos.distance.CormodeLZ.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), -0.0)
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), -0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.5)
        self.assertEqual(self.cmp.dist('', 'abc'), -0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.3333333333333333)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.75)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.75)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.75)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.75)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4444444444
        )

    def test_cormode_lz_sim(self):
        """Test abydos.distance.CormodeLZ.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), -0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.33333333333333326)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.25)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.25)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.25)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.25)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5555555556
        )

    def test_cormode_lz_dist_abs(self):
        """Test abydos.distance.CormodeLZ.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 1)
        self.assertEqual(self.cmp.dist_abs('a', ''), 2)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 4)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 1)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 5)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 4)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 4)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 4)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 4)
        self.assertAlmostEqual(self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 5)


if __name__ == '__main__':
    unittest.main()
