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

"""abydos.tests.distance.test_distance_gini.

This module contains unit tests for abydos.distance.Gini
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Gini


class GiniTestCases(unittest.TestCase):
    """Test Gini functions.

    abydos.distance.Gini
    """

    cmp = Gini()
    cmp_no_d = Gini(alphabet=1)

    def test_gini_sim(self):
        """Test abydos.distance.Gini.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), float('nan'))

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), float('nan'))
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), float('nan'))
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), float('nan'))
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), float('nan'))
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), float('nan')
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), float('nan'))

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), float('nan')
        )


if __name__ == '__main__':
    unittest.main()
