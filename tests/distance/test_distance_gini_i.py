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

"""abydos.tests.distance.test_distance_gini_i.

This module contains unit tests for abydos.distance.GiniI
"""

import unittest

from abydos.distance import GiniI


class GiniITestCases(unittest.TestCase):
    """Test GiniI functions.

    abydos.distance.GiniI
    """

    cmp = GiniI()
    cmp_no_d = GiniI(alphabet=0)

    def test_gini_i_sim(self):
        """Test abydos.distance.GiniI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.8742017879948869)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.4967907573812552)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7479180013)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7479180013)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7479180013)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7479180013)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7970761293
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.6666666666666666)
        self.assertEqual(
            self.cmp_no_d.sim('abcd', 'efgh'), 2.220446049250313e-16
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.4545454545
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.4545454545
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.4545454545
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.4545454545
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.539317703
        )

    def test_gini_i_dist(self):
        """Test abydos.distance.GiniI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.5)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.1257982120051131)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5032092426187448)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2520819987)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2520819987)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2520819987)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2520819987)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2029238707
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.33333333333333337)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.9999999999999998
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.5454545455
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.5454545455
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.5454545455
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.5454545455
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.460682297
        )

    def test_gini_i_corr(self):
        """Test abydos.distance.GiniI.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 0.7484035759897738)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.006418485237489576)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.4958360026)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.4958360026)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.4958360026)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.4958360026)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.5941522586
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.33333333333333326)
        self.assertEqual(
            self.cmp_no_d.corr('abcd', 'efgh'), -0.9999999999999996
        )

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.0909090909
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.0909090909
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.0909090909
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.0909090909
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), 0.078635406
        )


if __name__ == '__main__':
    unittest.main()
