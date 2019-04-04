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

"""abydos.tests.distance.test_distance_tichy.

This module contains unit tests for abydos.distance.Tichy
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Tichy


class TichyTestCases(unittest.TestCase):
    """Test Tichy functions.

    abydos.distance.Tichy
    """

    cmp = Tichy()

    def test_tichy_dist(self):
        """Test abydos.distance.Tichy.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.8)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.8)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.8)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.8)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4444444444
        )

    def test_tichy_sim(self):
        """Test abydos.distance.Tichy.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.2)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.2)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.2)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5555555556
        )

    def test_tichy_dist_abs(self):
        """Test abydos.distance.Tichy.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 3)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 4)

        self.assertEqual(self.cmp.dist_abs('Nigel', 'Niall'), 4)
        self.assertEqual(self.cmp.dist_abs('Niall', 'Nigel'), 4)
        self.assertEqual(self.cmp.dist_abs('Colin', 'Coiln'), 4)
        self.assertEqual(self.cmp.dist_abs('Coiln', 'Colin'), 4)
        self.assertEqual(self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 4)

        # Examples from paper

        self.assertEqual(self.cmp.dist_abs('abda', 'abcab'), 3)
        self.assertEqual(self.cmp.dist_abs('shanghai', 'sakhalin'), 7)
        self.assertEqual(self.cmp.dist_abs('abcde', 'deabc'), 2)
        self.assertEqual(self.cmp.dist_abs('abc', 'abcabc'), 2)
        self.assertEqual(self.cmp.dist_abs('abcdea', 'cdab'), 2)
        self.assertEqual(self.cmp.dist_abs('abcdefdeab', 'cdeabc'), 2)


if __name__ == '__main__':
    unittest.main()
