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

"""abydos.tests.distance.test_distance_gwet_gamma.

This module contains unit tests for abydos.distance.GwetGamma
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import GwetGamma


class GwetGammaTestCases(unittest.TestCase):
    """Test GwetGamma functions.

    abydos.distance.GwetGamma
    """

    cmp = GwetGamma()
    cmp_no_d = GwetGamma(alphabet=0)

    def test_gwet_gamma_sim(self):
        """Test abydos.distance.GwetGamma.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9974424635860967)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9974424635860967)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9948718619588964)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9948718619588964)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9870811678360627)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9922289037)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9922289037)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9922289037)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9922289037)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9908290686
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), -1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), -1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), -0.2)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.2
        )

    def test_gwet_gamma_dist(self):
        """Test abydos.distance.GwetGamma.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0025575364139033274)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0025575364139033274)
        self.assertEqual(self.cmp.dist('abc', ''), 0.005128138041103569)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.005128138041103569)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.0129188321639373)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0077710963)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0077710963)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0077710963)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0077710963)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0091709314
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), 2.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 2.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 2.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 2.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.2)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.2)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.2)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.2)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.8
        )


if __name__ == '__main__':
    unittest.main()
