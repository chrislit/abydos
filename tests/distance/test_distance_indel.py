# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_indel.

This module contains unit tests for abydos.distance.Indel
"""

import unittest

from abydos.distance import Indel, dist_indel, indel, sim_indel


class IndelTestCases(unittest.TestCase):
    """Test indel functions.

    abydos.distance.Indel
    """

    cmp = Indel()

    def test_indel_sim(self):
        """Test abydos.distance.Indel.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('a', ''), 0)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('abc', ''), 0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.8)

        # Test wrapper
        self.assertAlmostEqual(sim_indel('Colin', 'Coiln'), 0.8)

    def test_indel_dist(self):
        """Test abydos.distance.Indel.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('a', ''), 1)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('abc', ''), 1)
        self.assertEqual(self.cmp.dist('', 'abc'), 1)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2)

        # Test wrapper
        self.assertAlmostEqual(dist_indel('Colin', 'Coiln'), 0.2)

    def test_indel_dist_abs(self):
        """Test abydos.distance.Indel.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 3)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 3)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 8)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 4)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 4)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 2)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 2)

        # Test wrapper
        self.assertAlmostEqual(indel('Colin', 'Coiln'), 2)


if __name__ == '__main__':
    unittest.main()
