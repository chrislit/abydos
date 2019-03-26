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
    cmp_no_d = KuhnsXII(alphabet=0)

    def test_kuhns_xii_sim(self):
        """Test abydos.distance.KuhnsXII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 195.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 64.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 64.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 64.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 64.3333333333)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 48.8909090909
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), -0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), -0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), -0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), -0.25)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), -0.1090909091
        )

    def test_kuhns_xii_dist(self):
        """Test abydos.distance.KuhnsXII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), -194.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), -63.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), -63.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), -63.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), -63.3333333333)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), -47.8909090909
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.25)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.25)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.25)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.25)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.1090909091
        )


if __name__ == '__main__':
    unittest.main()
