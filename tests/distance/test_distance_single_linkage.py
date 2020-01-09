# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_single_linkage.

This module contains unit tests for abydos.distance.SingleLinkage
"""

import unittest

from abydos.distance import JaroWinkler, SingleLinkage


class SingleLinkageTestCases(unittest.TestCase):
    """Test SingleLinkage functions.

    abydos.distance.SingleLinkage
    """

    cmp = SingleLinkage()
    cmp_jw = SingleLinkage(metric=JaroWinkler())

    def test_single_linkage_dist(self):
        """Test abydos.distance.SingleLinkage.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0)

    def test_single_linkage_sim(self):
        """Test abydos.distance.SingleLinkage.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.5)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 1.0)

    def test_single_linkage_dist_abs(self):
        """Test abydos.distance.SingleLinkage.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('a', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('', 'a'), float('inf'))
        self.assertEqual(self.cmp.dist_abs('abc', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('', 'abc'), float('inf'))
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 1)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 0)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 0)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 0)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 0)
        self.assertAlmostEqual(self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 0)

        self.assertAlmostEqual(self.cmp_jw.dist_abs('abcd', 'dj'), 1 / 3)


if __name__ == '__main__':
    unittest.main()
