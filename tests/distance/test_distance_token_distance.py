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

"""abydos.tests.distance.test_distance_tulloss_r.

This module contains unit tests for abydos.distance.TullossR
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import DamerauLevenshtein, Jaccard


class TokenDistanceTestCases(unittest.TestCase):
    """Test _TokenDistance functions.

    abydos.distance._TokenDistance
    """

    cmp_j_crisp = Jaccard(intersection_type='crisp')
    cmp_j_soft = Jaccard(intersection_type='soft')
    cmp_j_fuzzy = Jaccard(
        intersection_type='fuzzy', metric=DamerauLevenshtein(), threshold=0.4
    )
    cmp_j_linkage = Jaccard(intersection_type='linkage')

    def test_crisp_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim (crisp)."""
        # Base cases
        self.assertEqual(self.cmp_j_crisp.sim('', ''), 1.0)
        self.assertEqual(self.cmp_j_crisp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_j_crisp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_j_crisp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_j_crisp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_j_crisp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_j_crisp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('Nigel', 'Niall'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('Niall', 'Nigel'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('Colin', 'Coiln'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('Coiln', 'Colin'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

    def test_soft_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim (soft)."""
        # Base cases
        self.assertEqual(self.cmp_j_soft.sim('', ''), 1.0)
        self.assertEqual(self.cmp_j_soft.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_j_soft.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_j_soft.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_j_soft.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_j_soft.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_j_soft.sim('abcd', 'efgh'), 0.1)

        self.assertAlmostEqual(
            self.cmp_j_soft.sim('Nigel', 'Niall'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_j_soft.sim('Niall', 'Nigel'), 0.4444444444
        )
        self.assertAlmostEqual(self.cmp_j_soft.sim('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp_j_soft.sim('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp_j_soft.sim('ATCAACGAGT', 'AACGATTAG'), 0.6071428571428571
        )

    def test_fuzzy_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim (fuzzy)."""
        # Base cases
        self.assertEqual(self.cmp_j_fuzzy.sim('', ''), 1.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('abcd', 'efgh'), 0.1)

        self.assertAlmostEqual(self.cmp_j_fuzzy.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp_j_fuzzy.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(
            self.cmp_j_fuzzy.sim('Colin', 'Coiln'), 0.72222222222
        )
        self.assertAlmostEqual(
            self.cmp_j_fuzzy.sim('Coiln', 'Colin'), 0.72222222222
        )
        self.assertAlmostEqual(
            self.cmp_j_fuzzy.sim('ATCAACGAGT', 'AACGATTAG'), 0.7857142857142857
        )

    def test_linkage_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim (group linkage)."""
        # Base cases
        self.assertEqual(self.cmp_j_linkage.sim('', ''), 1.0)
        self.assertEqual(self.cmp_j_linkage.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_j_linkage.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_j_linkage.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_j_linkage.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_j_linkage.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_j_linkage.sim('abcd', 'efgh'), 0.1)

        self.assertAlmostEqual(
            self.cmp_j_linkage.sim('Nigel', 'Niall'), 0.4444444444444444
        )
        self.assertAlmostEqual(
            self.cmp_j_linkage.sim('Niall', 'Nigel'), 0.5
        )
        self.assertAlmostEqual(self.cmp_j_linkage.sim('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp_j_linkage.sim('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp_j_linkage.sim('ATCAACGAGT', 'AACGATTAG'),
            0.6428571428571429,
        )

    def test_token_distance(self):
        """Test abydos.distance._TokenDistance members."""
        pass


if __name__ == '__main__':
    unittest.main()
