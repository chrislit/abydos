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

"""abydos.tests.distance.test_distance_saps.

This module contains unit tests for abydos.distance.SAPS
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import SAPS
from abydos.tokenizer import QGrams


class SAPSTestCases(unittest.TestCase):
    """Test SAPS functions.

    abydos.distance.SAPS
    """

    cmp = SAPS()
    cmp_q2 = SAPS(tokenizer=QGrams(2))

    def test_saps_sim(self):
        """Test abydos.distance.SAPS.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0666666667)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4333333333
        )

        # Coverage
        self.assertAlmostEqual(
            self.cmp_q2.sim('Stevenson', 'Stinson'), 0.3857142857
        )

        # Examples from paper
        self.assertAlmostEqual(
            self.cmp.sim('Stevenson', 'Stinson'), 0.551724138
        )

    def test_saps_dist(self):
        """Test abydos.distance.SAPS.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.9333333333)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.9333333333)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.9333333333)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.9333333333)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5666666667
        )

        # Coverage
        self.assertAlmostEqual(
            self.cmp_q2.dist('Stevenson', 'Stinson'), 0.614285714
        )

        # Examples from paper
        self.assertAlmostEqual(
            self.cmp.dist('Stevenson', 'Stinson'), 0.448275862
        )

    def test_saps_sim_score(self):
        """Test abydos.distance.SAPS.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0)
        self.assertEqual(self.cmp.sim_score('a', ''), -3)
        self.assertEqual(self.cmp.sim_score('', 'a'), -3)
        self.assertEqual(self.cmp.sim_score('abc', ''), -7)
        self.assertEqual(self.cmp.sim_score('', 'abc'), -7)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 13)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), -7)

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 1)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 13
        )

        # Coverage
        self.assertEqual(self.cmp_q2.sim_score('Stevenson', 'Stinson'), 27)

        # Examples from paper
        self.assertEqual(self.cmp.sim_score('Stevenson', 'Stinson'), 16)


if __name__ == '__main__':
    unittest.main()
