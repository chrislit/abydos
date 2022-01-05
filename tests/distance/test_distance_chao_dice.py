# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_chao_dice.

This module contains unit tests for abydos.distance.ChaoDice
"""

import random
import sys
import unittest

from abydos.distance import ChaoDice


class ChaoDiceTestCases(unittest.TestCase):
    """Test ChaoDice functions.

    abydos.distance.ChaoDice
    """

    cmp = ChaoDice()

    def test_chao_dice_sim(self):
        """Test abydos.distance.ChaoDice.sim."""
        # Skip testing for Python <= 3.5
        if sys.version_info[0:2] < (3, 6):
            return

        random.seed(0)

        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.4230769230769231)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.2361111111)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5596491228)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.67327824
        )

    def test_chao_dice_sim_score(self):
        """Test abydos.distance.ChaoDice.sim_score."""
        # Skip testing for Python <= 3.5
        if sys.version_info[0:2] < (3, 6):
            return

        random.seed(0)

        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('a', 'a'), 1.5)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 0.4230769230769231)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 0.2361111111
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 0.5596491228
        )
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.67327824
        )


if __name__ == '__main__':
    unittest.main()
