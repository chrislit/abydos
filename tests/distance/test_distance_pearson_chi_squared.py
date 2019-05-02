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

"""abydos.tests.distance.test_distance_pearson_chi_squared.

This module contains unit tests for abydos.distance.PearsonChiSquared
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import PearsonChiSquared
from abydos.tokenizer import QSkipgrams


class PearsonChiSquaredTestCases(unittest.TestCase):
    """Test PearsonChiSquared functions.

    abydos.distance.PearsonChiSquared
    """

    cmp = PearsonChiSquared()
    cmp_no_d = PearsonChiSquared(alphabet=0)

    def test_pearson_chi_squared_sim(self):
        """Test abydos.distance.PearsonChiSquared.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.4999794015236281)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.623079414)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.623079414)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.623079414)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.623079414)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7197346065
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.375)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.375)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.375)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.375)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.4454545455
        )

    def test_pearson_chi_squared_dist(self):
        """Test abydos.distance.PearsonChiSquared.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5000205984763719)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.376920586)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.376920586)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.376920586)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.376920586)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2802653935
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.625)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.625)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.625)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.625)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5545454545
        )

    def test_pearson_chi_squared_sim_score(self):
        """Test abydos.distance.PearsonChiSquared.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 784.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 784.0)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), 0.032298410951138765
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 192.9885210909
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 192.9885210909
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 192.9885210909
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 192.9885210909
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 344.5438630111
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 4.0)
        self.assertEqual(self.cmp_no_d.sim_score('abcd', 'efgh'), 10.0)

        self.assertAlmostEqual(self.cmp_no_d.sim_score('Nigel', 'Niall'), 2.25)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Niall', 'Nigel'), 2.25)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Colin', 'Coiln'), 2.25)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Coiln', 'Colin'), 2.25)
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), 1.5272727273
        )

        self.assertEqual(PearsonChiSquared(alphabet=None, tokenizer=QSkipgrams(qval=2)).sim_score('eh', 'a'), 0.0)

    def test_pearson_chi_squared_corr(self):
        """Test abydos.distance.PearsonChiSquared.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(
            self.cmp.corr('abcd', 'efgh'), -4.1196952743799446e-05
        )

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.2461588279)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.2461588279)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.2461588279)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.2461588279)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.439469213
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -0.25)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -0.25)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -0.25)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -0.25)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.1090909091
        )


if __name__ == '__main__':
    unittest.main()
