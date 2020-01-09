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

"""abydos.tests.distance.test_distance_koppen_i.

This module contains unit tests for abydos.distance.KoppenI
"""

import unittest

from abydos.distance import KoppenI


class KoppenITestCases(unittest.TestCase):
    """Test KoppenI functions.

    abydos.distance.KoppenI
    """

    cmp = KoppenI()
    cmp_no_d = KoppenI(alphabet=0)

    def test_koppen_i_sim(self):
        """Test abydos.distance.KoppenI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.49936143039591324)
        self.assertEqual(self.cmp.sim('', 'a'), 0.49936143039591324)
        self.assertEqual(self.cmp.sim('abc', ''), 0.4987212276214834)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.4987212276214834)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.49679075738125805)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7471079692)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7471079692)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7471079692)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7471079692)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.8295625943
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0
        )

    def test_koppen_i_dist(self):
        """Test abydos.distance.KoppenI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.5006385696040867)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5006385696040867)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5012787723785166)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5012787723785166)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.503209242618742)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2528920308)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2528920308)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2528920308)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2528920308)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.1704374057
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.0
        )

    def test_koppen_i_corr(self):
        """Test abydos.distance.KoppenI.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), -0.0012771392081735637)
        self.assertEqual(self.cmp.corr('', 'a'), -0.0012771392081735637)
        self.assertEqual(self.cmp.corr('abc', ''), -0.002557544757033164)
        self.assertEqual(self.cmp.corr('', 'abc'), -0.002557544757033164)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.006418485237483896)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.4942159383)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.4942159383)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.4942159383)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.4942159383)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.6591251885
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -1.0
        )


if __name__ == '__main__':
    unittest.main()
