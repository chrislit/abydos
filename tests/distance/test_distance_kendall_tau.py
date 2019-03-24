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

"""abydos.tests.distance.test_distance_kendall_tau.

This module contains unit tests for abydos.distance.KendallTau
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KendallTau


class KendallTauTestCases(unittest.TestCase):
    """Test KendallTau functions.

    abydos.distance.KendallTau
    """

    cmp = KendallTau()
    cmp_no_d = KendallTau(alphabet=0)

    def test_kendall_tau_sim(self):
        """Test abydos.distance.KendallTau.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5012771392081737)
        self.assertEqual(self.cmp.sim('a', ''), 0.5012706231918055)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5012706231918055)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5012641071754372)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5012641071754372)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.5012771392081737)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.5012445591263325)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5012575912)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5012575912)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5012575912)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5012575912)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5012543332
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.16666666666666669)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.16666666666666669)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.8333333333333333)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.3888888888888889)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.4583333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.4583333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.4583333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.4583333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

    def test_kendall_tau_dist(self):
        """Test abydos.distance.KendallTau.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.49872286079182626)
        self.assertEqual(self.cmp.dist('a', ''), 0.4987293768081945)
        self.assertEqual(self.cmp.dist('', 'a'), 0.4987293768081945)
        self.assertEqual(self.cmp.dist('abc', ''), 0.49873589282456277)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.49873589282456277)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.49872286079182626)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.4987554408736675)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4987424088)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4987424088)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.4987424088)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.4987424088)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4987456668
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.8333333333333333)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.8333333333333333)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.16666666666666674)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.6111111111111112
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.5416666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.5416666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.5416666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.5416666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

    def test_kendall_tau_corr(self):
        """Test abydos.distance.KendallTau.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.002554278416347382)
        self.assertEqual(self.cmp.corr('a', ''), 0.0025412463836109156)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0025412463836109156)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0025282143508744493)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0025282143508744493)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 0.002554278416347382)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), 0.0024891182526650506)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.0025151823)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.0025151823)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.0025151823)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.0025151823)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.0025086663
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), -2.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), -2.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), -0.6666666666666666)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), -0.6666666666666666)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.6666666666666666)
        self.assertEqual(
            self.cmp_no_d.corr('abcd', 'efgh'), -0.2222222222222222
        )

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.0833333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.0833333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.0833333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.0833333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), 0.0
        )


if __name__ == '__main__':
    unittest.main()
