# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_sift4.

This module contains unit tests for abydos.distance.Sift4
"""

import unittest

from abydos.distance import Sift4, dist_sift4, sift4_common, sim_sift4


class Sift4TestCases(unittest.TestCase):
    """Test Sift4 functions.

    abydos.distance.Sift4
    """

    cmp = Sift4()
    cmp55 = Sift4(5, 5)

    def test_sift4_dist_abs(self):
        """Test abydos.distance.Sift4.dist_abs."""
        # tests copied from Lukas Benedix's post at
        # https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 3)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 3)

        self.assertEqual(self.cmp.dist_abs('a', 'a'), 0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0)

        self.assertEqual(self.cmp.dist_abs('a', 'ab'), 1)
        self.assertEqual(self.cmp.dist_abs('ac', 'abc'), 1)
        self.assertEqual(self.cmp.dist_abs('abcdefg', 'xabxcdxxefxgx'), 7)

        self.assertEqual(self.cmp.dist_abs('ab', 'b'), 1)
        self.assertEqual(self.cmp.dist_abs('ab', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', 'ac'), 1)
        self.assertEqual(self.cmp.dist_abs('xabxcdxxefxgx', 'abcdefg'), 7)

        self.assertEqual(self.cmp.dist_abs('a', 'b'), 1)
        self.assertEqual(self.cmp.dist_abs('ab', 'ac'), 1)
        self.assertEqual(self.cmp.dist_abs('ac', 'bc'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', 'axc'), 1)
        self.assertEqual(
            self.cmp.dist_abs('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6
        )

        self.assertEqual(self.cmp.dist_abs('example', 'samples'), 2)
        self.assertEqual(self.cmp.dist_abs('sturgeon', 'urgently'), 3)
        self.assertEqual(self.cmp.dist_abs('levenshtein', 'frankenstein'), 6)
        self.assertEqual(self.cmp.dist_abs('distance', 'difference'), 5)

        # Tests copied from
        # https://github.com/tdebatty/java-string-similarity/blob/master/src/test/java/info/debatty/java/stringsimilarity/experimental/Sift4Test.java
        self.assertEqual(
            Sift4(5).dist_abs(
                'This is the first string', 'And this is another string'
            ),
            11,
        )
        self.assertEqual(
            Sift4(10).dist_abs(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'Amet Lorm ispum dolor sit amet, consetetur adixxxpiscing'
                + ' elit.',
            ),
            12,
        )

        # cases with max_distance
        self.assertEqual(self.cmp55.dist_abs('example', 'samples'), 5)
        self.assertEqual(self.cmp55.dist_abs('sturgeon', 'urgently'), 5)
        self.assertEqual(self.cmp55.dist_abs('levenshtein', 'frankenstein'), 5)
        self.assertEqual(self.cmp55.dist_abs('distance', 'difference'), 5)

        # Test wrapper
        self.assertEqual(sift4_common('xabxcdxxefxgx', 'abcdefg'), 7)

    def test_sift4_dist(self):
        """Test abydos.distance.Sift4.dist."""
        # tests copied from Lukas Benedix's post at
        # https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('a', ''), 1)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('abc', ''), 1)
        self.assertEqual(self.cmp.dist('', 'abc'), 1)

        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0)

        self.assertEqual(self.cmp.dist('a', 'ab'), 0.5)
        self.assertEqual(self.cmp.dist('ac', 'abc'), 1 / 3)
        self.assertAlmostEqual(
            self.cmp.dist('abcdefg', 'xabxcdxxefxgx'), 0.538461538
        )

        self.assertEqual(self.cmp.dist('ab', 'b'), 0.5)
        self.assertEqual(self.cmp.dist('ab', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'ac'), 1 / 3)
        self.assertAlmostEqual(
            self.cmp.dist('xabxcdxxefxgx', 'abcdefg'), 0.538461538
        )

        self.assertEqual(self.cmp.dist('a', 'b'), 1)
        self.assertEqual(self.cmp.dist('ab', 'ac'), 0.5)
        self.assertEqual(self.cmp.dist('ac', 'bc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'axc'), 1 / 3)
        self.assertAlmostEqual(
            self.cmp.dist('xabxcdxxefxgx', '1ab2cd34ef5g6'), 0.461538461
        )

        self.assertAlmostEqual(
            self.cmp.dist('example', 'samples'), 0.285714285
        )
        self.assertAlmostEqual(self.cmp.dist('sturgeon', 'urgently'), 0.375)
        self.assertAlmostEqual(
            self.cmp.dist('levenshtein', 'frankenstein'), 0.5
        )
        self.assertAlmostEqual(self.cmp.dist('distance', 'difference'), 0.5)

        # Tests copied from
        # https://github.com/tdebatty/java-string-similarity/blob/master/src/test/java/info/debatty/java/stringsimilarity/experimental/Sift4Test.java
        self.assertAlmostEqual(
            Sift4(5).dist(
                'This is the first string', 'And this is another string'
            ),
            0.423076923,
        )
        self.assertAlmostEqual(
            Sift4(10).dist(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'Amet Lorm ispum dolor sit amet, consetetur adixxxpiscing'
                + ' elit.',
            ),
            0.193548387,
        )

        # cases with max_distance
        self.assertAlmostEqual(
            self.cmp55.dist('example', 'samples'), 0.714285714
        )
        self.assertAlmostEqual(self.cmp55.dist('sturgeon', 'urgently'), 0.625)
        self.assertAlmostEqual(
            self.cmp55.dist('levenshtein', 'frankenstein'), 0.416666666
        )
        self.assertAlmostEqual(self.cmp55.dist('distance', 'difference'), 0.5)

        # Test wrapper
        self.assertAlmostEqual(
            dist_sift4('xabxcdxxefxgx', 'abcdefg'), 0.538461538
        )

    def test_sift4_sim(self):
        """Test abydos.distance.Sift4.sim."""
        # tests copied from Lukas Benedix's post at
        # https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('a', ''), 0)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('abc', ''), 0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0)

        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1)

        self.assertEqual(self.cmp.sim('a', 'ab'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('ac', 'abc'), 2 / 3)
        self.assertAlmostEqual(
            self.cmp.sim('abcdefg', 'xabxcdxxefxgx'), 0.461538461
        )

        self.assertEqual(self.cmp.sim('ab', 'b'), 0.5)
        self.assertEqual(self.cmp.sim('ab', 'a'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('abc', 'ac'), 2 / 3)
        self.assertAlmostEqual(
            self.cmp.sim('xabxcdxxefxgx', 'abcdefg'), 0.461538461
        )

        self.assertEqual(self.cmp.sim('a', 'b'), 0)
        self.assertEqual(self.cmp.sim('ab', 'ac'), 0.5)
        self.assertEqual(self.cmp.sim('ac', 'bc'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('abc', 'axc'), 2 / 3)
        self.assertAlmostEqual(
            self.cmp.sim('xabxcdxxefxgx', '1ab2cd34ef5g6'), 0.538461538
        )

        self.assertAlmostEqual(self.cmp.sim('example', 'samples'), 0.714285714)
        self.assertAlmostEqual(self.cmp.sim('sturgeon', 'urgently'), 0.625)
        self.assertAlmostEqual(
            self.cmp.sim('levenshtein', 'frankenstein'), 0.5
        )
        self.assertAlmostEqual(self.cmp.sim('distance', 'difference'), 0.5)

        # Tests copied from
        # https://github.com/tdebatty/java-string-similarity/blob/master/src/test/java/info/debatty/java/stringsimilarity/experimental/Sift4Test.java
        self.assertAlmostEqual(
            Sift4(5).sim(
                'This is the first string', 'And this is another string'
            ),
            0.576923077,
        )
        self.assertAlmostEqual(
            Sift4(10).sim(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'Amet Lorm ispum dolor sit amet, consetetur adixxxpiscing'
                + ' elit.',
            ),
            0.806451613,
        )

        # cases with max_distance
        self.assertAlmostEqual(
            self.cmp55.sim('example', 'samples'), 0.285714286
        )
        self.assertAlmostEqual(self.cmp55.sim('sturgeon', 'urgently'), 0.375)
        self.assertAlmostEqual(
            self.cmp55.sim('levenshtein', 'frankenstein'), 0.583333333
        )
        self.assertAlmostEqual(self.cmp55.sim('distance', 'difference'), 0.5)

        # Test wrapper
        self.assertAlmostEqual(
            sim_sift4('xabxcdxxefxgx', 'abcdefg'), 0.461538461
        )


if __name__ == '__main__':
    unittest.main()
