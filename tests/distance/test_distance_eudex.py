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

This module contains unit tests for abydos.distance._eudex
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance import dist_eudex, eudex_hamming, sim_eudex


class EudexTestCases(unittest.TestCase):
    """Test Eudex distance functions.

    abydos.distance._eudex.eudex_hamming, dist_eudex, & sim_eudex
    """

    def test_eudex_hamming(self):
        """Test abydos.distance._eudex.eudex_hamming."""

        def _yield_1():
            while True:
                yield 1

        # Base cases
        self.assertEqual(eudex_hamming('', ''), 0)
        self.assertEqual(eudex_hamming('', '', None), 0)
        self.assertEqual(eudex_hamming('', '', 'fibonacci'), 0)
        self.assertEqual(eudex_hamming('', '', [10, 1, 1, 1]), 0)
        self.assertEqual(eudex_hamming('', '', _yield_1), 0)
        self.assertEqual(eudex_hamming('', '', normalized=True), 0)

        self.assertEqual(eudex_hamming('Niall', 'Niall'), 0)
        self.assertEqual(eudex_hamming('Niall', 'Niall', None), 0)
        self.assertEqual(eudex_hamming('Niall', 'Niall', 'fibonacci'), 0)
        self.assertEqual(eudex_hamming('Niall', 'Niall', [10, 1, 1, 1]), 0)
        self.assertEqual(eudex_hamming('Niall', 'Niall', _yield_1), 0)
        self.assertEqual(eudex_hamming('Niall', 'Niall', normalized=True), 0)

        self.assertEqual(eudex_hamming('Niall', 'Neil'), 2)
        self.assertEqual(eudex_hamming('Niall', 'Neil', None), 1)
        self.assertEqual(eudex_hamming('Niall', 'Neil', 'fibonacci'), 2)
        self.assertEqual(eudex_hamming('Niall', 'Neil', [10, 1, 1, 1]), 1)
        self.assertEqual(eudex_hamming('Niall', 'Neil', _yield_1), 1)
        self.assertAlmostEqual(
            eudex_hamming('Niall', 'Neil', normalized=True), 0.00098039
        )

        self.assertEqual(eudex_hamming('Niall', 'Colin'), 524)
        self.assertEqual(eudex_hamming('Niall', 'Colin', None), 10)
        self.assertEqual(eudex_hamming('Niall', 'Colin', 'fibonacci'), 146)
        self.assertEqual(eudex_hamming('Niall', 'Colin', [10, 1, 1, 1]), 6)
        self.assertEqual(eudex_hamming('Niall', 'Colin', _yield_1), 10)
        self.assertAlmostEqual(
            eudex_hamming('Niall', 'Colin', normalized=True), 0.25686274
        )

    def test_dist_eudex(self):
        """Test abydos.distance._eudex.dist_eudex."""
        # Base cases
        self.assertEqual(dist_eudex('', ''), 0)
        self.assertEqual(dist_eudex('', '', None), 0)
        self.assertEqual(dist_eudex('', '', 'fibonacci'), 0)

        self.assertEqual(dist_eudex('Niall', 'Niall'), 0)
        self.assertEqual(dist_eudex('Niall', 'Niall', None), 0)
        self.assertEqual(dist_eudex('Niall', 'Niall', 'fibonacci'), 0)

        self.assertAlmostEqual(dist_eudex('Niall', 'Neil'), 0.00098039)
        self.assertAlmostEqual(dist_eudex('Niall', 'Neil', None), 0.11111111)
        self.assertAlmostEqual(
            dist_eudex('Niall', 'Neil', 'fibonacci'), 0.00287356
        )

        self.assertAlmostEqual(dist_eudex('Niall', 'Colin'), 0.25686275)
        self.assertAlmostEqual(dist_eudex('Niall', 'Colin', None), 0.16666667)
        self.assertAlmostEqual(
            dist_eudex('Niall', 'Colin', 'fibonacci'), 0.20977011
        )

    def test_sim_eudex(self):
        """Test abydos.distance._eudex.sim_eudex."""
        # Base cases
        self.assertEqual(sim_eudex('', ''), 1)
        self.assertEqual(sim_eudex('', '', None), 1)
        self.assertEqual(sim_eudex('', '', 'fibonacci'), 1)

        self.assertEqual(sim_eudex('Niall', 'Niall'), 1)
        self.assertEqual(sim_eudex('Niall', 'Niall', None), 1)
        self.assertEqual(sim_eudex('Niall', 'Niall', 'fibonacci'), 1)

        self.assertAlmostEqual(sim_eudex('Niall', 'Neil'), 0.99901961)
        self.assertAlmostEqual(sim_eudex('Niall', 'Neil', None), 0.88888889)
        self.assertAlmostEqual(
            sim_eudex('Niall', 'Neil', 'fibonacci'), 0.99712644
        )

        self.assertAlmostEqual(sim_eudex('Niall', 'Colin'), 0.74313725)
        self.assertAlmostEqual(sim_eudex('Niall', 'Colin', None), 0.83333333)
        self.assertAlmostEqual(
            sim_eudex('Niall', 'Colin', 'fibonacci'), 0.79022989
        )


if __name__ == '__main__':
    unittest.main()
