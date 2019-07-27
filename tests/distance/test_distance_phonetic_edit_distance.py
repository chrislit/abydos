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

"""abydos.tests.distance.test_distance_phonetic_edit_distance.

This module contains unit tests for abydos.distance.PhoneticEditDistance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import PhoneticEditDistance


class PhoneticEditDistanceTestCases(unittest.TestCase):
    """Test phonetic edit distance functions.

    abydos.distance.PhoneticEditDistance
    """

    ped = PhoneticEditDistance()

    def test_phonetic_edit_distance_dist(self):
        """Test abydos.distance.PhoneticEditDistance.dist."""
        # Base cases
        self.assertEqual(self.ped.dist('', ''), 0.0)
        self.assertEqual(self.ped.dist('a', ''), 1.0)
        self.assertEqual(self.ped.dist('', 'a'), 1.0)
        self.assertEqual(self.ped.dist('abc', ''), 1.0)
        self.assertEqual(self.ped.dist('', 'abc'), 1.0)
        self.assertEqual(self.ped.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.ped.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.ped.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.ped.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.ped.dist('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.ped.dist('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(self.ped.dist('ATCAACGAGT', 'AACGATTAG'), 1.0)

    def test_phonetic_edit_distance_dist_abs(self):
        """Test abydos.distance.PhoneticEditDistance.dist_abs."""
        # Base cases
        self.assertEqual(self.ped.dist_abs('', ''), 0)
        self.assertEqual(self.ped.dist_abs('a', ''), 1)
        self.assertEqual(self.ped.dist_abs('', 'a'), 1)
        self.assertEqual(self.ped.dist_abs('abc', ''), 1)
        self.assertEqual(self.ped.dist_abs('', 'abc'), 1)
        self.assertEqual(self.ped.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.ped.dist_abs('abcd', 'efgh'), 1)

        self.assertAlmostEqual(self.ped.dist_abs('Nigel', 'Niall'), 1)
        self.assertAlmostEqual(self.ped.dist_abs('Niall', 'Nigel'), 1)
        self.assertAlmostEqual(self.ped.dist_abs('Colin', 'Coiln'), 0)
        self.assertAlmostEqual(self.ped.dist_abs('Coiln', 'Colin'), 0)
        self.assertAlmostEqual(self.ped.dist_abs('ATCAACGAGT', 'AACGATTAG'), 1)


if __name__ == '__main__':
    unittest.main()
