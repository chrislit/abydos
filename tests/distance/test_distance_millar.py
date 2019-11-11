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

"""abydos.tests.distance.test_distance_millar.

This module contains unit tests for abydos.distance.Millar
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Millar


class MillarTestCases(unittest.TestCase):
    """Test Millar functions.

    abydos.distance.Millar
    """

    cmp = Millar()

    def test_inclusion_dist_abs(self):
        """Test abydos.distance.Millar.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist_abs('a', 'a'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 0.0114358323
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 0.0114358323
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 0.0114358323
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 0.0114358323
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 0.0139593909
        )


if __name__ == '__main__':
    unittest.main()
