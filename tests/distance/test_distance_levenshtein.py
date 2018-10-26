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

"""abydos.tests.distance.test_distance_levenshtein.

This module contains unit tests for abydos.distance
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance.levenshtein import (
    damerau_levenshtein,
    dist_damerau,
    dist_indel,
    dist_levenshtein,
    levenshtein,
    sim_damerau,
    sim_indel,
    sim_levenshtein,
)


class LevenshteinTestCases(unittest.TestCase):
    """Test Levenshtein functions.

    abydos.distance.levenshtein.levenshtein, .dist_levenshtein, &
    .sim_levenshtein
    """

    def test_levenshtein(self):
        """Test abydos.distance.levenshtein.levenshtein."""
        self.assertEqual(levenshtein('', ''), 0)

        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('', 'a'), 1)
        self.assertEqual(levenshtein('abc', ''), 3)
        self.assertEqual(levenshtein('', 'abc'), 3)
        self.assertEqual(levenshtein('', ''), 0)
        self.assertEqual(levenshtein('a', 'a'), 0)
        self.assertEqual(levenshtein('abc', 'abc'), 0)
        self.assertEqual(levenshtein('', 'a'), 1)
        self.assertEqual(levenshtein('a', 'ab'), 1)
        self.assertEqual(levenshtein('b', 'ab'), 1)
        self.assertEqual(levenshtein('ac', 'abc'), 1)
        self.assertEqual(levenshtein('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('ab', 'a'), 1)
        self.assertEqual(levenshtein('ab', 'b'), 1)
        self.assertEqual(levenshtein('abc', 'ac'), 1)
        self.assertEqual(levenshtein('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(levenshtein('a', 'b'), 1)
        self.assertEqual(levenshtein('ab', 'ac'), 1)
        self.assertEqual(levenshtein('ac', 'bc'), 1)
        self.assertEqual(levenshtein('abc', 'axc'), 1)
        self.assertEqual(levenshtein('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(levenshtein('example', 'samples'), 3)
        self.assertEqual(levenshtein('sturgeon', 'urgently'), 6)
        self.assertEqual(levenshtein('levenshtein', 'frankenstein'), 6)
        self.assertEqual(levenshtein('distance', 'difference'), 5)
        self.assertEqual(levenshtein('java was neat', 'scala is great'), 7)

        # https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
        self.assertEqual(levenshtein('CA', 'ABC', 'dam'), 2)
        self.assertEqual(levenshtein('CA', 'ABC', 'osa'), 3)

        # test cost of insert
        self.assertEqual(levenshtein('', 'b', 'lev', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('', 'b', 'osa', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('', 'b', 'dam', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('a', 'ab', 'lev', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('a', 'ab', 'osa', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('a', 'ab', 'dam', cost=(5, 7, 10, 10)), 5)

        # test cost of delete
        self.assertEqual(levenshtein('b', '', 'lev', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('b', '', 'osa', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('b', '', 'dam', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('ab', 'a', 'lev', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('ab', 'a', 'osa', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('ab', 'a', 'dam', cost=(5, 7, 10, 10)), 7)

        # test cost of substitute
        self.assertEqual(levenshtein('a', 'b', 'lev', cost=(10, 10, 5, 10)), 5)
        self.assertEqual(levenshtein('a', 'b', 'osa', cost=(10, 10, 5, 10)), 5)
        self.assertEqual(levenshtein('a', 'b', 'dam', cost=(10, 10, 5, 10)), 5)
        self.assertEqual(
            levenshtein('ac', 'bc', 'lev', cost=(10, 10, 5, 10)), 5
        )
        self.assertEqual(
            levenshtein('ac', 'bc', 'osa', cost=(10, 10, 5, 10)), 5
        )
        self.assertEqual(
            levenshtein('ac', 'bc', 'dam', cost=(10, 10, 5, 10)), 5
        )

        # test cost of transpose
        self.assertEqual(
            levenshtein('ab', 'ba', 'lev', cost=(10, 10, 10, 5)), 20
        )
        self.assertEqual(
            levenshtein('ab', 'ba', 'osa', cost=(10, 10, 10, 5)), 5
        )
        self.assertEqual(levenshtein('ab', 'ba', 'dam', cost=(5, 5, 10, 5)), 5)
        self.assertEqual(
            levenshtein('abc', 'bac', 'lev', cost=(10, 10, 10, 5)), 20
        )
        self.assertEqual(
            levenshtein('abc', 'bac', 'osa', cost=(10, 10, 10, 5)), 5
        )
        self.assertEqual(
            levenshtein('abc', 'bac', 'dam', cost=(5, 5, 10, 5)), 5
        )
        self.assertEqual(
            levenshtein('cab', 'cba', 'lev', cost=(10, 10, 10, 5)), 20
        )
        self.assertEqual(
            levenshtein('cab', 'cba', 'osa', cost=(10, 10, 10, 5)), 5
        )
        self.assertEqual(
            levenshtein('cab', 'cba', 'dam', cost=(5, 5, 10, 5)), 5
        )

        # test exception
        self.assertRaises(
            ValueError, levenshtein, 'ab', 'ba', 'dam', cost=(10, 10, 10, 5)
        )

    def test_dist_levenshtein(self):
        """Test abydos.distance.levenshtein.dist_levenshtein."""
        self.assertEqual(dist_levenshtein('', ''), 0)

        self.assertEqual(dist_levenshtein('a', 'a'), 0)
        self.assertEqual(dist_levenshtein('ab', 'ab'), 0)
        self.assertEqual(dist_levenshtein('', 'a'), 1)
        self.assertEqual(dist_levenshtein('', 'ab'), 1)
        self.assertEqual(dist_levenshtein('a', 'c'), 1)

        self.assertAlmostEqual(dist_levenshtein('abc', 'ac'), 1 / 3)
        self.assertAlmostEqual(dist_levenshtein('abbc', 'ac'), 1 / 2)
        self.assertAlmostEqual(dist_levenshtein('abbc', 'abc'), 1 / 4)

    def test_sim_levenshtein(self):
        """Test abydos.distance.levenshtein.sim_levenshtein."""
        self.assertEqual(sim_levenshtein('', ''), 1)

        self.assertEqual(sim_levenshtein('a', 'a'), 1)
        self.assertEqual(sim_levenshtein('ab', 'ab'), 1)
        self.assertEqual(sim_levenshtein('', 'a'), 0)
        self.assertEqual(sim_levenshtein('', 'ab'), 0)
        self.assertEqual(sim_levenshtein('a', 'c'), 0)

        self.assertAlmostEqual(sim_levenshtein('abc', 'ac'), 2 / 3)
        self.assertAlmostEqual(sim_levenshtein('abbc', 'ac'), 1 / 2)
        self.assertAlmostEqual(sim_levenshtein('abbc', 'abc'), 3 / 4)


class DamerauLevenshteinTestCases(unittest.TestCase):
    """Test Damerau-Levenshtein functions.

    abydos.distance.levenshtein.damerau, .dist_damerau, & .sim_damerau
    """

    def test_damerau_levenshtein(self):
        """Test abydos.distance.levenshtein.damerau_levenshtein."""
        self.assertEqual(damerau_levenshtein('', ''), 0)
        self.assertEqual(damerau_levenshtein('CA', 'CA'), 0)
        self.assertEqual(damerau_levenshtein('CA', 'ABC'), 2)
        self.assertEqual(damerau_levenshtein('', 'b', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(
            damerau_levenshtein('a', 'ab', cost=(5, 7, 10, 10)), 5
        )
        self.assertEqual(damerau_levenshtein('b', '', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(
            damerau_levenshtein('ab', 'a', cost=(5, 7, 10, 10)), 7
        )
        self.assertEqual(
            damerau_levenshtein('a', 'b', cost=(10, 10, 5, 10)), 5
        )
        self.assertEqual(
            damerau_levenshtein('ac', 'bc', cost=(10, 10, 5, 10)), 5
        )
        self.assertEqual(
            damerau_levenshtein('ab', 'ba', cost=(5, 5, 10, 5)), 5
        )
        self.assertEqual(
            damerau_levenshtein('abc', 'bac', cost=(5, 5, 10, 5)), 5
        )
        self.assertEqual(
            damerau_levenshtein('cab', 'cba', cost=(5, 5, 10, 5)), 5
        )
        self.assertRaises(
            ValueError, damerau_levenshtein, 'ab', 'ba', cost=(10, 10, 10, 5)
        )

    def test_dist_damerau(self):
        """Test abydos.distance.levenshtein.dist_damerau."""
        self.assertEqual(dist_damerau('', ''), 0)

        self.assertEqual(dist_damerau('a', 'a'), 0)
        self.assertEqual(dist_damerau('ab', 'ab'), 0)
        self.assertEqual(dist_damerau('', 'a'), 1)
        self.assertEqual(dist_damerau('', 'ab'), 1)
        self.assertEqual(dist_damerau('a', 'c'), 1)

        self.assertAlmostEqual(dist_damerau('abc', 'ac'), 1 / 3)
        self.assertAlmostEqual(dist_damerau('abbc', 'ac'), 1 / 2)
        self.assertAlmostEqual(dist_damerau('abbc', 'abc'), 1 / 4)

        self.assertAlmostEqual(dist_damerau('CA', 'ABC'), 2 / 3)
        self.assertAlmostEqual(dist_damerau('', 'b', cost=(5, 7, 10, 10)), 1)
        self.assertAlmostEqual(
            dist_damerau('a', 'ab', cost=(5, 7, 10, 10)), 1 / 2
        )
        self.assertAlmostEqual(dist_damerau('b', '', cost=(5, 7, 10, 10)), 1)
        self.assertAlmostEqual(
            dist_damerau('ab', 'a', cost=(5, 7, 10, 10)), 1 / 2
        )
        self.assertAlmostEqual(
            dist_damerau('a', 'b', cost=(10, 10, 5, 10)), 1 / 2
        )
        self.assertAlmostEqual(
            dist_damerau('ac', 'bc', cost=(10, 10, 5, 10)), 1 / 4
        )
        self.assertAlmostEqual(
            dist_damerau('ab', 'ba', cost=(5, 5, 10, 5)), 1 / 2
        )
        self.assertAlmostEqual(
            dist_damerau('abc', 'bac', cost=(5, 5, 10, 5)), 1 / 3
        )
        self.assertAlmostEqual(
            dist_damerau('cab', 'cba', cost=(5, 5, 10, 5)), 1 / 3
        )
        self.assertRaises(
            ValueError, dist_damerau, 'ab', 'ba', cost=(10, 10, 10, 5)
        )

    def test_sim_damerau(self):
        """Test abydos.distance.levenshtein.sim_damerau."""
        self.assertEqual(sim_damerau('', ''), 1)

        self.assertEqual(sim_damerau('a', 'a'), 1)
        self.assertEqual(sim_damerau('ab', 'ab'), 1)
        self.assertEqual(sim_damerau('', 'a'), 0)
        self.assertEqual(sim_damerau('', 'ab'), 0)
        self.assertEqual(sim_damerau('a', 'c'), 0)

        self.assertAlmostEqual(sim_damerau('abc', 'ac'), 2 / 3)
        self.assertAlmostEqual(sim_damerau('abbc', 'ac'), 1 / 2)
        self.assertAlmostEqual(sim_damerau('abbc', 'abc'), 3 / 4)

        self.assertAlmostEqual(sim_damerau('CA', 'ABC'), 1 / 3)
        self.assertAlmostEqual(sim_damerau('', 'b', cost=(5, 7, 10, 10)), 0)
        self.assertAlmostEqual(
            sim_damerau('a', 'ab', cost=(5, 7, 10, 10)), 1 / 2
        )
        self.assertAlmostEqual(sim_damerau('b', '', cost=(5, 7, 10, 10)), 0)
        self.assertAlmostEqual(
            sim_damerau('ab', 'a', cost=(5, 7, 10, 10)), 1 / 2
        )
        self.assertAlmostEqual(
            sim_damerau('a', 'b', cost=(10, 10, 5, 10)), 1 / 2
        )
        self.assertAlmostEqual(
            sim_damerau('ac', 'bc', cost=(10, 10, 5, 10)), 3 / 4
        )
        self.assertAlmostEqual(
            sim_damerau('ab', 'ba', cost=(5, 5, 10, 5)), 1 / 2
        )
        self.assertAlmostEqual(
            sim_damerau('abc', 'bac', cost=(5, 5, 10, 5)), 2 / 3
        )
        self.assertAlmostEqual(
            sim_damerau('cab', 'cba', cost=(5, 5, 10, 5)), 2 / 3
        )
        self.assertRaises(
            ValueError, sim_damerau, 'ab', 'ba', cost=(10, 10, 10, 5)
        )


class IndelTestCases(unittest.TestCase):
    """Test indel functions.

    abydos.distance.levenshtein.sim_indel & .dist_indel
    """

    def test_sim_indel(self):
        """Test abydos.distance.levenshtein.sim_indel."""
        # Base cases
        self.assertEqual(sim_indel('', ''), 1)
        self.assertEqual(sim_indel('a', ''), 0)
        self.assertEqual(sim_indel('', 'a'), 0)
        self.assertEqual(sim_indel('abc', ''), 0)
        self.assertEqual(sim_indel('', 'abc'), 0)
        self.assertEqual(sim_indel('abcd', 'efgh'), 0)

        self.assertAlmostEqual(sim_indel('Nigel', 'Niall'), 0.6)
        self.assertAlmostEqual(sim_indel('Niall', 'Nigel'), 0.6)
        self.assertAlmostEqual(sim_indel('Colin', 'Coiln'), 0.8)
        self.assertAlmostEqual(sim_indel('Coiln', 'Colin'), 0.8)

    def test_dist_indel(self):
        """Test abydos.distance.levenshtein.dist_indel."""
        # Base cases
        self.assertEqual(dist_indel('', ''), 0)
        self.assertEqual(dist_indel('a', ''), 1)
        self.assertEqual(dist_indel('', 'a'), 1)
        self.assertEqual(dist_indel('abc', ''), 1)
        self.assertEqual(dist_indel('', 'abc'), 1)
        self.assertEqual(dist_indel('abcd', 'efgh'), 1)

        self.assertAlmostEqual(dist_indel('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(dist_indel('Niall', 'Nigel'), 0.4)
        self.assertAlmostEqual(dist_indel('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(dist_indel('Coiln', 'Colin'), 0.2)


if __name__ == '__main__':
    unittest.main()
