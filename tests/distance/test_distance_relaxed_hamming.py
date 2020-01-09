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

"""abydos.tests.distance.test_distance_relaxed_hamming.

This module contains unit tests for abydos.distance.RelaxedHamming
"""

import unittest

from abydos.distance import RelaxedHamming


class RelaxedHammingTestCases(unittest.TestCase):
    """Test RelaxedHamming functions.

    abydos.distance.RelaxedHamming
    """

    cmp = RelaxedHamming()

    def test_relaxed_hamming_dist(self):
        """Test abydos.distance.RelaxedHamming.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.24)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.08)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.08)
        self.assertAlmostEqual(self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.36)

        self.assertAlmostEqual(
            self.cmp.dist('hamming', 'hamstring'), 0.37777777777
        )

        # coverage
        self.assertAlmostEqual(
            RelaxedHamming(qval=2).dist('Nigel', 'Niall'), 0.5
        )
        self.assertAlmostEqual(
            RelaxedHamming(qval=2).dist('Nigal', 'Niall'), 0.3666666666666667
        )
        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall\1'), 0.5)

    def test_relaxed_hamming_dist_abs(self):
        """Test abydos.distance.RelaxedHamming.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 3.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 3.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 4.0)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 2.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 1.2)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 0.4)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 0.4)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 3.6
        )

        self.assertAlmostEqual(self.cmp.dist_abs('hamming', 'hamstring'), 3.4)


if __name__ == '__main__':
    unittest.main()
