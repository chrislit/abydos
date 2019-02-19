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

"""abydos.tests.distance.test_distance_saps.

This module contains unit tests for abydos.distance.SAPS
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import SAPS


class SAPSTestCases(unittest.TestCase):
    """Test SAPS functions.

    abydos.distance.SAPS
    """

    cmp = SAPS()

    def test_saps_sim(self):
        """Test abydos.distance.SAPS.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), -0.5)
        self.assertEqual(self.cmp.sim('', 'a'), -0.5)
        self.assertEqual(self.cmp.sim('abc', ''), -0.5384615384615384)
        self.assertEqual(self.cmp.sim('', 'abc'), -0.5384615384615384)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.3684210526315789)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0666666667)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4333333333
        )

    def test_saps_sim_score(self):
        """Test abydos.distance.SAPS.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0)
        self.assertEqual(self.cmp.sim_score('a', ''), -3)
        self.assertEqual(self.cmp.sim_score('', 'a'), -3)
        self.assertEqual(self.cmp.sim_score('abc', ''), -7)
        self.assertEqual(self.cmp.sim_score('', 'abc'), -7)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 13)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), -7)

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 1)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 13
        )


if __name__ == '__main__':
    unittest.main()
