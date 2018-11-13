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

"""abydos.tests.distance.test_distance_jaro_winkler.

This module contains unit tests for abydos.distance.JaroWinkler
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import JaroWinkler, dist_jaro_winkler, sim_jaro_winkler


class JaroWinklerTestCases(unittest.TestCase):
    """Test Jaro(-Winkler) functions.

    abydos.distance.JaroWinkler
    """

    cmp = JaroWinkler()

    def test_sim_jaro_winkler(self):
        """Test abydos.distance.JaroWinkler.sim."""
        self.assertEqual(self.cmp.sim('', '', mode='jaro'), 1)
        self.assertEqual(self.cmp.sim('', '', mode='winkler'), 1)
        self.assertEqual(self.cmp.sim('MARTHA', '', mode='jaro'), 0)
        self.assertEqual(self.cmp.sim('MARTHA', '', mode='winkler'), 0)
        self.assertEqual(self.cmp.sim('', 'MARHTA', mode='jaro'), 0)
        self.assertEqual(self.cmp.sim('', 'MARHTA', mode='winkler'), 0)
        self.assertEqual(self.cmp.sim('MARTHA', 'MARTHA', mode='jaro'), 1)
        self.assertEqual(self.cmp.sim('MARTHA', 'MARTHA', mode='winkler'), 1)

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertAlmostEqual(
            self.cmp.sim('MARTHA', 'MARHTA', mode='jaro'), 0.94444444
        )
        self.assertAlmostEqual(
            self.cmp.sim('MARTHA', 'MARHTA', mode='winkler'), 0.96111111
        )
        self.assertAlmostEqual(
            self.cmp.sim('DWAYNE', 'DUANE', mode='jaro'), 0.82222222
        )
        self.assertAlmostEqual(
            self.cmp.sim('DWAYNE', 'DUANE', mode='winkler'), 0.84
        )
        self.assertAlmostEqual(
            self.cmp.sim('DIXON', 'DICKSONX', mode='jaro'), 0.76666666
        )
        self.assertAlmostEqual(
            self.cmp.sim('DIXON', 'DICKSONX', mode='winkler'), 0.81333333
        )

        self.assertRaises(
            ValueError, self.cmp.sim, 'abcd', 'dcba', boost_threshold=2
        )
        self.assertRaises(
            ValueError, self.cmp.sim, 'abcd', 'dcba', boost_threshold=-1
        )
        self.assertRaises(
            ValueError, self.cmp.sim, 'abcd', 'dcba', scaling_factor=0.3
        )
        self.assertRaises(
            ValueError, self.cmp.sim, 'abcd', 'dcba', scaling_factor=-1
        )

        self.assertAlmostEqual(self.cmp.sim('ABCD', 'EFGH'), 0.0)

        # long_strings = True (applies only to Jaro-Winkler, not Jaro)
        self.assertEqual(
            self.cmp.sim('ABCD', 'EFGH', long_strings=True),
            self.cmp.sim('ABCD', 'EFGH'),
        )
        self.assertEqual(
            self.cmp.sim('DIXON', 'DICKSONX', mode='jaro', long_strings=True),
            self.cmp.sim('DIXON', 'DICKSONX', mode='jaro'),
        )
        self.assertAlmostEqual(
            self.cmp.sim(
                'DIXON', 'DICKSONX', mode='winkler', long_strings=True
            ),
            0.83030303,
        )
        self.assertAlmostEqual(
            self.cmp.sim(
                'MARTHA', 'MARHTA', mode='winkler', long_strings=True
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
        self.assertEqual(self.cmp.dist('', '', mode='jaro'), 0)
        self.assertEqual(self.cmp.dist('', '', mode='winkler'), 0)
        self.assertEqual(self.cmp.dist('MARTHA', '', mode='jaro'), 1)
        self.assertEqual(self.cmp.dist('MARTHA', '', mode='winkler'), 1)
        self.assertEqual(self.cmp.dist('', 'MARHTA', mode='jaro'), 1)
        self.assertEqual(self.cmp.dist('', 'MARHTA', mode='winkler'), 1)
        self.assertEqual(self.cmp.dist('MARTHA', 'MARTHA', mode='jaro'), 0)
        self.assertEqual(self.cmp.dist('MARTHA', 'MARTHA', mode='winkler'), 0)

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertAlmostEqual(
            self.cmp.dist('MARTHA', 'MARHTA', mode='jaro'), 0.05555555
        )
        self.assertAlmostEqual(
            self.cmp.dist('MARTHA', 'MARHTA', mode='winkler'), 0.03888888
        )
        self.assertAlmostEqual(
            self.cmp.dist('DWAYNE', 'DUANE', mode='jaro'), 0.17777777
        )
        self.assertAlmostEqual(
            self.cmp.dist('DWAYNE', 'DUANE', mode='winkler'), 0.16
        )
        self.assertAlmostEqual(
            self.cmp.dist('DIXON', 'DICKSONX', mode='jaro'), 0.23333333
        )
        self.assertAlmostEqual(
            self.cmp.dist('DIXON', 'DICKSONX', mode='winkler'), 0.18666666
        )

        self.assertRaises(
            ValueError, self.cmp.dist, 'abcd', 'dcba', boost_threshold=2
        )
        self.assertRaises(
            ValueError, self.cmp.dist, 'abcd', 'dcba', boost_threshold=-1
        )
        self.assertRaises(
            ValueError, self.cmp.dist, 'abcd', 'dcba', scaling_factor=0.3
        )
        self.assertRaises(
            ValueError, self.cmp.dist, 'abcd', 'dcba', scaling_factor=-1
        )

        self.assertAlmostEqual(self.cmp.dist('ABCD', 'EFGH'), 1.0)

        # Test wrapper
        self.assertAlmostEqual(
            dist_jaro_winkler('DIXON', 'DICKSONX', mode='jaro'), 0.23333333
        )
        self.assertAlmostEqual(
            dist_jaro_winkler('DIXON', 'DICKSONX', mode='winkler'), 0.18666666
        )


if __name__ == '__main__':
    unittest.main()
