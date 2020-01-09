# -*- coding: utf-8 -*-

# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_phonetic_distance.

This module contains unit tests for abydos.distance.PhoneticDistance
"""

import unittest

from abydos.distance import JaroWinkler, Levenshtein, PhoneticDistance
from abydos.fingerprint import OmissionKey
from abydos.phonetic import Metaphone, Soundex
from abydos.stemmer import Porter2


class PhoneticDistanceTestCases(unittest.TestCase):
    """Test phonetic distance functions.

    abydos.distance.PhoneticDistance
    """

    sdx = PhoneticDistance(transforms=Soundex)
    sdx_lev = PhoneticDistance(transforms=Soundex(), metric=Levenshtein())
    # Having mixed instantiated & uninstantiated classes is... weird... but
    # this covers another line of code.
    three_jaro = PhoneticDistance(
        transforms=[Porter2, Metaphone, OmissionKey()],
        metric=JaroWinkler,
        encode_alpha=True,
    )

    def test_phonetic_distance_dist(self):
        """Test abydos.distance.PhoneticDistance.dist."""
        # Base cases
        self.assertEqual(self.sdx.dist('', ''), 0.0)
        self.assertEqual(self.sdx.dist('a', ''), 1.0)
        self.assertEqual(self.sdx.dist('', 'a'), 1.0)
        self.assertEqual(self.sdx.dist('abc', ''), 1.0)
        self.assertEqual(self.sdx.dist('', 'abc'), 1.0)
        self.assertEqual(self.sdx.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.sdx.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.sdx.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.sdx.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.sdx.dist('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.sdx.dist('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(self.sdx.dist('ATCAACGAGT', 'AACGATTAG'), 1.0)

        self.assertEqual(self.sdx_lev.dist('', ''), 0.0)
        self.assertEqual(self.sdx_lev.dist('a', ''), 0.25)
        self.assertEqual(self.sdx_lev.dist('', 'a'), 0.25)
        self.assertEqual(self.sdx_lev.dist('abc', ''), 0.75)
        self.assertEqual(self.sdx_lev.dist('', 'abc'), 0.75)
        self.assertEqual(self.sdx_lev.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.sdx_lev.dist('abcd', 'efgh'), 0.5)

        self.assertAlmostEqual(self.sdx_lev.dist('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.sdx_lev.dist('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.sdx_lev.dist('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.sdx_lev.dist('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.sdx_lev.dist('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

        self.assertEqual(self.three_jaro.dist('', ''), 0.0)
        self.assertEqual(self.three_jaro.dist('a', ''), 1.0)
        self.assertEqual(self.three_jaro.dist('', 'a'), 1.0)
        self.assertEqual(self.three_jaro.dist('abc', ''), 1.0)
        self.assertEqual(self.three_jaro.dist('', 'abc'), 1.0)
        self.assertEqual(self.three_jaro.dist('abc', 'abc'), 0.0)
        self.assertAlmostEqual(self.three_jaro.dist('abcd', 'efgh'), 0.4722222)

        self.assertAlmostEqual(self.three_jaro.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.three_jaro.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.three_jaro.dist('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.three_jaro.dist('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.three_jaro.dist('ATCAACGAGT', 'AACGATTAG'), 0.0
        )

        # More tests to complete coverage
        self.assertEqual(PhoneticDistance().dist('a', 'ab'), 1.0)
        self.assertRaises(TypeError, PhoneticDistance, ['hello!'])
        self.assertRaises(TypeError, PhoneticDistance, 3.14)
        self.assertRaises(TypeError, PhoneticDistance, metric=3.14)
        self.assertEqual(
            PhoneticDistance(lambda s: s.lower()).dist('ONE', 'one'), 0.0
        )

    def test_phonetic_distance_dist_abs(self):
        """Test abydos.distance.PhoneticDistance.dist_abs."""
        # Base cases
        self.assertEqual(self.sdx.dist_abs('', ''), 0)
        self.assertEqual(self.sdx.dist_abs('a', ''), 1)
        self.assertEqual(self.sdx.dist_abs('', 'a'), 1)
        self.assertEqual(self.sdx.dist_abs('abc', ''), 1)
        self.assertEqual(self.sdx.dist_abs('', 'abc'), 1)
        self.assertEqual(self.sdx.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.sdx.dist_abs('abcd', 'efgh'), 1)

        self.assertAlmostEqual(self.sdx.dist_abs('Nigel', 'Niall'), 1)
        self.assertAlmostEqual(self.sdx.dist_abs('Niall', 'Nigel'), 1)
        self.assertAlmostEqual(self.sdx.dist_abs('Colin', 'Coiln'), 0)
        self.assertAlmostEqual(self.sdx.dist_abs('Coiln', 'Colin'), 0)
        self.assertAlmostEqual(self.sdx.dist_abs('ATCAACGAGT', 'AACGATTAG'), 1)

        self.assertEqual(self.sdx_lev.dist_abs('', ''), 0)
        self.assertEqual(self.sdx_lev.dist_abs('a', ''), 1)
        self.assertEqual(self.sdx_lev.dist_abs('', 'a'), 1)
        self.assertEqual(self.sdx_lev.dist_abs('abc', ''), 3)
        self.assertEqual(self.sdx_lev.dist_abs('', 'abc'), 3)
        self.assertEqual(self.sdx_lev.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.sdx_lev.dist_abs('abcd', 'efgh'), 2)

        self.assertAlmostEqual(self.sdx_lev.dist_abs('Nigel', 'Niall'), 2)
        self.assertAlmostEqual(self.sdx_lev.dist_abs('Niall', 'Nigel'), 2)
        self.assertAlmostEqual(self.sdx_lev.dist_abs('Colin', 'Coiln'), 0)
        self.assertAlmostEqual(self.sdx_lev.dist_abs('Coiln', 'Colin'), 0)
        self.assertAlmostEqual(
            self.sdx_lev.dist_abs('ATCAACGAGT', 'AACGATTAG'), 2
        )


if __name__ == '__main__':
    unittest.main()
