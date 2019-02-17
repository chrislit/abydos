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

"""abydos.tests.distance.test_distance_meta_levenshtein.

This module contains unit tests for abydos.distance.MetaLevenshtein
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import MetaLevenshtein


class MetaLevenshteinTestCases(unittest.TestCase):
    """Test MetaLevenshtein functions.

    abydos.distance.MetaLevenshtein
    """

    cmp = MetaLevenshtein()

    def test_meta_levenshtein_dist(self):
        """Test abydos.distance.MetaLevenshtein.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.8463953614713058)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3077801314)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3077801314)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.3077801314)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.3077801314)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2931752664
        )

    def test_meta_levenshtein_dist_abs(self):
        """Test abydos.distance.MetaLevenshtein.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 3.385581445885223)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 1.5389006572
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 1.5389006572
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 1.5389006572
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 1.5389006572
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 2.9317526638
        )


if __name__ == '__main__':
    unittest.main()
