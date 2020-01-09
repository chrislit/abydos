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

"""abydos.tests.distance.test_distance_kuhns_v.

This module contains unit tests for abydos.distance.KuhnsV
"""

import unittest

from abydos.distance import KuhnsV


class KuhnsVTestCases(unittest.TestCase):
    """Test KuhnsV functions.

    abydos.distance.KuhnsV
    """

    cmp = KuhnsV()
    cmp_no_d = KuhnsV(alphabet=0)

    def test_kuhns_v_sim(self):
        """Test abydos.distance.KuhnsV.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertAlmostEqual(self.cmp.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7480719794)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.8162413266
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.25)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.35
        )

    def test_kuhns_v_dist(self):
        """Test abydos.distance.KuhnsV.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.5)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertAlmostEqual(
            self.cmp.dist('abcd', 'efgh'), 0.503209242618742
        )

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2519280206)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.1837586734
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.75)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.65
        )

    def test_kuhns_v_corr(self):
        """Test abydos.distance.KuhnsV.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertAlmostEqual(
            self.cmp.corr('abcd', 'efgh'), -0.006418485237484
        )

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.4961439589)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.6324826532
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -0.5)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.3
        )


if __name__ == '__main__':
    unittest.main()
