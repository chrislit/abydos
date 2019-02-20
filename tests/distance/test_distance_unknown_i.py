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

"""abydos.tests.distance.test_distance_unknown_i.

This module contains unit tests for abydos.distance.UnknownI
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import UnknownI


class UnknownITestCases(unittest.TestCase):
    """Test UnknownI functions.

    abydos.distance.UnknownI
    """

    cmp = UnknownI()

    def test_unknown_i_sim(self):
        """Test abydos.distance.UnknownI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), -1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -2.5)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), -2.5)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), -2.5)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), -2.5)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), -2.5)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), -4.8325761875
        )

    def test_unknown_i_dist(self):
        """Test abydos.distance.UnknownI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), 2.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 3.5)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 3.5)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 3.5)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 3.5)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 3.5)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 5.8325761875
        )


if __name__ == '__main__':
    unittest.main()
