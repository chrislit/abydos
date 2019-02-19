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

    def test_pearson_chi_squared_sim(self):
        """Test abydos.distance.PearsonChiSquared.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 788.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.032298410951138765)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 193.7269975747)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 193.7269975747)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 193.7269975747)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 193.7269975747)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 347.6201475023
        )


if __name__ == '__main__':
    unittest.main()
