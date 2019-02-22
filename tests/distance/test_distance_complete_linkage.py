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

"""abydos.tests.distance.test_distance_complete_linkage.

This module contains unit tests for abydos.distance.CompleteLinkage
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import CompleteLinkage


class CompleteLinkageTestCases(unittest.TestCase):
    """Test CompleteLinkage functions.

    abydos.distance.CompleteLinkage
    """

    cmp = CompleteLinkage()

    def test_complete_linkage_dist(self):
        """Test abydos.distance.CompleteLinkage.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('inf'))
        self.assertEqual(self.cmp.dist('a', ''), float('inf'))
        self.assertEqual(self.cmp.dist('', 'a'), float('inf'))
        self.assertEqual(self.cmp.dist('abc', ''), float('inf'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('inf'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), float('inf'))
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), float('inf'))

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), float('inf'))
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), float('inf'))
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), float('inf'))
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), float('inf'))
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), float('inf')
        )

    def test_complete_linkage_sim(self):
        """Test abydos.distance.CompleteLinkage.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), -inf)
        self.assertEqual(self.cmp.sim('a', ''), -inf)
        self.assertEqual(self.cmp.sim('', 'a'), -inf)
        self.assertEqual(self.cmp.sim('abc', ''), -inf)
        self.assertEqual(self.cmp.sim('', 'abc'), -inf)
        self.assertEqual(self.cmp.sim('abc', 'abc'), -inf)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -inf)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), -inf)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), -inf)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), -inf)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), -inf)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), -inf)

    def test_complete_linkage_dist_abs(self):
        """Test abydos.distance.CompleteLinkage.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('a', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('', 'a'), float('inf'))
        self.assertEqual(self.cmp.dist_abs('abc', ''), float('inf'))
        self.assertEqual(self.cmp.dist_abs('', 'abc'), float('inf'))
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), float('inf'))
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), float('inf'))

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), float('inf')
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), float('inf')
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), float('inf')
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), float('inf')
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), float('inf')
        )


if __name__ == '__main__':
    unittest.main()
