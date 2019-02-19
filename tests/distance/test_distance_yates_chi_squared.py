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

"""abydos.tests.distance.test_distance_yates_chi_squared.

This module contains unit tests for abydos.distance.YatesChiSquared
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import YatesChiSquared


class YatesChiSquaredTestCases(unittest.TestCase):
    """Test YatesChiSquared functions.

    abydos.distance.YatesChiSquared
    """

    cmp = YatesChiSquared()

    def test_yates_chi_squared_sim(self):
        """Test abydos.distance.YatesChiSquared.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 601.5458464825773)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 6.960385076156687)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 133.4890783477)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 133.4890783477)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 133.4890783477)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 133.4890783477)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 298.3719265483
        )


if __name__ == '__main__':
    unittest.main()
