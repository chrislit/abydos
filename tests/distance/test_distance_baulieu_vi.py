# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_baulieu_vi.

This module contains unit tests for abydos.distance.BaulieuVI
"""

import unittest

from abydos.distance import BaulieuVI


class BaulieuVITestCases(unittest.TestCase):
    """Test BaulieuVI functions.

    abydos.distance.BaulieuVI
    """

    cmp = BaulieuVI()
    cmp_no_d = BaulieuVI(alphabet=0)

    def test_baulieu_vi_dist(self):
        """Test abydos.distance.BaulieuVI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.6666666666666666)
        self.assertEqual(self.cmp.dist('', 'a'), 0.6666666666666666)
        self.assertEqual(self.cmp.dist('abc', ''), 0.8)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.8)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.9090909090909091)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.6)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.6)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.6)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.6)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4666666667
        )

    def test_baulieu_vi_sim(self):
        """Test abydos.distance.BaulieuVI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.33333333333333337)
        self.assertEqual(self.cmp.sim('', 'a'), 0.33333333333333337)
        self.assertEqual(self.cmp.sim('abc', ''), 0.19999999999999996)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.19999999999999996)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.09090909090909094)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5333333333
        )


if __name__ == '__main__':
    unittest.main()
