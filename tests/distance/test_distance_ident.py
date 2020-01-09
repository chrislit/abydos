# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_ident.

This module contains unit tests for abydos.distance.Ident
"""

import unittest

from abydos.distance import Ident, dist_ident, sim_ident


class IdentTestCases(unittest.TestCase):
    """Test identity similarity functions.

    abydos.distance.Ident
    """

    cmp = Ident()

    def test_ident_sim(self):
        """Test abydos.distance.Ident.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('a', ''), 0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('abcd', 'abcd'), 1)
        self.assertEqual(self.cmp.sim('abcd', 'dcba'), 0)
        self.assertEqual(self.cmp.sim('abc', 'cba'), 0)

        # Test wrapper
        self.assertEqual(sim_ident('abcd', 'dcba'), 0)

    def test_ident_dist(self):
        """Test abydos.distance.Ident.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('a', ''), 1)
        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('abcd', 'abcd'), 0)
        self.assertEqual(self.cmp.dist('abcd', 'dcba'), 1)
        self.assertEqual(self.cmp.dist('abc', 'cba'), 1)

        # Test wrapper
        self.assertEqual(dist_ident('abcd', 'dcba'), 1)


if __name__ == '__main__':
    unittest.main()
