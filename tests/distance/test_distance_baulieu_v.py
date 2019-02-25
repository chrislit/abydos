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

"""abydos.tests.distance.test_distance_baulieu_v.

This module contains unit tests for abydos.distance.BaulieuV
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import BaulieuV


class BaulieuVTestCases(unittest.TestCase):
    """Test BaulieuV functions.

    abydos.distance.BaulieuV
    """

    cmp = BaulieuV()
    cmp_no_d = BaulieuV(alphabet=0)

    def test_baulieu_v_dist(self):
        """Test abydos.distance.BaulieuV.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.2)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.7)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.7)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.7)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.7)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5333333333
        )

    def test_baulieu_v_sim(self):
        """Test abydos.distance.BaulieuV.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.8)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.3)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.3)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.3)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.3)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4666666667
        )


if __name__ == '__main__':
    unittest.main()
