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

"""abydos.tests.distance.test_distance_length.

This module contains unit tests for abydos.distance.Length
"""

import unittest

from abydos.distance import Length, dist_length, sim_length


class LengthTestCases(unittest.TestCase):
    """Test length similarity functions.

    abydos.distance.Length
    """

    cmp = Length()

    def test_length_sim(self):
        """Test abydos.distance.Length.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('a', ''), 0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('abcd', 'abcd'), 1)
        self.assertEqual(self.cmp.sim('abcd', 'dcba'), 1)
        self.assertEqual(self.cmp.sim('abc', 'cba'), 1)
        self.assertEqual(self.cmp.sim('abc', 'dcba'), 0.75)
        self.assertEqual(self.cmp.sim('abcd', 'cba'), 0.75)
        self.assertEqual(self.cmp.sim('ab', 'dcba'), 0.5)
        self.assertEqual(self.cmp.sim('abcd', 'ba'), 0.5)

        # Test wrapper
        self.assertEqual(sim_length('abcd', 'cba'), 0.75)

    def test_length_dist(self):
        """Test abydos.distance.Length.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('a', ''), 1)
        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('abcd', 'abcd'), 0)
        self.assertEqual(self.cmp.dist('abcd', 'dcba'), 0)
        self.assertEqual(self.cmp.dist('abc', 'cba'), 0)
        self.assertEqual(self.cmp.dist('abc', 'dcba'), 0.25)
        self.assertEqual(self.cmp.dist('abcd', 'cba'), 0.25)
        self.assertEqual(self.cmp.dist('ab', 'dcba'), 0.5)
        self.assertEqual(self.cmp.dist('abcd', 'ba'), 0.5)

        # Test wrapper
        self.assertEqual(dist_length('abcd', 'cba'), 0.25)


if __name__ == '__main__':
    unittest.main()
