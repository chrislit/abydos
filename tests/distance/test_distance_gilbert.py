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

"""abydos.tests.distance.test_distance_gilbert.

This module contains unit tests for abydos.distance.Gilbert
"""

import unittest

from abydos.distance import Gilbert


class GilbertTestCases(unittest.TestCase):
    """Test Gilbert functions.

    abydos.distance.Gilbert
    """

    cmp = Gilbert()
    cmp_no_d = Gilbert(alphabet=0)

    def test_gilbert_sim(self):
        """Test abydos.distance.Gilbert.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.4984005118362124)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.664957265)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.664957265)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.664957265)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.664957265)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7474691699
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(
            self.cmp_no_d.sim('abcd', 'efgh'), 0.33333333333333337
        )

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.4)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.4)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.4)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.4302325581
        )

    def test_gilbert_dist(self):
        """Test abydos.distance.Gilbert.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5015994881637875)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.335042735)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.335042735)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.335042735)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.335042735)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2525308301
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.6666666666666666
        )

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.6)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.6)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.6)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.6)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5697674419
        )

    def test_gilbert_corr(self):
        """Test abydos.distance.Gilbert.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.003198976327575176)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.3299145299)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.3299145299)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.3299145299)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.3299145299)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.4949383398
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(
            self.cmp_no_d.corr('abcd', 'efgh'), -0.3333333333333333
        )

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -0.2)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -0.2)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.1395348837
        )


if __name__ == '__main__':
    unittest.main()
