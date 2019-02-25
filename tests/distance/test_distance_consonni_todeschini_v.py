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

"""abydos.tests.distance.test_distance_consonni_todeschini_v.

This module contains unit tests for abydos.distance.ConsonniTodeschiniV
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ConsonniTodeschiniV


class ConsonniTodeschiniVTestCases(unittest.TestCase):
    """Test ConsonniTodeschiniV functions.

    abydos.distance.ConsonniTodeschiniV
    """

    cmp = ConsonniTodeschiniV()
    cmp_no_d = ConsonniTodeschiniV(alphabet=1)

    def test_consonni_todeschini_v_sim(self):
        """Test abydos.distance.ConsonniTodeschiniV.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.6737189369511224)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.2728145951429799)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4562952871)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4562952871)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4562952871)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4562952871)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5047118763
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), -0.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), -0.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), -0.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), -0.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), -0.6556580454
        )

    def test_consonni_todeschini_v_dist(self):
        """Test abydos.distance.ConsonniTodeschiniV.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.3262810630488776)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.27281459514298)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5437047129)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5437047129)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5437047129)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5437047129)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4952881237
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 1.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 1.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 1.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 1.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.6556580454
        )


if __name__ == '__main__':
    unittest.main()