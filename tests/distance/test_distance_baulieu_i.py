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

"""abydos.tests.distance.test_distance_baulieu_i.

This module contains unit tests for abydos.distance.BaulieuI
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import BaulieuI


class BaulieuITestCases(unittest.TestCase):
    """Test BaulieuI functions.

    abydos.distance.BaulieuI
    """

    cmp = BaulieuI()
    cmp_no_d = BaulieuI(alphabet=1)

    def test_baulieu_i_sim(self):
        """Test abydos.distance.BaulieuI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.75)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.75)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.75)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.75)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5545454545
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.75)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5545454545
        )


if __name__ == '__main__':
    unittest.main()
