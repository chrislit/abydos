# -*- coding: utf-8 -*-

# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_jaro_winkler.

This module contains unit tests for abydos.distance.JaroWinkler
"""

import unittest

from abydos.distance import JaroWinkler, dist_jaro_winkler, sim_jaro_winkler


class JaroWinklerTestCases(unittest.TestCase):
    """Test Jaro(-Winkler) functions.

    abydos.distance.JaroWinkler
    """

    jaro = JaroWinkler(mode='jaro')
    jaro_winkler = JaroWinkler(mode='winkler')

    def test_sim_jaro_winkler(self):
        """Test abydos.distance.JaroWinkler.sim."""
        self.assertEqual(self.jaro.sim('', ''), 1)
        self.assertEqual(self.jaro_winkler.sim('', ''), 1)
        self.assertEqual(self.jaro.sim('MARTHA', ''), 0)
        self.assertEqual(self.jaro_winkler.sim('MARTHA', ''), 0)
        self.assertEqual(self.jaro.sim('', 'MARHTA'), 0)
        self.assertEqual(self.jaro_winkler.sim('', 'MARHTA'), 0)
        self.assertEqual(self.jaro.sim('MARTHA', 'MARTHA'), 1)
        self.assertEqual(self.jaro_winkler.sim('MARTHA', 'MARTHA'), 1)

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertAlmostEqual(self.jaro.sim('MARTHA', 'MARHTA'), 0.94444444)
        self.assertAlmostEqual(
            self.jaro_winkler.sim('MARTHA', 'MARHTA'), 0.96111111
        )
        self.assertAlmostEqual(self.jaro.sim('DWAYNE', 'DUANE'), 0.82222222)
        self.assertAlmostEqual(self.jaro_winkler.sim('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(self.jaro.sim('DIXON', 'DICKSONX'), 0.76666666)
        self.assertAlmostEqual(
            self.jaro_winkler.sim('DIXON', 'DICKSONX'), 0.81333333
        )

        self.assertRaises(
            ValueError, JaroWinkler(boost_threshold=2).sim, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, JaroWinkler(boost_threshold=-1).sim, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, JaroWinkler(scaling_factor=0.3).sim, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, JaroWinkler(scaling_factor=-1).sim, 'abcd', 'dcba'
        )

        self.assertAlmostEqual(self.jaro_winkler.sim('ABCD', 'EFGH'), 0.0)

        # long_strings = True (applies only to Jaro-Winkler, not Jaro)
        self.assertEqual(
            JaroWinkler(long_strings=True).sim('ABCD', 'EFGH'),
            self.jaro.sim('ABCD', 'EFGH'),
        )
        self.assertEqual(
            JaroWinkler(mode='jaro', long_strings=True).sim(
                'DIXON', 'DICKSONX'
            ),
            self.jaro.sim('DIXON', 'DICKSONX'),
        )
        self.assertAlmostEqual(
            JaroWinkler(mode='winkler', long_strings=True).sim(
                'DIXON', 'DICKSONX'
            ),
            0.83030303,
        )
        self.assertAlmostEqual(
            JaroWinkler(mode='winkler', long_strings=True).sim(
                'MARTHA', 'MARHTA'
            ),
            0.97083333,
        )

        # Test wrapper
        self.assertAlmostEqual(
            sim_jaro_winkler('DIXON', 'DICKSONX', mode='jaro'), 0.76666666
        )
        self.assertAlmostEqual(
            sim_jaro_winkler('DIXON', 'DICKSONX', mode='winkler'), 0.81333333
        )

    def test_dist_jaro_winkler(self):
        """Test abydos.distance.JaroWinkler.dist."""
        self.assertEqual(self.jaro.dist('', ''), 0)
        self.assertEqual(self.jaro_winkler.dist('', ''), 0)
        self.assertEqual(self.jaro.dist('MARTHA', ''), 1)
        self.assertEqual(self.jaro_winkler.dist('MARTHA', ''), 1)
        self.assertEqual(self.jaro.dist('', 'MARHTA'), 1)
        self.assertEqual(self.jaro_winkler.dist('', 'MARHTA'), 1)
        self.assertEqual(self.jaro.dist('MARTHA', 'MARTHA'), 0)
        self.assertEqual(self.jaro_winkler.dist('MARTHA', 'MARTHA'), 0)

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertAlmostEqual(self.jaro.dist('MARTHA', 'MARHTA'), 0.05555555)
        self.assertAlmostEqual(
            self.jaro_winkler.dist('MARTHA', 'MARHTA'), 0.03888888
        )
        self.assertAlmostEqual(self.jaro.dist('DWAYNE', 'DUANE'), 0.17777777)
        self.assertAlmostEqual(self.jaro_winkler.dist('DWAYNE', 'DUANE'), 0.16)
        self.assertAlmostEqual(self.jaro.dist('DIXON', 'DICKSONX'), 0.23333333)
        self.assertAlmostEqual(
            self.jaro_winkler.dist('DIXON', 'DICKSONX'), 0.18666666
        )

        self.assertRaises(
            ValueError, JaroWinkler(boost_threshold=2).dist, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, JaroWinkler(boost_threshold=-1).dist, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, JaroWinkler(scaling_factor=0.3).dist, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, JaroWinkler(scaling_factor=-1).dist, 'abcd', 'dcba'
        )

        self.assertAlmostEqual(self.jaro_winkler.dist('ABCD', 'EFGH'), 1.0)

        # Test wrapper
        self.assertAlmostEqual(
            dist_jaro_winkler('DIXON', 'DICKSONX', mode='jaro'), 0.23333333
        )
        self.assertAlmostEqual(
            dist_jaro_winkler('DIXON', 'DICKSONX', mode='winkler'), 0.18666666
        )


if __name__ == '__main__':
    unittest.main()
