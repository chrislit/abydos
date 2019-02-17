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

"""abydos.tests.distance.test_distance_azzoo.

This module contains unit tests for abydos.distance.AZZOO
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import AZZOO


class AZZOOTestCases(unittest.TestCase):
    """Test AZZOO functions.

    abydos.distance.AZZOO
    """

    cmp = AZZOO()

    def test_azzoo_sim(self):
        """Test abydos.distance.AZZOO.sim."""
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

    def test_azzoo_sim_abs(self):
        """Test abydos.distance.AZZOO.sim_abs."""
        # Base cases
        self.assertEqual(self.cmp.sim_abs('', ''), 0.0)
        self.assertEqual(self.cmp.sim_abs('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_abs('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_abs('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_abs('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_abs('abc', 'abc'), 4.0)
        self.assertEqual(self.cmp.sim_abs('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim_abs('Nigel', 'Niall'), 3.0)
        self.assertAlmostEqual(self.cmp.sim_abs('Niall', 'Nigel'), 3.0)
        self.assertAlmostEqual(self.cmp.sim_abs('Colin', 'Coiln'), 3.0)
        self.assertAlmostEqual(self.cmp.sim_abs('Coiln', 'Colin'), 3.0)
        self.assertAlmostEqual(
            self.cmp.sim_abs('ATCAACGAGT', 'AACGATTAG'), 7.0
        )


if __name__ == '__main__':
    unittest.main()
