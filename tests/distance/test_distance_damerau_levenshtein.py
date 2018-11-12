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

"""abydos.tests.distance.test_distance_damerau_levenshtein.

This module contains unit tests for abydos.distance.DamerauLevenshtein
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import (
    DamerauLevenshtein,
    damerau_levenshtein,
    dist_damerau,
    sim_damerau,
)


class DamerauLevenshteinTestCases(unittest.TestCase):
    """Test Damerau-Levenshtein functions.

    abydos.distance.DamerauLevenshtein
    """
    cmp = DamerauLevenshtein()

    def test_damerau_levenshtein_dist_abs(self):
        """Test abydos.distance.DamerauLevenshtein.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('CA', 'CA'), 0)
        self.assertEqual(self.cmp.dist_abs('CA', 'ABC'), 2)
        self.assertEqual(self.cmp.dist_abs('', 'b', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(
            self.cmp.dist_abs('a', 'ab', cost=(5, 7, 10, 10)), 5
        )
        self.assertEqual(self.cmp.dist_abs('b', '', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(
            self.cmp.dist_abs('ab', 'a', cost=(5, 7, 10, 10)), 7
        )
        self.assertEqual(
            self.cmp.dist_abs('a', 'b', cost=(10, 10, 5, 10)), 5
        )
        self.assertEqual(
            self.cmp.dist_abs('ac', 'bc', cost=(10, 10, 5, 10)), 5
        )
        self.assertEqual(
            self.cmp.dist_abs('ab', 'ba', cost=(5, 5, 10, 5)), 5
        )
        self.assertEqual(
            self.cmp.dist_abs('abc', 'bac', cost=(5, 5, 10, 5)), 5
        )
        self.assertEqual(
            self.cmp.dist_abs('cab', 'cba', cost=(5, 5, 10, 5)), 5
        )
        self.assertRaises(
            ValueError, self.cmp.dist_abs, 'ab', 'ba', cost=(10, 10, 10, 5)
        )

        # Test wrapper
        self.assertEqual(damerau_levenshtein('CA', 'ABC'), 2)

    def test_damerau_dist(self):
        """Test abydos.distance.DamerauLevenshtein.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)

        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('ab', 'ab'), 0)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('', 'ab'), 1)
        self.assertEqual(self.cmp.dist('a', 'c'), 1)

        self.assertAlmostEqual(self.cmp.dist('abc', 'ac'), 1 / 3)
        self.assertAlmostEqual(self.cmp.dist('abbc', 'ac'), 1 / 2)
        self.assertAlmostEqual(self.cmp.dist('abbc', 'abc'), 1 / 4)

        self.assertAlmostEqual(self.cmp.dist('CA', 'ABC'), 2 / 3)
        self.assertAlmostEqual(self.cmp.dist('', 'b', cost=(5, 7, 10, 10)), 1)
        self.assertAlmostEqual(
            self.cmp.dist('a', 'ab', cost=(5, 7, 10, 10)), 1 / 2
        )
        self.assertAlmostEqual(self.cmp.dist('b', '', cost=(5, 7, 10, 10)), 1)
        self.assertAlmostEqual(
            self.cmp.dist('ab', 'a', cost=(5, 7, 10, 10)), 1 / 2
        )
        self.assertAlmostEqual(
            self.cmp.dist('a', 'b', cost=(10, 10, 5, 10)), 1 / 2
        )
        self.assertAlmostEqual(
            self.cmp.dist('ac', 'bc', cost=(10, 10, 5, 10)), 1 / 4
        )
        self.assertAlmostEqual(
            self.cmp.dist('ab', 'ba', cost=(5, 5, 10, 5)), 1 / 2
        )
        self.assertAlmostEqual(
            self.cmp.dist('abc', 'bac', cost=(5, 5, 10, 5)), 1 / 3
        )
        self.assertAlmostEqual(
            self.cmp.dist('cab', 'cba', cost=(5, 5, 10, 5)), 1 / 3
        )
        self.assertRaises(
            ValueError, self.cmp.dist, 'ab', 'ba', cost=(10, 10, 10, 5)
        )

        # Test wrapper
        self.assertAlmostEqual(dist_damerau('abbc', 'abc'), 1 / 4)

    def test_damerau_sim(self):
        """Test abydos.distance.DamerauLevenshtein.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)

        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('ab', 'ab'), 1)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('', 'ab'), 0)
        self.assertEqual(self.cmp.sim('a', 'c'), 0)

        self.assertAlmostEqual(self.cmp.sim('abc', 'ac'), 2 / 3)
        self.assertAlmostEqual(self.cmp.sim('abbc', 'ac'), 1 / 2)
        self.assertAlmostEqual(self.cmp.sim('abbc', 'abc'), 3 / 4)

        self.assertAlmostEqual(self.cmp.sim('CA', 'ABC'), 1 / 3)
        self.assertAlmostEqual(self.cmp.sim('', 'b', cost=(5, 7, 10, 10)), 0)
        self.assertAlmostEqual(
            self.cmp.sim('a', 'ab', cost=(5, 7, 10, 10)), 1 / 2
        )
        self.assertAlmostEqual(self.cmp.sim('b', '', cost=(5, 7, 10, 10)), 0)
        self.assertAlmostEqual(
            self.cmp.sim('ab', 'a', cost=(5, 7, 10, 10)), 1 / 2
        )
        self.assertAlmostEqual(
            self.cmp.sim('a', 'b', cost=(10, 10, 5, 10)), 1 / 2
        )
        self.assertAlmostEqual(
            self.cmp.sim('ac', 'bc', cost=(10, 10, 5, 10)), 3 / 4
        )
        self.assertAlmostEqual(
            self.cmp.sim('ab', 'ba', cost=(5, 5, 10, 5)), 1 / 2
        )
        self.assertAlmostEqual(
            self.cmp.sim('abc', 'bac', cost=(5, 5, 10, 5)), 2 / 3
        )
        self.assertAlmostEqual(
            self.cmp.sim('cab', 'cba', cost=(5, 5, 10, 5)), 2 / 3
        )
        self.assertRaises(
            ValueError, self.cmp.sim, 'ab', 'ba', cost=(10, 10, 10, 5)
        )

        # Test wrapper
        self.assertAlmostEqual(sim_damerau('abbc', 'abc'), 3 / 4)


if __name__ == '__main__':
    unittest.main()
