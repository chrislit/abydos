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

"""abydos.tests.distance.test_distance_kuhns_ii.

This module contains unit tests for abydos.distance.KuhnsII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsII


class KuhnsIITestCases(unittest.TestCase):
    """Test KuhnsII functions.

    abydos.distance.KuhnsII
    """

    cmp = KuhnsII()
    cmp_no_d = KuhnsII(alphabet=0)

    def test_kuhns_ii_sim(self):
        """Test abydos.distance.KuhnsII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.3333333333333333)
        self.assertEqual(self.cmp.sim('a', ''), 0.3333333333333333)
        self.assertEqual(self.cmp.sim('', 'a'), 0.3333333333333333)
        self.assertEqual(self.cmp.sim('abc', ''), 0.3333333333333333)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.3333333333333333)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9965986394557823)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.32908163265306123)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6615646259)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6615646259)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6615646259)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6615646259)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7490723562
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.3333333333333333)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.3333333333333333)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.3333333333333333)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.3333333333333333)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.3333333333333333)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.3333333333333333)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.2813852814
        )

    def test_kuhns_ii_dist(self):
        """Test abydos.distance.KuhnsII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.6666666666666667)
        self.assertEqual(self.cmp.dist('a', ''), 0.6666666666666667)
        self.assertEqual(self.cmp.dist('', 'a'), 0.6666666666666667)
        self.assertEqual(self.cmp.dist('abc', ''), 0.6666666666666667)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.6666666666666667)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.003401360544217691)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.6709183673469388)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3384353741)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3384353741)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.3384353741)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.3384353741)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2509276438
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.6666666666666667)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.6666666666666667)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.6666666666666667)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.6666666666666667)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.6666666666666667)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.6666666666666667)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.7777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.7777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.7777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.7777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.7186147186
        )

    def test_kuhns_ii_corr(self):
        """Test abydos.distance.KuhnsII.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 0.9948979591836735)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.006377551020408163)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.4923469388)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.4923469388)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.4923469388)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.4923469388)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.6236085343
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -0.5)

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.0779220779
        )


if __name__ == '__main__':
    unittest.main()
