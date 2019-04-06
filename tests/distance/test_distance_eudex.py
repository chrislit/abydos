# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_eudex.

This module contains unit tests for abydos.distance.Eudex
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Eudex, dist_eudex, eudex_hamming, sim_eudex


def _yield_1():
    while True:
        yield 1


class EudexTestCases(unittest.TestCase):
    """Test Eudex distance functions.

    abydos.distance.Eudex
    """

    cmp = Eudex()

    def test_eudex_dist_abs(self):
        """Test abydos.distance.Eudex.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(Eudex(None).dist_abs('', ''), 0)
        self.assertEqual(Eudex('fibonacci').dist_abs('', ''), 0)
        self.assertEqual(Eudex([10, 1, 1, 1]).dist_abs('', ''), 0)
        self.assertEqual(Eudex(_yield_1).dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', '', normalized=True), 0)

        self.assertEqual(self.cmp.dist_abs('Niall', 'Niall'), 0)
        self.assertEqual(Eudex(None).dist_abs('Niall', 'Niall'), 0)
        self.assertEqual(Eudex('fibonacci').dist_abs('Niall', 'Niall'), 0)
        self.assertEqual(Eudex([10, 1, 1, 1]).dist_abs('Niall', 'Niall'), 0)
        self.assertEqual(Eudex(_yield_1).dist_abs('Niall', 'Niall'), 0)
        self.assertEqual(
            self.cmp.dist_abs('Niall', 'Niall', normalized=True), 0
        )

        self.assertEqual(self.cmp.dist_abs('Niall', 'Neil'), 2)
        self.assertEqual(Eudex(None).dist_abs('Niall', 'Neil'), 1)
        self.assertEqual(Eudex('fibonacci').dist_abs('Niall', 'Neil'), 2)
        self.assertEqual(Eudex([10, 1, 1, 1]).dist_abs('Niall', 'Neil'), 1)
        self.assertEqual(Eudex(_yield_1).dist_abs('Niall', 'Neil'), 1)
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Neil', normalized=True), 0.00098039
        )

        self.assertEqual(self.cmp.dist_abs('Niall', 'Colin'), 524)
        self.assertEqual(Eudex(None).dist_abs('Niall', 'Colin'), 10)
        self.assertEqual(Eudex('fibonacci').dist_abs('Niall', 'Colin'), 146)
        self.assertEqual(Eudex([10, 1, 1, 1]).dist_abs('Niall', 'Colin'), 42)
        self.assertEqual(Eudex(_yield_1).dist_abs('Niall', 'Colin'), 10)
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Colin', normalized=True), 0.25686274
        )

        # Test wrapper
        self.assertEqual(eudex_hamming('Niall', 'Neil', 'fibonacci'), 2)

    def test_eudex_dist(self):
        """Test abydos.distance.Eudex.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(Eudex(None).dist('', ''), 0)
        self.assertEqual(Eudex('fibonacci').dist('', ''), 0)

        self.assertEqual(self.cmp.dist('Niall', 'Niall'), 0)
        self.assertEqual(Eudex(None).dist('Niall', 'Niall'), 0)
        self.assertEqual(Eudex('fibonacci').dist('Niall', 'Niall'), 0)

        self.assertAlmostEqual(self.cmp.dist('Niall', 'Neil'), 0.00098039)
        self.assertAlmostEqual(Eudex(None).dist('Niall', 'Neil'), 0.11111111)
        self.assertAlmostEqual(
            Eudex('fibonacci').dist('Niall', 'Neil'), 0.00287356
        )

        self.assertAlmostEqual(self.cmp.dist('Niall', 'Colin'), 0.25686275)
        self.assertAlmostEqual(Eudex(None).dist('Niall', 'Colin'), 0.16666667)
        self.assertAlmostEqual(
            Eudex('fibonacci').dist('Niall', 'Colin'), 0.20977011
        )

        with self.assertRaises(ValueError):
            Eudex('veryLarge').dist_abs('Niall', 'Colin')

        # Test wrapper
        self.assertAlmostEqual(
            dist_eudex('Niall', 'Neil', 'fibonacci'), 0.00287356
        )

    def test_eudex_sim(self):
        """Test abydos.distance.Eudex.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(Eudex(None).sim('', ''), 1)
        self.assertEqual(Eudex('fibonacci').sim('', ''), 1)

        self.assertEqual(self.cmp.sim('Niall', 'Niall'), 1)
        self.assertEqual(Eudex(None).sim('Niall', 'Niall'), 1)
        self.assertEqual(Eudex('fibonacci').sim('Niall', 'Niall'), 1)

        self.assertAlmostEqual(self.cmp.sim('Niall', 'Neil'), 0.99901961)
        self.assertAlmostEqual(Eudex(None).sim('Niall', 'Neil'), 0.88888889)
        self.assertAlmostEqual(
            Eudex('fibonacci').sim('Niall', 'Neil'), 0.99712644
        )

        self.assertAlmostEqual(self.cmp.sim('Niall', 'Colin'), 0.74313725)
        self.assertAlmostEqual(Eudex(None).sim('Niall', 'Colin'), 0.83333333)
        self.assertAlmostEqual(
            Eudex('fibonacci').sim('Niall', 'Colin'), 0.79022989
        )

        # Test wrapper
        self.assertAlmostEqual(
            sim_eudex('Niall', 'Neil', 'fibonacci'), 0.99712644
        )


if __name__ == '__main__':
    unittest.main()
