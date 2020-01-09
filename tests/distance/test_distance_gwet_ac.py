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

"""abydos.tests.distance.test_distance_gwet_ac.

This module contains unit tests for abydos.distance.GwetAC
"""

import unittest

from abydos.distance import GwetAC


class GwetACTestCases(unittest.TestCase):
    """Test GwetAC functions.

    abydos.distance.GwetAC
    """

    cmp = GwetAC()
    cmp_no_d = GwetAC(alphabet=0)

    def test_gwet_ac_sim(self):
        """Test abydos.distance.GwetAC.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9987212317930483)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9987212317930483)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9974359309794483)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9974359309794483)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9935405839180314)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9961144519)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9961144519)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9961144519)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9961144519)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9954145343
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.4)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.4)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.4)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.6
        )

    def test_gwet_ac_dist(self):
        """Test abydos.distance.GwetAC.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0012787682069517192)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0012787682069517192)
        self.assertEqual(self.cmp.dist('abc', ''), 0.002564069020551729)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.002564069020551729)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.00645941608196865)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0038855481)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0038855481)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0038855481)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0038855481)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0045854657
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.6)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.6)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.6)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.6)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.4
        )

    def test_gwet_ac_corr(self):
        """Test abydos.distance.GwetAC.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.9974424635860967)
        self.assertEqual(self.cmp.corr('', 'a'), 0.9974424635860967)
        self.assertEqual(self.cmp.corr('abc', ''), 0.9948718619588964)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.9948718619588964)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), 0.9870811678360627)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.9922289037)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.9922289037)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.9922289037)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.9922289037)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.9908290686
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -0.2)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), 0.2
        )


if __name__ == '__main__':
    unittest.main()
