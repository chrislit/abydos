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

"""abydos.tests.distance.test_distance_warrens_iii.

This module contains unit tests for abydos.distance.WarrensIII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import WarrensIII


class WarrensIIITestCases(unittest.TestCase):
    """Test WarrensIII functions.

    abydos.distance.WarrensIII
    """

    cmp = WarrensIII()
    cmp_no_d = WarrensIII(alphabet=0)

    def test_warrens_iii_sim(self):
        """Test abydos.distance.WarrensIII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9974457215836526)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9974457215836526)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9948849104859335)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9948849104859335)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9871630295250321)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9922879177)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9922879177)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9922879177)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9922879177)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9909502262
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), -1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), -1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), -1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), -1.0
        )

    def test_warrens_iii_dist(self):
        """Test abydos.distance.WarrensIII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0025542784163473664)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0025542784163473664)
        self.assertEqual(self.cmp.dist('abc', ''), 0.005115089514066473)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.005115089514066473)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.012836970474967901)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0077120823)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0077120823)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0077120823)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0077120823)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0090497738
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 2.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 2.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 2.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 2.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 2.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 2.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 2.0
        )


if __name__ == '__main__':
    unittest.main()
