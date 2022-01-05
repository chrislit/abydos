# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_sift4_simplest.

This module contains unit tests for abydos.distance.Sift4Simplest
"""

import unittest

from abydos.distance import Sift4Simplest


class Sift4TestCases(unittest.TestCase):
    """Test Sift4Simplest functions.

    abydos.distance.Sift4Simplest
    """

    cmp = Sift4Simplest()

    def test_sift4_simplest_dist_abs(self):
        """Test abydos.distance.Sift4Simplest.dist_abs."""
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
        self.assertEqual(self.cmp.dist_abs('abcdefg', 'xabxcdxxefxgx'), 10)

        self.assertEqual(self.cmp.dist_abs('ab', 'b'), 1)
        self.assertEqual(self.cmp.dist_abs('ab', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', 'ac'), 1)
        self.assertEqual(self.cmp.dist_abs('xabxcdxxefxgx', 'abcdefg'), 10)

        self.assertEqual(self.cmp.dist_abs('a', 'b'), 1)
        self.assertEqual(self.cmp.dist_abs('ab', 'ac'), 1)
        self.assertEqual(self.cmp.dist_abs('ac', 'bc'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', 'axc'), 1)
        self.assertEqual(
            self.cmp.dist_abs('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6
        )

        self.assertEqual(self.cmp.dist_abs('example', 'samples'), 2)
        self.assertEqual(self.cmp.dist_abs('sturgeon', 'urgently'), 4)
        self.assertEqual(self.cmp.dist_abs('levenshtein', 'frankenstein'), 10)
        self.assertEqual(self.cmp.dist_abs('distance', 'difference'), 7)

        # Tests copied from
        # https://github.com/tdebatty/java-string-similarity/blob/master/src/test/java/info/debatty/java/stringsimilarity/experimental/Sift4Test.java
        self.assertEqual(
            Sift4Simplest(5).dist_abs(
                'This is the first string', 'And this is another string'
            ),
            13,
        )
        self.assertEqual(
            Sift4Simplest(10).dist_abs(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                f"Amet Lorm ispum dolor sit amet, consetetur adixxxpiscing elit.",
            ),
            20,
        )


if __name__ == '__main__':
    unittest.main()
