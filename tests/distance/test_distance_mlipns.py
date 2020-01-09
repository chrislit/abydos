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

"""abydos.tests.distance.test_distance_mlipns.

This module contains unit tests for abydos.distance.MLIPNS
"""

import unittest

from abydos.distance import MLIPNS, dist_mlipns, sim_mlipns


class MLIPNSTestCases(unittest.TestCase):
    """Test MLIPNS functions.

    abydos.distance.MLIPNS
    """

    cmp = MLIPNS()

    def test_mlipns_sim(self):
        """Test abydos.distance.MLIPNS.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('a', ''), 0)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('ab', 'a'), 1)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1)
        self.assertEqual(self.cmp.sim('abc', 'abcde'), 1)
        self.assertEqual(self.cmp.sim('abcg', 'abcdeg'), 1)
        self.assertEqual(self.cmp.sim('abcg', 'abcdefg'), 0)
        self.assertEqual(self.cmp.sim('Tomato', 'Tamato'), 1)
        self.assertEqual(self.cmp.sim('ato', 'Tam'), 1)

        # Test wrapper
        self.assertEqual(sim_mlipns('abcg', 'abcdeg'), 1)

    def test_mlipns_dist(self):
        """Test abydos.distance.MLIPNS.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('a', ''), 1)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('ab', 'a'), 0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist('abc', 'abcde'), 0)
        self.assertEqual(self.cmp.dist('abcg', 'abcdeg'), 0)
        self.assertEqual(self.cmp.dist('abcg', 'abcdefg'), 1)
        self.assertEqual(self.cmp.dist('Tomato', 'Tamato'), 0)
        self.assertEqual(self.cmp.dist('ato', 'Tam'), 0)

        # Test wrapper
        self.assertEqual(dist_mlipns('abcg', 'abcdefg'), 1)


if __name__ == '__main__':
    unittest.main()
