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

"""abydos.tests.distance.test_distance_pearson_ii.

This module contains unit tests for abydos.distance.PearsonII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import PearsonII


class PearsonIITestCases(unittest.TestCase):
    """Test PearsonII functions.

    abydos.distance.PearsonII
    """

    cmp = PearsonII()

    def test_pearson_ii_sim(self):
        """Test abydos.distance.PearsonII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.7071067811865476)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.006418353030552324)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4444480535)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4444480535)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4444480535)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4444480535)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5525391276
        )


if __name__ == '__main__':
    unittest.main()
