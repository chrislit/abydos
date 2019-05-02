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

"""abydos.tests.distance.test_distance_goodman_kruskal_tau_a.

This module contains unit tests for abydos.distance.GoodmanKruskalTauA
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import GoodmanKruskalTauA
from abydos.tokenizer import QGrams


class GoodmanKruskalTauATestCases(unittest.TestCase):
    """Test GoodmanKruskalTauA functions.

    abydos.distance.GoodmanKruskalTauA
    """

    cmp = GoodmanKruskalTauA()
    cmp_no_d = GoodmanKruskalTauA(alphabet=0)

    def test_goodman_kruskal_tau_a_sim(self):
        """Test abydos.distance.GoodmanKruskalTauA.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.748403575989782)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 4.119695274745721e-05)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.3290773882)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.3290773882)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.3290773882)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.3290773882)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4593665172
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.3333333333333333)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.2727272727
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.2727272727
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.2727272727
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.2727272727
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.2437299035
        )

        self.assertEqual(
            GoodmanKruskalTauA(intersection_type='soft', alphabet=64, tokenizer=QGrams(qval=range(2, 4), skip=1)).sim('became', 'emigrant'),
            0.0
        )
        self.assertEqual(
            GoodmanKruskalTauA(intersection_type='soft', alphabet=64, tokenizer=QGrams(qval=range(2, 4), skip=1)).sim('emigrant', 'became'),
            0.0
        )

    def test_goodman_kruskal_tau_a_dist(self):
        """Test abydos.distance.GoodmanKruskalTauA.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.251596424010218)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.9999588030472526)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.6709226118)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.6709226118)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.6709226118)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.6709226118)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5406334828
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.6666666666666667)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.7272727273
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.7272727273
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.7272727273
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.7272727273
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.7562700965
        )


if __name__ == '__main__':
    unittest.main()
