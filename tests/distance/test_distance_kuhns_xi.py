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

"""abydos.tests.distance.test_distance_kuhns_xi.

This module contains unit tests for abydos.distance.KuhnsXI
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsXI


class KuhnsXITestCases(unittest.TestCase):
    """Test KuhnsXI functions.

    abydos.distance.KuhnsXI
    """

    cmp = KuhnsXI()
    cmp_no_d = KuhnsXI(alphabet=0)

    def test_kuhns_xi_sim(self):
        """Test abydos.distance.KuhnsXI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0025641025641026)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.4)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.8920030136)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.8920030136)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.8920030136)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.8920030136)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9249413152
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -0.4)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 1.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 1.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 1.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 1.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 6.4166666667
        )

    def test_kuhns_xi_dist(self):
        """Test abydos.distance.KuhnsXI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), -0.002564102564102555)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.4)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.1079969864)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.1079969864)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.1079969864)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.1079969864)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0750586848
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.4)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), -0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), -0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), -0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), -0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), -5.4166666667
        )


if __name__ == '__main__':
    unittest.main()
