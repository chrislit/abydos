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

"""abydos.tests.distance.test_distance_kuhns_iv.

This module contains unit tests for abydos.distance.KuhnsIV
"""

import unittest

from abydos.distance import KuhnsIV


class KuhnsIVTestCases(unittest.TestCase):
    """Test KuhnsIV functions.

    abydos.distance.KuhnsIV
    """

    cmp = KuhnsIV()
    cmp_no_d = KuhnsIV(alphabet=0)

    def test_kuhns_iv_sim(self):
        """Test abydos.distance.KuhnsIV.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9974489795918368)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.4968112244897959)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7461734694)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7461734694)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7461734694)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7461734694)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.8429846939
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.25)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.4166666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.4166666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.4166666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.4166666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.4571428571
        )

    def test_kuhns_iv_dist(self):
        """Test abydos.distance.KuhnsIV.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.5)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0025510204081632404)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.503188775510204)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2538265306)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2538265306)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2538265306)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2538265306)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.1570153061
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 0.75)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.5833333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.5833333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.5833333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.5833333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5428571429
        )

    def test_kuhns_iv_corr(self):
        """Test abydos.distance.KuhnsIV.corr."""
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
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.6859693878
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
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.0857142857
        )


if __name__ == '__main__':
    unittest.main()
