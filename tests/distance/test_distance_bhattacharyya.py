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

"""abydos.tests.distance.test_distance_bhattacharyya.

This module contains unit tests for abydos.distance.Bhattacharyya
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Bhattacharyya


class BhattacharyyaTestCases(unittest.TestCase):
    """Test Bhattacharyya functions.

    abydos.distance.Bhattacharyya
    """

    cmp = Bhattacharyya()

    def test_bhattacharyya_dist_abs(self):
        """Test abydos.distance.Bhattacharyya.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), float('nan'))
        self.assertEqual(self.cmp.dist_abs('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist_abs('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist_abs('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist_abs('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), -1.3862943611198906)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), float('nan'))

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), -1.0986122887
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), -1.0986122887
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), -1.0986122887
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), -1.0986122887
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), -1.9459101491
        )


if __name__ == '__main__':
    unittest.main()
