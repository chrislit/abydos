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

"""abydos.tests.distance.test_distance_ozbay.

This module contains unit tests for abydos.distance.Ozbay
"""

import unittest

from abydos.distance import Ozbay


class OzbayTestCases(unittest.TestCase):
    """Test Ozbay metric functions.

    abydos.distance.Ozbay
    """

    cmp = Ozbay()

    def test_ozbay_dist_abs(self):
        """Test abydos.distance.Ozbay.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)

        self.assertAlmostEqual(
            self.cmp.dist_abs('piccadilly', 'bandage'), 73.63636363636363
        )
        self.assertAlmostEqual(self.cmp.dist_abs('abcd', 'efgh'), 16)

        # Test cases from https://github.com/hakanozbay/ozbay-metric
        self.assertEqual(self.cmp.dist_abs('ban', 'ban'), 0.0)
        self.assertAlmostEqual(self.cmp.dist_abs('ban', 'bane'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.dist_abs('ban', 'band'), 0.3333333333)
        self.assertEqual(self.cmp.dist_abs('ban', 'bat'), 0.75)
        self.assertAlmostEqual(self.cmp.dist_abs('ban', 'bands'), 1.3333333333)
        self.assertEqual(self.cmp.dist_abs('ban', 'banana'), 2.0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ban', 'bandana'), 2.3333333333
        )
        self.assertEqual(self.cmp.dist_abs('ban', 'bandit'), 3.0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ban', 'bandage'), 4.6666666666
        )

        self.assertEqual(self.cmp.dist_abs('piccadilly', 'piccadilly'), 0.0)
        self.assertEqual(self.cmp.dist_abs('piccadilly', 'piccadilyl'), 0.25)
        self.assertAlmostEqual(
            self.cmp.dist_abs('piccadilly', 'piccadlily'), 0.3333333333
        )
        self.assertEqual(self.cmp.dist_abs('piccadilly', 'picacdilly'), 0.4)
        self.assertEqual(self.cmp.dist_abs('piccadilly', 'picadily'), 0.4)
        self.assertEqual(self.cmp.dist_abs('picadily', 'piccadilly'), 0.5)
        self.assertAlmostEqual(
            self.cmp.dist_abs('piccadilly', 'picacdlily'), 1.3333333333
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ipcacdily', 'piccadilly'), 1.4814814814814814
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('piccadilly', 'ipcacdily'), 1.333333333
        )
        self.assertEqual(self.cmp.dist_abs('piccadilly', 'pcicadlyil'), 2.0)

    def test_ozbay_dist(self):
        """Test abydos.distance.Ozbay.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)

        self.assertAlmostEqual(
            self.cmp.dist('piccadilly', 'bandage'), 0.9467532467532467
        )
        self.assertAlmostEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        # Test cases from https://github.com/hakanozbay/ozbay-metric
        self.assertEqual(self.cmp.dist('ban', 'ban'), 0.0)
        self.assertAlmostEqual(
            self.cmp.dist('ban', 'bane'), 0.006944444444444444
        )
        self.assertAlmostEqual(
            self.cmp.dist('ban', 'band'), 0.006944444444444444
        )
        self.assertEqual(self.cmp.dist('ban', 'bat'), 0.02777777777777778)
        self.assertAlmostEqual(
            self.cmp.dist('ban', 'bands'), 0.03555555555555556
        )
        self.assertEqual(self.cmp.dist('ban', 'banana'), 0.05555555555555555)
        self.assertAlmostEqual(
            self.cmp.dist('ban', 'bandana'), 0.0634920634920635
        )
        self.assertEqual(self.cmp.dist('ban', 'bandit'), 0.08333333333333333)
        self.assertAlmostEqual(
            self.cmp.dist('ban', 'bandage'), 0.126984126984127
        )

        self.assertEqual(self.cmp.dist('piccadilly', 'piccadilly'), 0.0)
        self.assertEqual(
            self.cmp.dist('piccadilly', 'piccadilyl'), 0.0004999999999999999
        )
        self.assertAlmostEqual(
            self.cmp.dist('piccadilly', 'piccadlily'), 0.0013333333333333335
        )
        self.assertEqual(self.cmp.dist('piccadilly', 'picacdilly'), 0.002)
        self.assertEqual(self.cmp.dist('piccadilly', 'picadily'), 0.0025)
        self.assertEqual(self.cmp.dist('picadily', 'piccadilly'), 0.003125)
        self.assertAlmostEqual(
            self.cmp.dist('piccadilly', 'picacdlily'), 0.009333333333333334
        )
        self.assertAlmostEqual(
            self.cmp.dist('ipcacdily', 'piccadilly'), 0.011522633744855966
        )
        self.assertAlmostEqual(
            self.cmp.dist('piccadilly', 'ipcacdily'), 0.01037037037037037
        )
        self.assertEqual(self.cmp.dist('piccadilly', 'pcicadlyil'), 0.014)


if __name__ == '__main__':
    unittest.main()
