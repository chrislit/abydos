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

"""abydos.tests.distance.test_distance_pearson_chi_squared.

This module contains unit tests for abydos.distance.PearsonChiSquared
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import PearsonChiSquared


class PearsonChiSquaredTestCases(unittest.TestCase):
    """Test PearsonChiSquared functions.

    abydos.distance.PearsonChiSquared
    """

    cmp = PearsonChiSquared()
    cmp_no_d = PearsonChiSquared(alphabet=1)

    def test_pearson_chi_squared_sim(self):
        """Test abydos.distance.PearsonChiSquared.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 784.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.032298410951138765)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 192.9885210909)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 192.9885210909)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 192.9885210909)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 192.9885210909)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 344.5438630111
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 10.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 2.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 2.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 2.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 2.25)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 1.5272727273
        )


if __name__ == '__main__':
    unittest.main()
