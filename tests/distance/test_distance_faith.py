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

"""abydos.tests.distance.test_distance_faith.

This module contains unit tests for abydos.distance.Faith
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Faith


class FaithTestCases(unittest.TestCase):
    """Test Faith functions.

    abydos.distance.Faith
    """

    cmp = Faith()
    cmp_no_d = Faith(alphabet=0)

    def test_faith_sim(self):
        """Test abydos.distance.Faith.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5)
        self.assertEqual(self.cmp.sim('a', ''), 0.4987244897959184)
        self.assertEqual(self.cmp.sim('', 'a'), 0.4987244897959184)
        self.assertEqual(self.cmp.sim('abc', ''), 0.49744897959183676)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.49744897959183676)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 4.497448979591836)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.49362244897959184)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 3.4942602041)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 3.4942602041)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 3.4942602041)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 3.4942602041)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 7.4910714286
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 4.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 3.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 3.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 3.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 3.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 7.0
        )

    def test_faith_dist(self):
        """Test abydos.distance.Faith.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.5)
        self.assertEqual(self.cmp.dist('a', ''), 0.5012755102040816)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5012755102040816)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5025510204081632)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5025510204081632)
        self.assertEqual(self.cmp.dist('abc', 'abc'), -3.4974489795918364)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5063775510204082)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), -2.4942602041)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), -2.4942602041)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), -2.4942602041)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), -2.4942602041)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), -6.4910714286
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), -3.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), -2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), -2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), -2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), -2.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), -6.0
        )


if __name__ == '__main__':
    unittest.main()
