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

"""abydos.tests.distance.test_distance_forbes_i.

This module contains unit tests for abydos.distance.ForbesI
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ForbesI


class ForbesITestCases(unittest.TestCase):
    """Test ForbesI functions.

    abydos.distance.ForbesI
    """

    cmp = ForbesI()
    cmp_no_d = ForbesI(alphabet=1)

    def test_forbes_i_sim(self):
        """Test abydos.distance.ForbesI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 196.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 65.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 65.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 65.3333333333)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 65.3333333333)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 49.8909090909
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.75)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.8909090909
        )

    def test_forbes_i_dist(self):
        """Test abydos.distance.ForbesI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), -195.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), -64.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), -64.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), -64.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), -64.3333333333)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), -48.8909090909
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.25)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.1090909091
        )


if __name__ == '__main__':
    unittest.main()
