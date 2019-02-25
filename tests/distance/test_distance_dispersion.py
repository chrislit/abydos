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

"""abydos.tests.distance.test_distance_dispersion.

This module contains unit tests for abydos.distance.Dispersion
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Dispersion


class DispersionTestCases(unittest.TestCase):
    """Test Dispersion functions.

    abydos.distance.Dispersion
    """

    cmp = Dispersion()
    cmp_no_d = Dispersion(alphabet=0)

    def test_dispersion_sim(self):
        """Test abydos.distance.Dispersion.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.005076009995835068)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -4.06731570179092e-05)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0037679613)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0037679613)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0037679613)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0037679613)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0087496095
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -0.25)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), -0.1111111111
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), -0.1111111111
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), -0.1111111111
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), -0.1111111111
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), -0.0612244898
        )

    def test_dispersion_dist(self):
        """Test abydos.distance.Dispersion.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.994923990004165)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.000040673157018)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.9962320387)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.9962320387)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.9962320387)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.9962320387)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.9912503905
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.25)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 1.1111111111
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 1.1111111111
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 1.1111111111
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 1.1111111111
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.0612244898
        )


if __name__ == '__main__':
    unittest.main()
