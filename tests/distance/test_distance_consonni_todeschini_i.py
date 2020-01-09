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

"""abydos.tests.distance.test_distance_consonni_todeschini_i.

This module contains unit tests for abydos.distance.ConsonniTodeschiniI
"""

import unittest

from abydos.distance import ConsonniTodeschiniI


class ConsonniTodeschiniITestCases(unittest.TestCase):
    """Test ConsonniTodeschiniI functions.

    abydos.distance.ConsonniTodeschiniI
    """

    cmp = ConsonniTodeschiniI()
    cmp_no_d = ConsonniTodeschiniI(alphabet=0)

    def test_consonni_todeschini_i_sim(self):
        """Test abydos.distance.ConsonniTodeschiniI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9996172903036489)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9996172903036489)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9992336018090547)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9992336018090547)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9980766131469967)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9988489295)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9988489295)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9988489295)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9988489295)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9986562228
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.6020599913
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.6020599913
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.6020599913
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.6020599913
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.7678740744
        )

    def test_consonni_todeschini_i_dist(self):
        """Test abydos.distance.ConsonniTodeschiniI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0003827096963511245)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0003827096963511245)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0007663981909452611)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0007663981909452611)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.001923386853003306)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0011510705)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0011510705)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0011510705)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0011510705)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0013437772
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.3979400087
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.3979400087
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.3979400087
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.3979400087
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.2321259256
        )


if __name__ == '__main__':
    unittest.main()
