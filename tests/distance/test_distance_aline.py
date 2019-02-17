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

"""abydos.tests.distance.test_distance_aline.

This module contains unit tests for abydos.distance.ALINE
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ALINE


class ALINETestCases(unittest.TestCase):
    """Test ALINE functions.

    abydos.distance.ALINE
    """

    cmp = ALINE()

    def test_aline_sim(self):
        """Test abydos.distance.ALINE.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.44583333333333336)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.625)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.625)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.775)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.775)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), float('nan')
        )

    def test_aline_sim_abs(self):
        """Test abydos.distance.ALINE.sim_abs."""
        # Base cases
        self.assertEqual(self.cmp.sim_abs('', ''), 0.0)
        self.assertEqual(self.cmp.sim_abs('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_abs('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_abs('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_abs('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_abs('abc', 'abc'), 85.0)
        self.assertEqual(self.cmp.sim_abs('abcd', 'efgh'), 53.5)

        self.assertAlmostEqual(self.cmp.sim_abs('Nigel', 'Niall'), 62.5)
        self.assertAlmostEqual(self.cmp.sim_abs('Niall', 'Nigel'), 62.5)
        self.assertAlmostEqual(self.cmp.sim_abs('Colin', 'Coiln'), 77.5)
        self.assertAlmostEqual(self.cmp.sim_abs('Coiln', 'Colin'), 77.5)
        self.assertAlmostEqual(
            self.cmp.sim_abs('ATCAACGAGT', 'AACGATTAG'), 0.0
        )


if __name__ == '__main__':
    unittest.main()
