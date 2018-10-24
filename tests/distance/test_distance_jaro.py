# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tests.test_distance.jaro.

This module contains unit tests for abydos.distance.jaro
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance.jaro import (
    dist_jaro_winkler,
    dist_strcmp95,
    sim_jaro_winkler,
    sim_strcmp95,
)


class JaroWinklerTestCases(unittest.TestCase):
    """Test Jaro(-Winkler) functions.

    abydos.distance.sim_strcmp95, .dist_strcmp95, .sim_jaro_winkler, &
    .dist_jaro_winkler
    """

    def test_sim_strcmp95(self):
        """Test abydos.distance.sim_strcmp95."""
        self.assertEqual(sim_strcmp95('', ''), 1)
        self.assertEqual(sim_strcmp95('MARTHA', ''), 0)
        self.assertEqual(sim_strcmp95('', 'MARTHA'), 0)
        self.assertEqual(sim_strcmp95('MARTHA', 'MARTHA'), 1)

        self.assertAlmostEqual(sim_strcmp95('MARTHA', 'MARHTA'), 0.96111111)
        self.assertAlmostEqual(sim_strcmp95('DWAYNE', 'DUANE'), 0.873)
        self.assertAlmostEqual(sim_strcmp95('DIXON', 'DICKSONX'), 0.839333333)

        self.assertAlmostEqual(sim_strcmp95('ABCD', 'EFGH'), 0.0)

        # long_strings = True
        self.assertAlmostEqual(
            sim_strcmp95('DIXON', 'DICKSONX', True), 0.85393939
        )
        self.assertAlmostEqual(
            sim_strcmp95('DWAYNE', 'DUANE', True), 0.89609090
        )
        self.assertAlmostEqual(
            sim_strcmp95('MARTHA', 'MARHTA', True), 0.97083333
        )

        # cover case where we don't boost, etc.
        self.assertAlmostEqual(sim_strcmp95('A', 'ABCDEFGHIJK'), 69 / 99)
        self.assertAlmostEqual(sim_strcmp95('A', 'ABCDEFGHIJK', True), 69 / 99)
        self.assertAlmostEqual(sim_strcmp95('d', 'abcdefgh'), 0.708333333)
        self.assertAlmostEqual(
            sim_strcmp95('d', 'abcdefgh', True), 0.708333333
        )
        self.assertAlmostEqual(
            sim_strcmp95('1', 'abc1efgh', True), 0.708333333
        )
        self.assertAlmostEqual(
            sim_strcmp95('12hundredths', '12hundred', True), 0.916666667
        )

    def test_dist_strcmp95(self):
        """Test abydos.distance.dist_strcmp95."""
        self.assertEqual(dist_strcmp95('', ''), 0)
        self.assertEqual(dist_strcmp95('MARTHA', ''), 1)
        self.assertEqual(dist_strcmp95('', 'MARTHA'), 1)
        self.assertEqual(dist_strcmp95('MARTHA', 'MARTHA'), 0)

        self.assertAlmostEqual(dist_strcmp95('MARTHA', 'MARHTA'), 0.03888888)
        self.assertAlmostEqual(dist_strcmp95('DWAYNE', 'DUANE'), 0.127)
        self.assertAlmostEqual(dist_strcmp95('DIXON', 'DICKSONX'), 0.160666666)

        self.assertAlmostEqual(dist_strcmp95('ABCD', 'EFGH'), 1.0)

    def test_sim_jaro_winkler(self):
        """Test abydos.distance.sim_jaro_winkler."""
        self.assertEqual(sim_jaro_winkler('', '', mode='jaro'), 1)
        self.assertEqual(sim_jaro_winkler('', '', mode='winkler'), 1)
        self.assertEqual(sim_jaro_winkler('MARTHA', '', mode='jaro'), 0)
        self.assertEqual(sim_jaro_winkler('MARTHA', '', mode='winkler'), 0)
        self.assertEqual(sim_jaro_winkler('', 'MARHTA', mode='jaro'), 0)
        self.assertEqual(sim_jaro_winkler('', 'MARHTA', mode='winkler'), 0)
        self.assertEqual(sim_jaro_winkler('MARTHA', 'MARTHA', mode='jaro'), 1)
        self.assertEqual(
            sim_jaro_winkler('MARTHA', 'MARTHA', mode='winkler'), 1
        )

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertAlmostEqual(
            sim_jaro_winkler('MARTHA', 'MARHTA', mode='jaro'), 0.94444444
        )
        self.assertAlmostEqual(
            sim_jaro_winkler('MARTHA', 'MARHTA', mode='winkler'), 0.96111111
        )
        self.assertAlmostEqual(
            sim_jaro_winkler('DWAYNE', 'DUANE', mode='jaro'), 0.82222222
        )
        self.assertAlmostEqual(
            sim_jaro_winkler('DWAYNE', 'DUANE', mode='winkler'), 0.84
        )
        self.assertAlmostEqual(
            sim_jaro_winkler('DIXON', 'DICKSONX', mode='jaro'), 0.76666666
        )
        self.assertAlmostEqual(
            sim_jaro_winkler('DIXON', 'DICKSONX', mode='winkler'), 0.81333333
        )

        self.assertRaises(
            ValueError, sim_jaro_winkler, 'abcd', 'dcba', boost_threshold=2
        )
        self.assertRaises(
            ValueError, sim_jaro_winkler, 'abcd', 'dcba', boost_threshold=-1
        )
        self.assertRaises(
            ValueError, sim_jaro_winkler, 'abcd', 'dcba', scaling_factor=0.3
        )
        self.assertRaises(
            ValueError, sim_jaro_winkler, 'abcd', 'dcba', scaling_factor=-1
        )

        self.assertAlmostEqual(sim_jaro_winkler('ABCD', 'EFGH'), 0.0)

        # long_strings = True (applies only to Jaro-Winkler, not Jaro)
        self.assertEqual(
            sim_jaro_winkler('ABCD', 'EFGH', long_strings=True),
            sim_jaro_winkler('ABCD', 'EFGH'),
        )
        self.assertEqual(
            sim_jaro_winkler(
                'DIXON', 'DICKSONX', mode='jaro', long_strings=True
            ),
            sim_jaro_winkler('DIXON', 'DICKSONX', mode='jaro'),
        )
        self.assertAlmostEqual(
            sim_jaro_winkler(
                'DIXON', 'DICKSONX', mode='winkler', long_strings=True
            ),
            0.83030303,
        )
        self.assertAlmostEqual(
            sim_jaro_winkler(
                'MARTHA', 'MARHTA', mode='winkler', long_strings=True
            ),
            0.97083333,
        )

    def test_dist_jaro_winkler(self):
        """Test abydos.distance.dist_jaro_winkler."""
        self.assertEqual(dist_jaro_winkler('', '', mode='jaro'), 0)
        self.assertEqual(dist_jaro_winkler('', '', mode='winkler'), 0)
        self.assertEqual(dist_jaro_winkler('MARTHA', '', mode='jaro'), 1)
        self.assertEqual(dist_jaro_winkler('MARTHA', '', mode='winkler'), 1)
        self.assertEqual(dist_jaro_winkler('', 'MARHTA', mode='jaro'), 1)
        self.assertEqual(dist_jaro_winkler('', 'MARHTA', mode='winkler'), 1)
        self.assertEqual(dist_jaro_winkler('MARTHA', 'MARTHA', mode='jaro'), 0)
        self.assertEqual(
            dist_jaro_winkler('MARTHA', 'MARTHA', mode='winkler'), 0
        )

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertAlmostEqual(
            dist_jaro_winkler('MARTHA', 'MARHTA', mode='jaro'), 0.05555555
        )
        self.assertAlmostEqual(
            dist_jaro_winkler('MARTHA', 'MARHTA', mode='winkler'), 0.03888888
        )
        self.assertAlmostEqual(
            dist_jaro_winkler('DWAYNE', 'DUANE', mode='jaro'), 0.17777777
        )
        self.assertAlmostEqual(
            dist_jaro_winkler('DWAYNE', 'DUANE', mode='winkler'), 0.16
        )
        self.assertAlmostEqual(
            dist_jaro_winkler('DIXON', 'DICKSONX', mode='jaro'), 0.23333333
        )
        self.assertAlmostEqual(
            dist_jaro_winkler('DIXON', 'DICKSONX', mode='winkler'), 0.18666666
        )

        self.assertRaises(
            ValueError, dist_jaro_winkler, 'abcd', 'dcba', boost_threshold=2
        )
        self.assertRaises(
            ValueError, dist_jaro_winkler, 'abcd', 'dcba', boost_threshold=-1
        )
        self.assertRaises(
            ValueError, dist_jaro_winkler, 'abcd', 'dcba', scaling_factor=0.3
        )
        self.assertRaises(
            ValueError, dist_jaro_winkler, 'abcd', 'dcba', scaling_factor=-1
        )

        self.assertAlmostEqual(dist_jaro_winkler('ABCD', 'EFGH'), 1.0)


if __name__ == '__main__':
    unittest.main()
