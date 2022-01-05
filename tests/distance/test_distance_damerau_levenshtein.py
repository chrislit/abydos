# Copyright 2014-2022 by Christopher C. Little.
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

import unittest

from abydos.distance import DamerauLevenshtein


class DamerauLevenshteinTestCases(unittest.TestCase):
    """Test Damerau-Levenshtein functions.

    abydos.distance.DamerauLevenshtein
    """

    cmp = DamerauLevenshtein()
    cmp571010 = DamerauLevenshtein(cost=(5, 7, 10, 10))
    cmp1010510 = DamerauLevenshtein(cost=(10, 10, 5, 10))
    cmp55105 = DamerauLevenshtein(cost=(5, 5, 10, 5))
    cmp1010105 = DamerauLevenshtein(cost=(10, 10, 10, 5))

    def test_damerau_levenshtein_dist_abs(self):
        """Test abydos.distance.DamerauLevenshtein.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('CA', 'CA'), 0)
        self.assertEqual(self.cmp.dist_abs('CA', 'ABC'), 2)
        self.assertEqual(self.cmp571010.dist_abs('', 'b'), 5)
        self.assertEqual(self.cmp571010.dist_abs('a', 'ab'), 5)
        self.assertEqual(self.cmp571010.dist_abs('b', ''), 7)
        self.assertEqual(self.cmp571010.dist_abs('ab', 'a'), 7)
        self.assertEqual(self.cmp1010510.dist_abs('a', 'b'), 5)
        self.assertEqual(self.cmp1010510.dist_abs('ac', 'bc'), 5)
        self.assertEqual(self.cmp55105.dist_abs('ab', 'ba'), 5)
        self.assertEqual(self.cmp55105.dist_abs('abc', 'bac'), 5)
        self.assertEqual(self.cmp55105.dist_abs('cab', 'cba'), 5)
        self.assertRaises(ValueError, self.cmp1010105.dist_abs, 'ab', 'ba')

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
        self.assertAlmostEqual(self.cmp571010.dist('', 'b'), 1)
        self.assertAlmostEqual(self.cmp571010.dist('a', 'ab'), 1 / 2)
        self.assertAlmostEqual(self.cmp571010.dist('b', ''), 1)
        self.assertAlmostEqual(self.cmp571010.dist('ab', 'a'), 1 / 2)
        self.assertAlmostEqual(self.cmp1010510.dist('a', 'b'), 1 / 2)
        self.assertAlmostEqual(self.cmp1010510.dist('ac', 'bc'), 1 / 4)
        self.assertAlmostEqual(self.cmp55105.dist('ab', 'ba'), 1 / 2)
        self.assertAlmostEqual(self.cmp55105.dist('abc', 'bac'), 1 / 3)
        self.assertAlmostEqual(self.cmp55105.dist('cab', 'cba'), 1 / 3)
        self.assertRaises(ValueError, self.cmp1010105.dist, 'ab', 'ba')

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
        self.assertAlmostEqual(self.cmp571010.sim('', 'b'), 0)
        self.assertAlmostEqual(self.cmp571010.sim('a', 'ab'), 1 / 2)
        self.assertAlmostEqual(self.cmp571010.sim('b', ''), 0)
        self.assertAlmostEqual(self.cmp571010.sim('ab', 'a'), 1 / 2)
        self.assertAlmostEqual(self.cmp1010510.sim('a', 'b'), 1 / 2)
        self.assertAlmostEqual(self.cmp1010510.sim('ac', 'bc'), 3 / 4)
        self.assertAlmostEqual(self.cmp55105.sim('ab', 'ba'), 1 / 2)
        self.assertAlmostEqual(self.cmp55105.sim('abc', 'bac'), 2 / 3)
        self.assertAlmostEqual(self.cmp55105.sim('cab', 'cba'), 2 / 3)
        self.assertRaises(ValueError, self.cmp1010105.sim, 'ab', 'ba')


if __name__ == '__main__':
    unittest.main()
