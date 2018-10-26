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

This module contains unit tests for abydos.distance._sift4
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance import (
    dist_sift4,
    sift4_common,
    sift4_simplest,
    sim_sift4,
)


class Sift4TestCases(unittest.TestCase):
    """Test Sift4 functions.

    abydos.distance._sift4.sift4_simplest, sift4_common, sim_sift4, & sim_sift4
    """

    def test_sift4_simplest(self):
        """Test abydos.distance._sift4.sift4_simplest."""
        # tests copied from Lukas Benedix's post at
        # https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
        self.assertEqual(sift4_simplest('', ''), 0)
        self.assertEqual(sift4_simplest('a', ''), 1)
        self.assertEqual(sift4_simplest('', 'a'), 1)
        self.assertEqual(sift4_simplest('abc', ''), 3)
        self.assertEqual(sift4_simplest('', 'abc'), 3)

        self.assertEqual(sift4_simplest('a', 'a'), 0)
        self.assertEqual(sift4_simplest('abc', 'abc'), 0)

        self.assertEqual(sift4_simplest('a', 'ab'), 1)
        self.assertEqual(sift4_simplest('ac', 'abc'), 1)
        self.assertEqual(sift4_simplest('abcdefg', 'xabxcdxxefxgx'), 10)

        self.assertEqual(sift4_simplest('ab', 'b'), 1)
        self.assertEqual(sift4_simplest('ab', 'a'), 1)
        self.assertEqual(sift4_simplest('abc', 'ac'), 1)
        self.assertEqual(sift4_simplest('xabxcdxxefxgx', 'abcdefg'), 10)

        self.assertEqual(sift4_simplest('a', 'b'), 1)
        self.assertEqual(sift4_simplest('ab', 'ac'), 1)
        self.assertEqual(sift4_simplest('ac', 'bc'), 1)
        self.assertEqual(sift4_simplest('abc', 'axc'), 1)
        self.assertEqual(sift4_simplest('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)

        self.assertEqual(sift4_simplest('example', 'samples'), 2)
        self.assertEqual(sift4_simplest('sturgeon', 'urgently'), 4)
        self.assertEqual(sift4_simplest('levenshtein', 'frankenstein'), 10)
        self.assertEqual(sift4_simplest('distance', 'difference'), 7)

        # Tests copied from
        # https://github.com/tdebatty/java-string-similarity/blob/master/src/test/java/info/debatty/java/stringsimilarity/experimental/Sift4Test.java
        self.assertEqual(
            sift4_simplest(
                'This is the first string', 'And this is another string', 5
            ),
            13,
        )
        self.assertEqual(
            sift4_simplest(
                'Lorem ipsum dolor sit amet, '
                + 'consectetur adipiscing elit.',
                'Amet Lorm ispum dolor sit amet, '
                + 'consetetur adixxxpiscing elit.',
                10,
            ),
            20,
        )

    def test_sift4_common(self):
        """Test abydos.distance._sift4.sift4_common."""
        # tests copied from Lukas Benedix's post at
        # https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
        self.assertEqual(sift4_common('', ''), 0)
        self.assertEqual(sift4_common('a', ''), 1)
        self.assertEqual(sift4_common('', 'a'), 1)
        self.assertEqual(sift4_common('abc', ''), 3)
        self.assertEqual(sift4_common('', 'abc'), 3)

        self.assertEqual(sift4_common('a', 'a'), 0)
        self.assertEqual(sift4_common('abc', 'abc'), 0)

        self.assertEqual(sift4_common('a', 'ab'), 1)
        self.assertEqual(sift4_common('ac', 'abc'), 1)
        self.assertEqual(sift4_common('abcdefg', 'xabxcdxxefxgx'), 7)

        self.assertEqual(sift4_common('ab', 'b'), 1)
        self.assertEqual(sift4_common('ab', 'a'), 1)
        self.assertEqual(sift4_common('abc', 'ac'), 1)
        self.assertEqual(sift4_common('xabxcdxxefxgx', 'abcdefg'), 7)

        self.assertEqual(sift4_common('a', 'b'), 1)
        self.assertEqual(sift4_common('ab', 'ac'), 1)
        self.assertEqual(sift4_common('ac', 'bc'), 1)
        self.assertEqual(sift4_common('abc', 'axc'), 1)
        self.assertEqual(sift4_common('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)

        self.assertEqual(sift4_common('example', 'samples'), 2)
        self.assertEqual(sift4_common('sturgeon', 'urgently'), 3)
        self.assertEqual(sift4_common('levenshtein', 'frankenstein'), 6)
        self.assertEqual(sift4_common('distance', 'difference'), 5)

        # Tests copied from
        # https://github.com/tdebatty/java-string-similarity/blob/master/src/test/java/info/debatty/java/stringsimilarity/experimental/Sift4Test.java
        self.assertEqual(
            sift4_common(
                'This is the first string', 'And this is another string', 5
            ),
            11,
        )
        self.assertEqual(
            sift4_common(
                'Lorem ipsum dolor sit amet, '
                + 'consectetur adipiscing elit.',
                'Amet Lorm ispum dolor sit amet, '
                + 'consetetur adixxxpiscing elit.',
                10,
            ),
            12,
        )

        # cases with max_distance
        self.assertEqual(sift4_common('example', 'samples', 5, 5), 5)
        self.assertEqual(sift4_common('sturgeon', 'urgently', 5, 5), 5)
        self.assertEqual(sift4_common('levenshtein', 'frankenstein', 5, 5), 5)
        self.assertEqual(sift4_common('distance', 'difference', 5, 5), 5)

    def test_dist_sift4(self):
        """Test abydos.distance._sift4.dist_sift4."""
        # tests copied from Lukas Benedix's post at
        # https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
        self.assertEqual(dist_sift4('', ''), 0)
        self.assertEqual(dist_sift4('a', ''), 1)
        self.assertEqual(dist_sift4('', 'a'), 1)
        self.assertEqual(dist_sift4('abc', ''), 1)
        self.assertEqual(dist_sift4('', 'abc'), 1)

        self.assertEqual(dist_sift4('a', 'a'), 0)
        self.assertEqual(dist_sift4('abc', 'abc'), 0)

        self.assertEqual(dist_sift4('a', 'ab'), 0.5)
        self.assertEqual(dist_sift4('ac', 'abc'), 1 / 3)
        self.assertAlmostEqual(
            dist_sift4('abcdefg', 'xabxcdxxefxgx'), 0.538461538
        )

        self.assertEqual(dist_sift4('ab', 'b'), 0.5)
        self.assertEqual(dist_sift4('ab', 'a'), 0.5)
        self.assertEqual(dist_sift4('abc', 'ac'), 1 / 3)
        self.assertAlmostEqual(
            dist_sift4('xabxcdxxefxgx', 'abcdefg'), 0.538461538
        )

        self.assertEqual(dist_sift4('a', 'b'), 1)
        self.assertEqual(dist_sift4('ab', 'ac'), 0.5)
        self.assertEqual(dist_sift4('ac', 'bc'), 0.5)
        self.assertEqual(dist_sift4('abc', 'axc'), 1 / 3)
        self.assertAlmostEqual(
            dist_sift4('xabxcdxxefxgx', '1ab2cd34ef5g6'), 0.461538461
        )

        self.assertAlmostEqual(dist_sift4('example', 'samples'), 0.285714285)
        self.assertAlmostEqual(dist_sift4('sturgeon', 'urgently'), 0.375)
        self.assertAlmostEqual(dist_sift4('levenshtein', 'frankenstein'), 0.5)
        self.assertAlmostEqual(dist_sift4('distance', 'difference'), 0.5)

        # Tests copied from
        # https://github.com/tdebatty/java-string-similarity/blob/master/src/test/java/info/debatty/java/stringsimilarity/experimental/Sift4Test.java
        self.assertAlmostEqual(
            dist_sift4(
                'This is the first string', 'And this is another string', 5
            ),
            0.423076923,
        )
        self.assertAlmostEqual(
            dist_sift4(
                'Lorem ipsum dolor sit amet, '
                + 'consectetur adipiscing elit.',
                'Amet Lorm ispum dolor sit amet, '
                + 'consetetur adixxxpiscing elit.',
                10,
            ),
            0.193548387,
        )

        # cases with max_distance
        self.assertAlmostEqual(
            dist_sift4('example', 'samples', 5, 5), 0.714285714
        )
        self.assertAlmostEqual(dist_sift4('sturgeon', 'urgently', 5, 5), 0.625)
        self.assertAlmostEqual(
            dist_sift4('levenshtein', 'frankenstein', 5, 5), 0.416666666
        )
        self.assertAlmostEqual(dist_sift4('distance', 'difference', 5, 5), 0.5)

    def test_sim_sift4(self):
        """Test abydos.distance._sift4.sim_sift4."""
        # tests copied from Lukas Benedix's post at
        # https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
        self.assertEqual(sim_sift4('', ''), 1)
        self.assertEqual(sim_sift4('a', ''), 0)
        self.assertEqual(sim_sift4('', 'a'), 0)
        self.assertEqual(sim_sift4('abc', ''), 0)
        self.assertEqual(sim_sift4('', 'abc'), 0)

        self.assertEqual(sim_sift4('a', 'a'), 1)
        self.assertEqual(sim_sift4('abc', 'abc'), 1)

        self.assertEqual(sim_sift4('a', 'ab'), 0.5)
        self.assertAlmostEqual(sim_sift4('ac', 'abc'), 2 / 3)
        self.assertAlmostEqual(
            sim_sift4('abcdefg', 'xabxcdxxefxgx'), 0.461538461
        )

        self.assertEqual(sim_sift4('ab', 'b'), 0.5)
        self.assertEqual(sim_sift4('ab', 'a'), 0.5)
        self.assertAlmostEqual(sim_sift4('abc', 'ac'), 2 / 3)
        self.assertAlmostEqual(
            sim_sift4('xabxcdxxefxgx', 'abcdefg'), 0.461538461
        )

        self.assertEqual(sim_sift4('a', 'b'), 0)
        self.assertEqual(sim_sift4('ab', 'ac'), 0.5)
        self.assertEqual(sim_sift4('ac', 'bc'), 0.5)
        self.assertAlmostEqual(sim_sift4('abc', 'axc'), 2 / 3)
        self.assertAlmostEqual(
            sim_sift4('xabxcdxxefxgx', '1ab2cd34ef5g6'), 0.538461538
        )

        self.assertAlmostEqual(sim_sift4('example', 'samples'), 0.714285714)
        self.assertAlmostEqual(sim_sift4('sturgeon', 'urgently'), 0.625)
        self.assertAlmostEqual(sim_sift4('levenshtein', 'frankenstein'), 0.5)
        self.assertAlmostEqual(sim_sift4('distance', 'difference'), 0.5)

        # Tests copied from
        # https://github.com/tdebatty/java-string-similarity/blob/master/src/test/java/info/debatty/java/stringsimilarity/experimental/Sift4Test.java
        self.assertAlmostEqual(
            sim_sift4(
                'This is the first string', 'And this is another string', 5
            ),
            0.576923077,
        )
        self.assertAlmostEqual(
            sim_sift4(
                'Lorem ipsum dolor sit amet, '
                + 'consectetur adipiscing elit.',
                'Amet Lorm ispum dolor sit amet, '
                + 'consetetur adixxxpiscing elit.',
                10,
            ),
            0.806451613,
        )

        # cases with max_distance
        self.assertAlmostEqual(
            sim_sift4('example', 'samples', 5, 5), 0.285714286
        )
        self.assertAlmostEqual(sim_sift4('sturgeon', 'urgently', 5, 5), 0.375)
        self.assertAlmostEqual(
            sim_sift4('levenshtein', 'frankenstein', 5, 5), 0.583333333
        )
        self.assertAlmostEqual(sim_sift4('distance', 'difference', 5, 5), 0.5)


if __name__ == '__main__':
    unittest.main()
