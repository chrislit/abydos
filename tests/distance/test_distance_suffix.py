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

"""abydos.tests.distance.test_distance_suffix.

This module contains unit tests for abydos.distance.suffix
"""

import unittest

from abydos.distance import Suffix


class SuffixTestCases(unittest.TestCase):
    """Test suffix similarity functions.

    abydos.distance.Suffix
    """

    cmp = Suffix()

    def test_suffix_sim(self):
        """Test abydos.distance.Suffix.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('a', ''), 0)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('ax', 'a'), 0)
        self.assertEqual(self.cmp.sim('axx', 'a'), 0)
        self.assertEqual(self.cmp.sim('ax', 'ay'), 0)
        self.assertEqual(self.cmp.sim('a', 'ay'), 0)
        self.assertEqual(self.cmp.sim('a', 'ayy'), 0)
        self.assertEqual(self.cmp.sim('ax', 'ay'), 0)
        self.assertEqual(self.cmp.sim('a', 'y'), 0)
        self.assertEqual(self.cmp.sim('y', 'a'), 0)
        self.assertEqual(self.cmp.sim('aaax', 'aaa'), 0)
        self.assertEqual(self.cmp.sim('axxx', 'aaa'), 0)
        self.assertEqual(self.cmp.sim('aaxx', 'aayy'), 0)
        self.assertEqual(self.cmp.sim('xxaa', 'yyaa'), 1 / 2)
        self.assertEqual(self.cmp.sim('aaxxx', 'aay'), 0)
        self.assertEqual(self.cmp.sim('aaxxxx', 'aayyy'), 0)
        self.assertEqual(self.cmp.sim('xa', 'a'), 1)
        self.assertEqual(self.cmp.sim('xxa', 'a'), 1)
        self.assertEqual(self.cmp.sim('xa', 'ya'), 1 / 2)
        self.assertEqual(self.cmp.sim('a', 'ya'), 1)
        self.assertEqual(self.cmp.sim('a', 'yya'), 1)
        self.assertEqual(self.cmp.sim('xa', 'ya'), 1 / 2)
        self.assertEqual(self.cmp.sim('xaaa', 'aaa'), 1)
        self.assertAlmostEqual(self.cmp.sim('xxxa', 'aaa'), 1 / 3)
        self.assertAlmostEqual(self.cmp.sim('xxxaa', 'yaa'), 2 / 3)
        self.assertEqual(self.cmp.sim('xxxxaa', 'yyyaa'), 2 / 5)

    def test_suffix_dist(self):
        """Test abydos.distance.Suffix.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('a', ''), 1)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('ax', 'a'), 1)
        self.assertEqual(self.cmp.dist('axx', 'a'), 1)
        self.assertEqual(self.cmp.dist('ax', 'ay'), 1)
        self.assertEqual(self.cmp.dist('a', 'ay'), 1)
        self.assertEqual(self.cmp.dist('a', 'ayy'), 1)
        self.assertEqual(self.cmp.dist('ax', 'ay'), 1)
        self.assertEqual(self.cmp.dist('a', 'y'), 1)
        self.assertEqual(self.cmp.dist('y', 'a'), 1)
        self.assertEqual(self.cmp.dist('aaax', 'aaa'), 1)
        self.assertEqual(self.cmp.dist('axxx', 'aaa'), 1)
        self.assertEqual(self.cmp.dist('aaxx', 'aayy'), 1)
        self.assertEqual(self.cmp.dist('xxaa', 'yyaa'), 1 / 2)
        self.assertEqual(self.cmp.dist('aaxxx', 'aay'), 1)
        self.assertEqual(self.cmp.dist('aaxxxx', 'aayyy'), 1)
        self.assertEqual(self.cmp.dist('xa', 'a'), 0)
        self.assertEqual(self.cmp.dist('xxa', 'a'), 0)
        self.assertEqual(self.cmp.dist('xa', 'ya'), 1 / 2)
        self.assertEqual(self.cmp.dist('a', 'ya'), 0)
        self.assertEqual(self.cmp.dist('a', 'yya'), 0)
        self.assertEqual(self.cmp.dist('xa', 'ya'), 1 / 2)
        self.assertEqual(self.cmp.dist('xaaa', 'aaa'), 0)
        self.assertAlmostEqual(self.cmp.dist('xxxa', 'aaa'), 2 / 3)
        self.assertAlmostEqual(self.cmp.dist('xxxaa', 'yaa'), 1 / 3)
        self.assertEqual(self.cmp.dist('xxxxaa', 'yyyaa'), 3 / 5)


if __name__ == '__main__':
    unittest.main()
