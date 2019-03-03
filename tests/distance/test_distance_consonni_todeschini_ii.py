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

"""abydos.tests.distance.test_distance_consonni_todeschini_ii.

This module contains unit tests for abydos.distance.ConsonniTodeschiniII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ConsonniTodeschiniII


class ConsonniTodeschiniIITestCases(unittest.TestCase):
    """Test ConsonniTodeschiniII functions.

    abydos.distance.ConsonniTodeschiniII
    """

    cmp = ConsonniTodeschiniII()
    cmp_no_d = ConsonniTodeschiniII(alphabet=0)

    def test_consonni_todeschini_ii_sim(self):
        """Test abydos.distance.ConsonniTodeschiniII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.8351838558230296)
        self.assertEqual(self.cmp.sim('', 'a'), 0.8351838558230296)
        self.assertEqual(self.cmp.sim('abc', ''), 0.7585487129939101)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.7585487129939101)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.640262668568961)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7080704349)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7080704349)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7080704349)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7080704349)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6880377723
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.15490196)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.15490196)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.15490196)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.15490196)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.2321259256
        )

    def test_consonni_todeschini_ii_dist(self):
        """Test abydos.distance.ConsonniTodeschiniII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.16481614417697044)
        self.assertEqual(self.cmp.dist('', 'a'), 0.16481614417697044)
        self.assertEqual(self.cmp.dist('abc', ''), 0.24145128700608987)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.24145128700608987)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.35973733143103903)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2919295651)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2919295651)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2919295651)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2919295651)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3119622277
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
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.84509804
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.84509804
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.84509804
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.84509804
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.7678740744
        )


if __name__ == '__main__':
    unittest.main()
