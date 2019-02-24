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

"""abydos.tests.distance.test_distance_kuhns_xii.

This module contains unit tests for abydos.distance.KuhnsXII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsXII


class KuhnsXIITestCases(unittest.TestCase):
    """Test KuhnsXII functions.

    abydos.distance.KuhnsXII
    """

    cmp = KuhnsXII()
    cmp_no_d = KuhnsXII(alphabet=1)

    def test_kuhns_xii_sim(self):
        """Test abydos.distance.KuhnsXII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 195.5)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.4)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 65.0)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 65.0)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 65.0)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 65.0)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 49.7)

    def test_kuhns_xii_dist(self):
        """Test abydos.distance.KuhnsXII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), -194.5)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.4)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), -64.0)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), -64.0)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), -64.0)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), -64.0)
        self.assertAlmostEqual(self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), -48.7)


if __name__ == '__main__':
    unittest.main()
