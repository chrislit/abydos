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

This module contains unit tests for abydos.distance.Levenshtein
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import (
    Levenshtein,
    dist_levenshtein,
    levenshtein,
    sim_levenshtein,
)


class LevenshteinTestCases(unittest.TestCase):
    """Test Levenshtein functions.

    abydos.distance.Levenshtein
    """

    cmp = Levenshtein()
    cmp_taper = Levenshtein(taper=True)

    def test_levenshtein_dist_abs(self):
        """Test abydos.distance.Levenshtein.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)

        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEqual(self.cmp.dist_abs('a', ''), 1)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 3)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 3)
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', 'a'), 0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('a', 'ab'), 1)
        self.assertEqual(self.cmp.dist_abs('b', 'ab'), 1)
        self.assertEqual(self.cmp.dist_abs('ac', 'abc'), 1)
        self.assertEqual(self.cmp.dist_abs('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1)
        self.assertEqual(self.cmp.dist_abs('ab', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('ab', 'b'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', 'ac'), 1)
        self.assertEqual(self.cmp.dist_abs('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(self.cmp.dist_abs('a', 'b'), 1)
        self.assertEqual(self.cmp.dist_abs('ab', 'ac'), 1)
        self.assertEqual(self.cmp.dist_abs('ac', 'bc'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', 'axc'), 1)
        self.assertEqual(
            self.cmp.dist_abs('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6
        )
        self.assertEqual(self.cmp.dist_abs('example', 'samples'), 3)
        self.assertEqual(self.cmp.dist_abs('sturgeon', 'urgently'), 6)
        self.assertEqual(self.cmp.dist_abs('levenshtein', 'frankenstein'), 6)
        self.assertEqual(self.cmp.dist_abs('distance', 'difference'), 5)
        self.assertEqual(
            self.cmp.dist_abs('java was neat', 'scala is great'), 7
        )

        # https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
        self.assertEqual(Levenshtein(mode='osa').dist_abs('CA', 'ABC'), 3)

        # test cost of insert
        self.assertEqual(
            Levenshtein(mode='lev', cost=(5, 7, 10, 10)).dist_abs('', 'b'), 5
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(5, 7, 10, 10)).dist_abs('', 'b'), 5
        )
        self.assertEqual(
            Levenshtein(mode='lev', cost=(5, 7, 10, 10)).dist_abs('a', 'ab'), 5
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(5, 7, 10, 10)).dist_abs('a', 'ab'), 5
        )

        # test cost of delete
        self.assertEqual(
            Levenshtein(mode='lev', cost=(5, 7, 10, 10)).dist_abs('b', ''), 7
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(5, 7, 10, 10)).dist_abs('b', ''), 7
        )
        self.assertEqual(
            Levenshtein(mode='lev', cost=(5, 7, 10, 10)).dist_abs('ab', 'a'), 7
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(5, 7, 10, 10)).dist_abs('ab', 'a'), 7
        )

        # test cost of substitute
        self.assertEqual(
            Levenshtein(mode='lev', cost=(10, 10, 5, 10)).dist_abs('a', 'b'), 5
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(10, 10, 5, 10)).dist_abs('a', 'b'), 5
        )
        self.assertEqual(
            Levenshtein(mode='lev', cost=(10, 10, 5, 10)).dist_abs('ac', 'bc'),
            5,
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(10, 10, 5, 10)).dist_abs('ac', 'bc'),
            5,
        )

        # test cost of transpose
        self.assertEqual(
            Levenshtein(mode='lev', cost=(10, 10, 10, 5)).dist_abs('ab', 'ba'),
            20,
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(10, 10, 10, 5)).dist_abs('ab', 'ba'),
            5,
        )
        self.assertEqual(
            Levenshtein(mode='lev', cost=(10, 10, 10, 5)).dist_abs(
                'abc', 'bac'
            ),
            20,
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(10, 10, 10, 5)).dist_abs(
                'abc', 'bac'
            ),
            5,
        )
        self.assertEqual(
            Levenshtein(mode='lev', cost=(10, 10, 10, 5)).dist_abs(
                'cab', 'cba'
            ),
            20,
        )
        self.assertEqual(
            Levenshtein(mode='osa', cost=(10, 10, 10, 5)).dist_abs(
                'cab', 'cba'
            ),
            5,
        )

        # tapered variant
        self.assertAlmostEqual(
            self.cmp_taper.dist_abs('abc', 'ac'), 1.33333333333
        )
        self.assertAlmostEqual(
            self.cmp_taper.dist_abs('xabxcdxxefxgx', 'abcdefg'),
            8.615384615384617,
        )
        self.assertAlmostEqual(
            self.cmp_taper.dist_abs('levenshtein', 'frankenstein'), 10
        )
        self.assertAlmostEqual(
            self.cmp_taper.dist_abs('distance', 'difference'),
            7.499999999999999,
        )

        # Test wrapper
        self.assertEqual(
            levenshtein('ab', 'ba', 'lev', cost=(10, 10, 10, 5)), 20
        )
        self.assertEqual(
            levenshtein('ab', 'ba', 'osa', cost=(10, 10, 10, 5)), 5
        )

    def test_levenshtein_dist(self):
        """Test abydos.distance.Levenshtein.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)

        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('ab', 'ab'), 0)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('', 'ab'), 1)
        self.assertEqual(self.cmp.dist('a', 'c'), 1)

        self.assertAlmostEqual(self.cmp.dist('abc', 'ac'), 1 / 3)
        self.assertAlmostEqual(self.cmp.dist('abbc', 'ac'), 1 / 2)
        self.assertAlmostEqual(self.cmp.dist('abbc', 'abc'), 1 / 4)

        # tapered variant
        self.assertAlmostEqual(
            self.cmp_taper.dist('abc', 'ac'), 0.2666666666666666
        )
        self.assertAlmostEqual(
            self.cmp_taper.dist('abbc', 'ac'), 0.4230769230769231
        )
        self.assertAlmostEqual(
            self.cmp_taper.dist('abbc', 'abc'), 0.19230769230769232
        )

        # Test wrapper
        self.assertAlmostEqual(dist_levenshtein('abbc', 'abc'), 1 / 4)

    def test_levenshtein_sim(self):
        """Test abydos.distance.Levenshtein.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)

        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('ab', 'ab'), 1)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('', 'ab'), 0)
        self.assertEqual(self.cmp.sim('a', 'c'), 0)

        self.assertAlmostEqual(self.cmp.sim('abc', 'ac'), 2 / 3)
        self.assertAlmostEqual(self.cmp.sim('abbc', 'ac'), 1 / 2)
        self.assertAlmostEqual(self.cmp.sim('abbc', 'abc'), 3 / 4)

        # Test wrapper
        self.assertAlmostEqual(sim_levenshtein('abbc', 'abc'), 3 / 4)


if __name__ == '__main__':
    unittest.main()
